from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Juris-Cape Backend"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    SWARM_SECRET: str = "change-me-in-prod-secure-swarm-key"
    STORAGE_TYPE: str = "local" # or 'supabase'

settings = Settings()