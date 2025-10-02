from pydantic import BaseModel, Field
from nonebot import get_driver


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
    
    def get_generate_api_key(self) -> str:
        """获取生成谜题的API Key"""
        return self.ats_openai_generate_api_key
    
    def get_generate_base_url(self) -> str:
        """获取生成谜题的Base URL"""
        return self.ats_openai_generate_base_url

    def get_generate_model(self) -> str:
        """获取生成谜题的模型"""
        return self.ats_openai_generate_model

    def get_judge_api_key(self) -> str:
        """获取评判问题的API Key"""
        return self.ats_openai_judge_api_key

    def get_judge_base_url(self) -> str:
        """获取评判问题的Base URL"""
        return self.ats_openai_judge_base_url

    def get_judge_model(self) -> str:
        """获取评判问题的模型"""
        return self.ats_openai_judge_model


# 从 .env 文件加载配置
plugin_config = Config.parse_obj(get_driver().config.dict())
