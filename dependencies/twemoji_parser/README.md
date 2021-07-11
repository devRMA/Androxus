# twemoji_parser
A python module made on top of PIL that draws twemoji from text to image.<br>
```sh
$ python3 -m pip install twemoji-parser
```

## Examples
### Basic example
```py
from twemoji_parser import TwemojiParser
from PIL import Image, ImageFont

async def main():
    im = Image.new("RGB", (500, 500), color=(255, 255, 255))
    font = ImageFont.truetype("/path/to/font.ttf", 30)
    parser = TwemojiParser(im)
    
    await parser.draw_text((5, 5), "I 💖 Python!", font=font, fill=(0, 0, 0))
    await parser.close()
    im.show()
```

### Basic example with Discord custom emoji
```py
from twemoji_parser import TwemojiParser
from PIL import Image, ImageFont

async def main():
    im = Image.new("RGB", (500, 500), color=(255, 255, 255))
    font = ImageFont.truetype("/path/to/font.ttf", 30)
    parser = TwemojiParser(im, parse_discord_emoji=True)
    
    await parser.draw_text((5, 5), "I 💖 Python! <:love_emoji:772448930448670723>", font=font, fill=(0, 0, 0))
    await parser.close()
    im.show()
```

### Get a twemoji URL from emoji:
```py
from twemoji_parser import emoji_to_url

async def main():
    url = await emoji_to_url("❤️")
    print(url)
```
