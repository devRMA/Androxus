# coding=utf-8
# Androxus bot
# Clear.py

#imports
import discord
from discord.ext import commands
from datetime import datetime

#class
class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.aliases = ['limpar', 'clear']
        self.prefixo = '..'

    #limpar
    @commands.guild_only()
    @commands.command(aliases = self.aliases)
    async def clean(self, ctx, *, quantia = None):
        embed = discord.Embed(title='WolfZ - Ajuda - Clean', url='https://wolfz-bot.glitch.me', description='', color=0x0000ff, timestamp=datetime.utcfromtimestamp(datetime.now().timestamp())))
        embed.set_author(name='===By yWolfBR#1330===')
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/755521679337455729/755521704800813246/WolfZ.png')
        embed.add_field(name=':duvida: **Como usar?**', value='**`--clean + Quantidade`**', inline=False)
        for c in range(0, self.aliases):
            self.aliases[c] = f'{self.prefixo}{self.aliases[c]}'
        embed.add_field(name=':igual: **Sinônimos**', value=', '.join(self.aliases), inline=False)
        embed.set_footer(text='https://wolfz-bot.glitch.me')
        if quantia is None:
            await ctx.send(embed=embed)
            return
        try:
            quantia = int(quantia)  # aqui vai verificar se a pessoa passou um número inteiro
            # se não deu erro, pode continuar
            if quantia <= 300: # um limite, para que a pessoa não consiga pagara 99999 mensagens
                await ctx.channel.purge(limit=quantia+1)
        except ValueError:
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Clear(client))
