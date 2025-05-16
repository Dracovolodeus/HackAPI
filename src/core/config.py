from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    url: str = f"https://45.143.203.44:10000/{host}:{port}"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    user: str = "/user"
    hackathon: str = "/hackathon"
    team: str = "/team"
    jury: str = "/jury"
    admin: str = "/admin"

    create: str = "/create"
    get: str = "/get"
    update: str = "/update"
    delete: str = "/delete"
    login: str = "/login"
    add: str = "/add"
    remove: str = "/remove"
    invite: str = "/invite"
    update_access_token: str = "/update_access_token"


class RoleId(BaseModel):
    user: int = 1
    resp_pers: int = 2
    root: int = 3


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    token_type_field: str = "type"
    access_token_type: str = "access"
    refresh_token_type: str = "refresh"
    access_token_expire_seconds: int = 864000
    refresh_token_expire_seconds: int = 2592000


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    auth_jwt: AuthJWT = AuthJWT()
    role: RoleId = RoleId()


settings = Settings()
