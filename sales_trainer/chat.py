from langchain_gigachat.chat_models import GigaChat

from sales_trainer.config import ChatAgentConfig


class ChatAgent:
    def __init__(self, cfg: ChatAgentConfig) -> None:
        self.cfg = cfg
        self.giga = GigaChat(
            credentials=self.cfg.giga_chat_token.get_secret_value(), verify_ssl_certs=False
        )
