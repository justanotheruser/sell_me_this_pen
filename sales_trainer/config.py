import os
from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings
from yaml import safe_load

from sales_trainer.trainer.config import TrainerConfig


class CorsConfig(BaseSettings):
    allow_origins: list[str]


class HostingConfig(BaseSettings):
    # Domain and port visible from the Internet
    domain: str
    port: int
    cors: CorsConfig


class Config(BaseSettings):
    testing: bool
    hosting: HostingConfig
    trainer: TrainerConfig


def load_config(path: Path | None = None) -> Config:
    if not path:
        path = Path(os.path.dirname(os.path.abspath(__file__))) / '..' / 'cfg' / 'cfg.yaml'
    return Config(**load_yaml(path))


def load_yaml(path: Path) -> dict[str, Any]:
    with open(path, 'r') as f:
        config = safe_load(f)
    if not isinstance(config, dict):
        raise TypeError(f"Config file has no top-level mapping: {path}")
    return config


config = load_config()
