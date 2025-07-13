import os
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from sales_trainer.trainer.config import TrainerConfig


class CorsConfig(BaseSettings):
    allow_origins: list[str]


class HostingConfig(BaseSettings):
    # Domain and port visible from the Internet
    domain: str
    port: int
    cors: CorsConfig


config_dir = Path(os.path.dirname(os.path.abspath(__file__))) / '..' / 'cfg'


class Config(BaseSettings):
    testing: bool = False
    hosting: HostingConfig
    trainer: TrainerConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Порядок, в котором используются значения (более поздние перезаписывают более ранние):
        - значения по-умолчанию
        - yaml-файл
        - .env-файл
        - переменные окружения
        """
        return (
            env_settings,
            DotEnvSettingsSource(
                settings_cls, env_file=config_dir / '.env', env_file_encoding='utf-8'
            ),
            YamlConfigSettingsSource(
                settings_cls, yaml_file=config_dir / 'cfg.yaml', yaml_file_encoding='utf-8'
            ),
            init_settings,
        )

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        case_sensitive=False,
    )


config = Config()  # type: ignore[call-arg]
