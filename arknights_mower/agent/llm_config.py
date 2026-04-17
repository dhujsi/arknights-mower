from langchain_openai import ChatOpenAI

from arknights_mower.utils import config

DEFAULT_LLM_CONFIGS = {
    "deepseek": {
        "model": "deepseek-chat",
        "base_url": "https://api.deepseek.com/v1",
    },
    "deepseek_reasoner": {
        "model": "deepseek-reasoner",
        "base_url": "https://api.deepseek.com/v1",
    },
}


def resolve_llm_config(api_key: str | None = None) -> dict:
    resolved_api_key = (api_key if api_key is not None else config.conf.ai_key).strip()
    ai_type = (config.conf.ai_type or "").strip()

    if ai_type in DEFAULT_LLM_CONFIGS:
        return {
            **DEFAULT_LLM_CONFIGS[ai_type],
            "api_key": resolved_api_key,
        }

    if ai_type == "openai_compatible":
        model = (config.conf.ai_model or "").strip()
        if not model:
            raise ValueError("missing ai_model for openai_compatible")
        base_url = (config.conf.ai_base_url or "").strip()
        llm_config = {
            "model": model,
            "api_key": resolved_api_key,
        }
        if base_url:
            llm_config["base_url"] = base_url
        return llm_config

    raise ValueError(f"unsupported ai_type={ai_type or '<empty>'}")


def build_chat_openai(api_key: str | None = None, **kwargs) -> ChatOpenAI:
    llm_config = resolve_llm_config(api_key=api_key)
    llm_config.update(kwargs)
    return ChatOpenAI(**llm_config)
