import logging

from apscheduler import Scheduler
from apscheduler.triggers.interval import IntervalTrigger

from sales_trainer.config import TrainerConfig, config
from sales_trainer.trainer.trainer import GigachatTrainer

logger = logging.getLogger(__name__)


class TrainerStore:
    def __init__(self, config: TrainerConfig, scheduler: Scheduler):
        self.store: dict[str, GigachatTrainer] = {}
        self.scheduler = scheduler
        self.renew_task_id = self.scheduler.add_schedule(self.__renew_access_token, trigger=IntervalTrigger(minutes=25))

    def add(self, sid: str) -> GigachatTrainer:
        trainer = GigachatTrainer(config.trainer)
        self.store[sid] = trainer
        return trainer

    def get(self, sid: str) -> GigachatTrainer | None:
        return self.store.get(sid, None)

    def remove(self, sid: str) -> None:
        if sid in self.store:
            del self.store[sid]
        else:
            logger.warning(f"No trainer for sid {sid}")

    def __renew_access_token(self) -> None:
        logger.info("renew access token")


_trainer_store = None


def trainer_store_factory(config: TrainerConfig, scheduler: Scheduler) -> TrainerStore:
    # TODO: refactor
    global _trainer_store
    if _trainer_store is None:
        _trainer_store = TrainerStore(config, scheduler)
    return _trainer_store
