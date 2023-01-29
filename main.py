import discord, json, os, asyncio, logging, logging.handlers, aiohttp
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self, config: dict, *args, **kwargs):
        self.config = config
        super().__init__(command_prefix="!", intents=discord.Intents.all())


        @self.event
        async def on_ready(self):
                print("Bot is ready")
        
    async def setup_hook(self) -> None:
            try:
                await self.load_extension("pterodactyl")
            except Exception as e:
                print(f"Error loading extension: {e}")
                raise e



async def main():
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)

        handler = logging.handlers.RotatingFileHandler(
                filename='discord.log',
                encoding='utf-8',
                maxBytes=32 * 1024 * 1024,  # 32 MiB
                backupCount=5,  # Rotate through 5 files
        )
        formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', '%Y-%m-%d %H:%M:%S', style='{')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        template_config = {
                "token": "token",
                "prefix": "prefix",
                "uri": "uri",
                "api_panel": "apipanel",
                "api_user": "apiuser",
                "white_roles": ["iduser","iduser"]
        }

        def create_config() -> None:
                with open("config.json", "w") as f:
                        json.dump(template_config, f, indent=4)

        def check_config(config: dict) -> bool:
                for key, value in template_config.items():
                        if key not in config:
                                return False
                        if config[key] == value:
                                return False
                return True

        if not os.path.exists("config.json"):
                create_config()
                print("Please fill out the config.json file")
                return
        elif not check_config(config := json.load(open("config.json"))):
                print("Please fill out the config.json file correctly")
                return
        else:
                config = json.load(open("config.json"))
                async with aiohttp.ClientSession() as session:
                        async with Bot(config=config) as bot:
                                await bot.start(config["token"])

if __name__ == "__main__":
        print("Starting bot...")
        asyncio.run(main())