"""
NoneBot2 Turtle Soup Game Plugin
海龟汤游戏插件
"""
from nonebot import on_message
from nonebot.plugin import PluginMetadata, require
from nonebot.rule import to_me
from nonebot.exception import FinishedException
from nonebot.adapters import Event
from .game_manager import GameManager
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="海龟汤游戏",
    description="AI驱动的海龟汤(情境猜谜)游戏",
    usage="""
    /开始海龟汤 [主题] - 开始一局新游戏
    @bot <问题> - 向AI提问(只能用是/否回答的问题)
    @bot 查看进度 - 查看当前游戏进度
    @bot 提示 - 获取游戏提示
    @bot 重新计算进度 - 重新分析并计算游戏进度
    @bot 放弃 - 放弃当前游戏并查看答案
    /海龟汤帮助 - 查看帮助信息
    """,
    type="application",
    homepage="https://github.com/xxtg666/nonebot-plugin-ai-turtle-soup",
    config=Config,
)

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    on_alconna,
    UniMessage
)


# 初始化游戏管理器
game_manager = GameManager()

# 定义 Alconna 命令
start_game = on_alconna(
    Alconna(
        "开始海龟汤",
        Args["theme", str, ""],
    ),
    priority=5,
    block=True,
    use_cmd_start=True
)

help_cmd = on_alconna(
    Alconna("海龟汤帮助"),
    priority=5,
    block=True,
    use_cmd_start=True
)

# @bot 消息处理器 - 用于提问、放弃、查看进度、提示、重新计算进度
at_bot_handler = on_message(rule=to_me(), priority=6, block=True)


@start_game.assign("$main")
async def handle_start_game(result: Arparma, event: Event):
    """开始新游戏"""
    session_id = _get_session_id(event)
    
    # 检查是否已有进行中的游戏
    if game_manager.has_active_game(session_id):
        await UniMessage("当前已有进行中的游戏!请先完成或放弃当前游戏。").finish()
    
    # 获取主题参数
    theme = result.query("theme")
    
    await UniMessage("正在生成新的海龟汤谜题,请稍候...").send()
    
    try:
        puzzle = await game_manager.create_game(session_id, theme=theme)

        print(puzzle)

        message_1 = (
            f"🎮 海龟汤游戏开始!\n\n"
            f"📖 题目: {puzzle['title']}\n\n"
            f"🤔 汤面:\n{puzzle['puzzle_setting']}\n\n"
            f"💡 直接 @我 提问即可,例如: @bot 这个人是故意的吗?\n"
            f"问题应该是可以用\"是\"、\"否\"或\"不重要\"回答的\n"
            f"想要放弃请 @我 说\"放弃\"\n"
            f"需要提示请 @我 说\"提示\"\n\n"
            f"📊 当前进度: 0%"
        )
        
        await UniMessage(message_1).send()
        
        # 生成谜题评分
        # await UniMessage("正在评估谜题质量...").send()
        rating = await game_manager.rate_puzzle(session_id)

        message_2 = (
            f"⭐ 谜题评分:\n"
            f"  综合评分: {rating['scores']['overall']}/10\n"
            f"  悬念度: {rating['scores']['suspense']}/10\n"
            f"  逻辑性: {rating['scores']['logic']}/10\n"
            f"  创意性: {rating['scores']['creativity']}/10\n"
            f"  可玩性: {rating['scores']['playability']}/10"
        )
        
        await UniMessage(message_2).finish()
    except FinishedException:
        return
        
    except Exception as e:
        await UniMessage(f"生成游戏失败: {str(e)}\n请检查配置或稍后重试。").finish()


