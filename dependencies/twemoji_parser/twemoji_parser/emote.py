import emoji
from aiohttp import ClientSession


async def valid_src(url: str, session: ClientSession):
    async with session.head(url) as resp:
        status = resp.status
    return status == 200


async def emoji_to_url(char, include_check: bool = True, session: ClientSession = None):
    try:
        url = f"https://twemoji.maxcdn.com/v/latest/72x72/{ord(char[0]):x}.png"
        if not include_check:
            return url

        _session = session or ClientSession()
        is_valid = await valid_src(url, _session)
        if not session:
            await _session.close()
        return url if is_valid else char
    except TypeError:
        return char
