import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

from sales_trainer.config import TrainerConfig

logger = logging.getLogger(__name__)


class GigachatTrainer:
    def __init__(self, cfg: TrainerConfig) -> None:
        self.cfg = cfg
        self.giga = GigaChat(
            access_token=self.cfg.giga_chat_token.get_secret_value(), verify_ssl_certs=False
        )
        self.is_started = False

    def invoke(self, message: str) -> str:
        messages = [HumanMessage(message)]
        if not self.is_started:
            messages = [SystemMessage(content=self.cfg.prompt.get_secret_value())] + messages
        resp = self.giga.invoke(messages)
        self.is_started = True
        logger.info(f"Model used: {resp.response_metadata['model_name']}")
        logger.info(f"Tokens used: {resp.response_metadata['token_usage']}")
        logger.info(f"LLM answer: {resp.content}")
        return resp.content
