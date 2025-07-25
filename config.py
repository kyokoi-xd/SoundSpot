import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', '')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '')
    SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', '')
    JAMENDO_CLIENT_ID = os.getenv('JAMENDO_CLIENT_ID', '')

    @classmethod
    def validate(cls) -> None:
        missing = [
            k for k, v in cls.__dict__.items()
            if not k.startswith('_') and isinstance(v, str) and not v
        ]
        if missing:
            raise RuntimeError(
                f'Missing environment variables: {", ".join(missing)}'
            )
        
config = Config()
config.validate()