from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AliasChoices

class Settings(BaseSettings):
    environment: str = Field(
        default="development",
        validation_alias=AliasChoices("MCP_ENV", "mcp_env"),
    )
    enable_git_connector: bool = Field(
        default=True,
        validation_alias=AliasChoices("MCP_ENABLE_GIT", "mcp_enable_git"),
    )
    enable_database_connector: bool = Field(
        default=False,
        validation_alias=AliasChoices("MCP_ENABLE_DB", "mcp_enable_db"),
    )
    git_root: str = Field(
        default="/tmp/repos",
        validation_alias=AliasChoices("MCP_GIT_ROOT", "mcp_git_root"),
    )
    database_url: str = Field(
        default="sqlite:///./mcp.db",
        validation_alias=AliasChoices("MCP_DATABASE_URL", "mcp_database_url"),
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
