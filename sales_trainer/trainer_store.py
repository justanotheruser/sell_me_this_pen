import logging

from sales_trainer.config import config
from sales_trainer.trainer import GigachatTrainer

logger = logging.getLogger(__name__)


class TrainerStore:
    def __init__(self):
        self._store: dict[str, GigachatTrainer] = {}

    def add(self, sid: str) -> GigachatTrainer:
        trainer = GigachatTrainer(config.trainer)
        self._store[sid] = trainer
        return trainer

    def get(self, sid: str) -> GigachatTrainer | None:
        return self._store.get(sid, None)

    def remove(self, sid: str) -> None:
        if sid in self._store:
            del self._store[sid]
        else:
            logger.warning(f"No trainer for sid {sid}")


trainer_store = TrainerStore()
