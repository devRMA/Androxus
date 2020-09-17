# coding=utf-8
# Androxus bot
# Ping.py

__author__ = 'Rafael'

from discord.ext import commands
import discord
from discord.Utils import pegar_o_prefixo, random_color
from datetime import datetime



class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_latency', 'help_latência'])
    async def help_ping(self, ctx):
        prefixo = pegar_o_prefixo(None, ctx)
        embed = discord.Embed(title=f"``{prefixo}ping``", colour=discord.Colour(random_color()),
                              description="Mostra a minha latência atual!",
                              timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
        embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="**Como usar?**",
                        value=f"``{prefixo}ping``",
                        inline=False)
        embed.add_field(name="Exemplo:",
                        value=f"``{prefixo}ping``",
                        inline=False)
        embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                        value=f"``{prefixo}latency``, ``{prefixo}latência``", inline=False)
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['latency', 'latência'], description='Mostra a minha latência atual.')
    async def ping(self, ctx):
        from stopwatch import Stopwatch
        mensagem_do_bot = await ctx.send(f'Minha latência atual é de {int(self.bot.latency * 1000)}ms !')
        stopwatch_banco = Stopwatch()
        pegar_o_prefixo(None, ctx) # abre uma conexão, faz um select no banco, e fecha
        stopwatch_banco.stop()
        await mensagem_do_bot.edit(content=f'Latência da API do discord: {int(self.bot.latency * 1000)}ms!\n' +
                                           f'Latência com o banco de dados: {str(stopwatch_banco)}!\n<a:hello:755774680949850173>')


def setup(bot):
    bot.add_cog(Ping(bot))
