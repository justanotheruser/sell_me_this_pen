import logging
from uuid import uuid4

import requests
from apscheduler import Scheduler
from apscheduler.triggers.interval import IntervalTrigger
from pydantic import SecretStr

from sales_trainer.trainer.config import TrainerConfig, TrainerConfigWithAuth
from sales_trainer.trainer.trainer import GigachatTrainer

logger = logging.getLogger(__name__)


class TrainerStore:
    def __init__(self, config: TrainerConfig, scheduler: Scheduler):
        self.store: dict[str, GigachatTrainer] = {}
        self.cfg = TrainerConfigWithAuth(**config.model_dump())
        self.cfg.access_token = self.__renew_access_token()
        self.scheduler = scheduler
        self.renew_task_id = self.scheduler.add_schedule(
            self.__renew_access_token, trigger=IntervalTrigger(minutes=29)
        )

    def add(self, sid: str) -> GigachatTrainer:
        trainer = GigachatTrainer(self.cfg)
        self.store[sid] = trainer
        return trainer

    def get(self, sid: str) -> GigachatTrainer | None:
        return self.store.get(sid, None)

    def remove(self, sid: str) -> None:
        if sid in self.store:
            del self.store[sid]
        else:
            logger.warning(f"No trainer for sid {sid}")

    def __renew_access_token(self) -> SecretStr | None:
        logger.info("renew access token")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid4()),
            "Authorization": f"Basic {self.cfg.gigachat_auth_key.get_secret_value()}",
        }
        data = {"scope": "GIGACHAT_API_PERS"}
        # TODO: использовать сертификат МинЦифры вместо verify=False
        try:
            response = requests.post(
                str(self.cfg.gigachat_auth_url),
                headers=headers,
                data=data,
                timeout=60,
                verify=False,  # nosec
            )
            response.raise_for_status()
            json_response = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request: {e}")
            return None
        access_token = SecretStr(json_response['access_token'])
        self.access_token = access_token
        return access_token


_trainer_store = None


def trainer_store_factory(config: TrainerConfig, scheduler: Scheduler) -> TrainerStore:
    # TODO: refactor
    global _trainer_store
    if _trainer_store is None:
        _trainer_store = TrainerStore(config, scheduler)
    return _trainer_store
