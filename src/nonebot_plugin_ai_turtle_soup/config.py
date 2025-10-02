from pydantic import BaseModel, Field
from nonebot import get_plugin_config


class Config(BaseModel):
    """插件配置类"""
    
    # OpenAI API 配置 - 生成谜题
    ats_openai_generate_api_key: str = Field(default="")
    ats_openai_generate_base_url: str = Field(default="")
    ats_openai_generate_model: str = Field(default="")
    
    # OpenAI API 配置 - 评判问题
    ats_openai_judge_api_key: str = Field(default="")
    ats_openai_judge_base_url: str = Field(default="")
    ats_openai_judge_model: str = Field(default="")
    
    # 游戏配置
    ats_max_questions: int = Field(default=50)
    ats_timeout: int = Field(default=7200)


# 从 .env 文件加载配置
plugin_config = get_plugin_config(Config)
