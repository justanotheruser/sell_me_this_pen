from pydantic import AnyHttpUrl, SecretStr
from pydantic_settings import BaseSettings


class TrainerConfig(BaseSettings):
    gigachat_auth_url: AnyHttpUrl
    gigachat_auth_key: SecretStr
    prompt: SecretStr


class TrainerConfigWithAuth(TrainerConfig):
    access_token: SecretStr | None = None