@at_bot_handler.handle()
async def handle_at_bot(event: Event):
    """处理@bot的消息 - 提问、放弃、查看进度、提示、重新计算进度"""
    session_id = _get_session_id(event)
    
    # 获取消息内容
    msg = await UniMessage.generate(event=event)
    text = msg.extract_plain_text().strip()
    
    # 如果是命令开头,不处理(让命令处理器处理)
    if text.startswith('/') or text.startswith('开始海龟汤') or text.startswith('海龟汤帮助'):
        await at_bot_handler.skip()
    
    # 检查是否有活跃游戏
    if not game_manager.has_active_game(session_id):
        # 没有游戏时不响应
        await at_bot_handler.skip()
    
    if not text:
        await UniMessage("请输入你的问题、\"查看进度\"、\"提示\"、\"重新计算进度\"或\"放弃\"").finish()
    
    # 检查是否是查看进度
    if text in ["查看进度", "进度", "当前进度", "看进度", "查询进度"]:
        game = game_manager.get_game(session_id)
        puzzle = game['puzzle']
        
        message = (
            f"📈 当前游戏进度\n\n"
            f"📖 题目: {puzzle['title']}\n\n"
            f"🤔 汤面:\n{puzzle['puzzle_setting']}\n\n"
            f"📊 进度: {game['percent']}%\n"
            f"🔢 已提问: {len(game['history'])}/{game_manager.config.ats_max_questions}次\n\n"
        )
        
        # 显示最近的3个问答
        if game['history']:
            message += "❓ 最近的问答:\n"
            recent_history = game['history'][-3:]
            for i, qa in enumerate(recent_history, 1):
                message += f"{i}. Q: {qa['question']}\n   A: {qa['answer']}\n"
        
        await UniMessage(message).finish()
    
    # 检查是否是提示
    if text in ["提示", "给个提示", "来个提示", "要提示"]:
        hint_result = game_manager.get_next_hint(session_id)
        
        if hint_result is None:
            await UniMessage("暂无可用的提示信息。").finish()
        elif hint_result['finished']:
            await UniMessage(f"所有提示已展示完毕!\n共 {hint_result['total']} 条提示。").finish()
        else:
            message = (
                f"💡 提示 [{hint_result['current']}/{hint_result['total']}]:\n"
                f"{hint_result['hint']}"
            )
            await UniMessage(message).finish()
    
    # 检查是否是重新计算进度
    if text in ["重新计算进度", "重算进度", "重新计算", "重新评估", "更新进度"]:
        await UniMessage("正在重新计算进度...").send()
        
        try:
            new_percent = await game_manager.recalculate_progress(session_id)
            game = game_manager.get_game(session_id)
            
            message = (
                f"🔄 进度已重新计算\n\n"
                f"📊 新的进度: {new_percent}%\n"
                f"🔢 已提问: {len(game['history'])}/{game_manager.config.ats_max_questions}次"
            )
            
            await UniMessage(message).finish()
        except FinishedException:
            return
        except Exception as e:
            await UniMessage(f"重新计算进度失败: {str(e)}").finish()
    
    # 检查是否是放弃
    if text in ["放弃", "我放弃", "不玩了", "公布答案", "看答案", "放弃游戏"]:
        game = game_manager.get_game(session_id)
        
        try:
            result = await game_manager.process_question(session_id, "我放弃了,请告诉我答案")
            game_manager.end_game(session_id)
            
            # 构建附加信息列表
            supplementary_info = "\n".join([f"• {info}" for info in game['puzzle']['supplementary_info']])
            
            message = (
                f"😔 游戏结束\n\n"
                f"📖 题目: {game['puzzle']['title']}\n\n"
                f"🔢 总提问数: {len(game['history'])}\n\n"
                f"📖 正确答案:\n{game['puzzle']['solution']}\n\n"
                f"💡 全部附加信息:\n{supplementary_info}\n\n"
                f"💡 再接再厉!使用 /开始海龟汤 开始新游戏"
            )
            
            await UniMessage(message).finish()
        except FinishedException:
            return
            
        except Exception as e:
            # 即使出错也要结束游戏并显示答案
            game_manager.end_game(session_id)
            # 构建附加信息列表
            supplementary_info = "\n".join([f"• {info}" for info in game['puzzle']['supplementary_info']])
            message = (
                f"📖 正确答案:\n{game['puzzle']['solution']}\n\n"
                f"💡 全部附加信息:\n{supplementary_info}\n\n"
                f"💡 使用 /开始海龟汤 开始新游戏"
            )
            await UniMessage(message).finish()
    
    # 处理提问
    question = text
    game = game_manager.get_game(session_id)
    
    # 检查问题数量限制
    if len(game['history']) >= game_manager.config.ats_max_questions:
        await UniMessage(
            f"已达到最大提问次数({game_manager.config.ats_max_questions}次)!\n"
            f"@我 说\"放弃\"可以查看答案。"
        ).finish()
    
    try:
        result = await game_manager.process_question(session_id, question)
        
        # 构建回复消息
        message = f"❓ 你的问题: {question}\n"
        message += f"💬 回答: {result['reply']}\n"
        message += f"📊 进度: {result['percent']}%\n"
        message += f"🔢 已提问: {len(game['history'])}/{game_manager.config.ats_max_questions}次"
        
        # 检查是否游戏结束
        if result['percent'] >= 100:
            # 构建附加信息列表
            supplementary_info = "\n".join([f"• {info}" for info in game['puzzle']['supplementary_info']])
            
            game_manager.end_game(session_id)
            
            if result['reply'] and result['reply'] not in ["是", "不是", "不重要"]:
                # 玩家猜对了
                message += f"\n\n📖 完整答案:\n{game['puzzle']['solution']}"
                message += f"\n\n💡 全部附加信息:\n{supplementary_info}"
                message += f"\n\n🎉 使用 /开始海龟汤 开始新游戏"
            else:
                # 玩家放弃了
                message += f"\n\n📖 正确答案:\n{game['puzzle']['solution']}"
                message += f"\n\n💡 全部附加信息:\n{supplementary_info}"
        
        await UniMessage(message).finish()
    except FinishedException:
        return
        
    except Exception as e:
        await UniMessage(f"处理问题时出错: {str(e)}").finish()


