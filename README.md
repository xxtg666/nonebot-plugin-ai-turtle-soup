![](https://socialify.git.ci/xxtg666/nonebot-plugin-ai-turtle-soup/image?description=1&forks=1&issues=1&language=1&logo=https://raw.githubusercontent.com/xxtg666/nonebot-plugin-ai-turtle-soup/main/docs/nbp_logo.png&name=1&owner=1&pulls=1&stargazers=1&theme=Light)

<div align="center">

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/xxtg666/nonebot-plugin-ai-turtle-soup.svg?style=for-the-badge" alt="license">
</a>

<a href="https://pypi.python.org/pypi/nonebot-plugin-ai-turtle-soup">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-ai-turtle-soup.svg?style=for-the-badge" alt="pypi">
</a>

<img src="https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge" alt="python">

</div>

## 📖 介绍

一个由 AI 驱动的海龟汤(情境猜谜)游戏插件，为 NoneBot2 机器人提供互动式推理游戏体验。

### 什么是海龟汤？

海龟汤(Situation Puzzle / Lateral Thinking Puzzle)是一种情境猜谜游戏：
- 🧩 系统给出一个离奇的情境描述(汤面)
- 🤔 玩家通过提出封闭式问题来推理
- 💡 AI 只能回答"是"、"否"或"不重要"
- 🎯 最终推理出完整的故事真相(汤底)

### 特色功能

- 🤖 **AI 生成谜题** - 每次都能获得全新的创意谜题
- 🎮 **智能主持** - AI 自动判断问题并给出合理答案
- 📊 **进度跟踪** - 实时显示游戏进度百分比
- 💡 **提示系统** - 卡关时可请求提示
- ⭐ **谜题评分** - 自动评估谜题质量(悬念度/逻辑性/创意性/可玩性)
- 🎨 **主题定制** - 可指定主题生成特定类型的谜题
- 🔄 **进度重算** - 支持重新评估当前进度

## 💿 安装

### 先决条件

在安装之前，请确保您的环境符合以下条件：

1. 拥有一个能够运行的 Python，版本在 3.9 及以上
2. 已经安装并配置好 pip 等任意一款 Python3 包管理器
3. 已经创建或拥有了一个 NoneBot2 机器人项目
4. 拥有可用的 OpenRouter API 或兼容的 API 服务

### 安装方法

<details>
<summary>通过文件安装</summary>

1. 在您的 `pyproject.toml` 中配置一个插件目录
```toml
plugin_dirs = ["src/plugins"]
```
> 您需要确保此目录存在，下文将使用 `插件目录` 代指此目录。

2. [下载本仓库](https://github.com/xxtg666/nonebot-plugin-ai-turtle-soup/archive/refs/heads/main.zip)

3. 将 `src` 文件夹中的 `nonebot_plugin_ai_turtle_soup` 文件夹解压到插件目录

4. 安装依赖
> 进入 `requirements.txt` 同目录下执行
```bash
pip install -r requirements.txt
```

</details>

<details>
<summary>通过 PIP 安装</summary>

1. 使用 pip 安装插件
```bash
pip install nonebot-plugin-ai-turtle-soup
```

2. 修改 `pyproject.toml` 在 `plugins` 中添加 `nonebot_plugin_ai_turtle_soup`

</details>

## ⚙️ 配置

请在机器人目录中创建一个 `.env` 文件(或编辑对应 `.env` 文件，可能为 `.env.dev` 或 `.env.prod`)，然后将下方的配置内容复制进去并修改。

### 配置项说明

```env
# OpenAI API Configuration - 生成谜题
ATS_OPENAI_GENERATE_API_KEY=
ATS_OPENAI_GENERATE_BASE_URL=https://api-inference.modelscope.cn/v1
ATS_OPENAI_GENERATE_MODEL=ZhipuAI/GLM-4.5 # 推荐使用 GLM-4.5 / GLM-4.6

# OpenAI API Configuration - 评判问题、刷新进度、谜题打分
ATS_OPENAI_JUDGE_API_KEY=
ATS_OPENAI_JUDGE_BASE_URL=https://openrouter.ai/api/v1
ATS_OPENAI_JUDGE_MODEL=x-ai/grok-4-fast # 推荐使用 grok-4-fast，最好是带 reasoning 的模型

# 游戏配置
ATS_MAX_QUESTIONS=50  # 每局游戏最大提问次数
ATS_TIMEOUT=7200      # 游戏超时时间(秒)，默认2小时
```

### 配置说明

- **双 API 配置**：插件使用两套 API 配置
  - `GENERATE`: 用于生成新谜题(需要较高创造力)
  - `JUDGE`: 用于游戏主持、回答问题、计算进度(需要较高准确性)
  - 可以配置为相同或不同的 API 服务
  
- **API 兼容性**：支持 OpenRouter API 以及任何兼容 OpenAI 格式的 API 服务

## 🎉 使用

### 基本命令

- `/开始海龟汤` - 开始一局随机主题的新游戏
- `/开始海龟汤 [主题]` - 开始指定主题的新游戏(如: `/开始海龟汤 密室`)
- `@bot <问题>` - 向 AI 提问(需要是封闭式问题)
- `@bot 查看进度` - 查看当前游戏进度和历史记录
- `@bot 提示` - 获取一条提示信息
- `@bot 重新计算进度` - 重新评估当前游戏进度
- `@bot 放弃` - 放弃游戏并查看完整答案
- `/海龟汤帮助` - 查看详细帮助信息

### 游玩技巧

- ✅ **好的问题**：
  - "这是故意的吗？"
  - "他的身体有什么特殊情况吗？"
  - "这件事发生在室内吗？"
  - "时间因素重要吗？"

- ❌ **不好的问题**：
  - "发生了什么？"(太开放)
  - "他为什么这么做？"(无法用是/否回答)
  - "是不是A或者B？"(尽量避免多选)

### 多人游戏

- 支持群组和频道内多人协作
- 每个群组/频道独立维护游戏状态
- 所有成员都可以提问
- 建议协作讨论，共同推理

## ⚠️ 注意事项

- 本插件需要调用 AI API，可能会产生相应的 API 费用
- 建议设置合理的 `ATS_MAX_QUESTIONS` 以控制单局游戏的 API 调用次数
- 游戏会话会在超时时间(`ATS_TIMEOUT`)后自动清除