from os import getenv

from colorama import init
from discord.ext import commands
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database.bootstrap import bootstrap as db_bootstrap
from database.repositories.guild_repository import GuildRepository

init()
load_dotenv()
bot = commands.Bot(command_prefix='!!')


@bot.event
async def on_ready():
    user = getenv('DB_USER')
    pw = getenv('DB_PASS')
    host = getenv('DB_HOST')
    port = getenv('DB_PORT')
    db_name = getenv('DB_NAME')
    dsn = f'postgresql+asyncpg://{user}:{pw}@{host}:{port}/{db_name}'
    engine = create_async_engine(
        dsn
    )
    await db_bootstrap(engine)
    async_session = sessionmaker(
        engine,
        autocommit=False,
        expire_on_commit=False,
        class_=AsyncSession
    )
    repository = GuildRepository(async_session)
    guild = await repository.create(1)
    if guild is None:
        print('Guild already exists')
    else:
        print(f'guild.id: {guild.id}')
        await repository.delete(guild)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(getenv('TOKEN'))