@help_cmd.assign("$main")
async def handle_help():
    """显示帮助信息"""
    help_text = """
🐢 海龟汤游戏说明

海龟汤(Situation Puzzle)是一种情境猜谜游戏。
系统会给出一个离奇的情境描述(汤面),
你需要通过提问来推理出完整的故事(汤底)。

📜 游戏规则:
1. 只能提出可以用"是"、"否"或"不重要"回答的问题
2. 根据AI的回答逐步推理出真相
3. 进度达到100%表示猜对或放弃

🎮 使用方式:
/开始海龟汤 [主题] - 开始新游戏,可选指定主题
@bot <问题> - 提出问题(例如: @bot 这是故意的吗?)
@bot 查看进度 - 查看当前游戏状态
@bot 提示 - 获取一条提示
@bot 重新计算进度 - 重新分析并计算游戏进度
@bot 放弃 - 放弃游戏并查看答案
/海龟汤帮助 - 显示此帮助

💡 提问技巧:
• 先确认基本事实(人物、地点、时间等)
• 排除法缩小可能性
• 关注异常和矛盾之处
• 注意细节和隐含信息

📝 示例对话:
玩家: /开始海龟汤
机器人: [显示题目和汤面]
玩家: @bot 这个人是故意的吗?
机器人: 不是
玩家: @bot 他的身体有什么特殊情况吗?
机器人: 是
玩家: @bot 查看进度
机器人: [显示当前进度]
...

祝你玩得开心! 🎉
"""
    await UniMessage(help_text.strip()).finish()


def _get_session_id(event: Event) -> str:
    """获取会话ID - 支持多平台"""
    # 尝试获取群组ID
    if hasattr(event, 'group_id') and event.group_id:
        return f"group_{event.group_id}"
    # 尝试获取频道ID
    elif hasattr(event, 'guild_id') and event.guild_id:
        guild_id = event.guild_id
        channel_id = getattr(event, 'channel_id', '')
        return f"guild_{guild_id}_{channel_id}"
    # 尝试获取用户ID
    elif hasattr(event, 'user_id') and event.user_id:
        return f"private_{event.user_id}"
    # 获取不到，使用通用标识
    else:
        return f"unknown_{id(event)}"
