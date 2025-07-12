import logging

from langchain_core.messages import (
    HumanMessage,
    MessageLikeRepresentation,
    SystemMessage,
)
from langchain_gigachat.chat_models import GigaChat

from sales_trainer.trainer.config import TrainerConfigWithAuth

logger = logging.getLogger(__name__)


class GigachatTrainer:
    def __init__(self, cfg: TrainerConfigWithAuth) -> None:
        self.cfg = cfg
        # TODO: recreate GigaChat with fresh access token if invoke fails with auth error
        self.giga = GigaChat(
            access_token=self.cfg.access_token.get_secret_value(), verify_ssl_certs=False  # type: ignore
        )
        self.messages: list[MessageLikeRepresentation] = [
            SystemMessage(content=self.cfg.prompt.get_secret_value())
        ]

    def invoke(self, message: str) -> str:
        self.messages.append(HumanMessage(message))
        resp = self.giga.invoke(self.messages)
        self.is_started = True
        logger.info(f"Model used: {resp.response_metadata['model_name']}")
        logger.info(f"Tokens used: {resp.response_metadata['token_usage']}")
        logger.info(f"LLM answer: {resp.content}")
        return resp.content  # type: ignore[return-value]
