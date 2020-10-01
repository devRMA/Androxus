# coding=utf-8
# Androxus bot
# Ping.py

__author__ = 'Rafael'

from discord.ext import commands

from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.utils.Utils import pegar_o_prefixo


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_latency', 'help_latência'])
    async def help_ping(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.ping.name,
                          descricao=self.ping.description,
                          exemplos=['``{pref}ping``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.ping.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['latency', 'latência'], description='Mostra a minha latência atual.')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ping(self, ctx):
        from stopwatch import Stopwatch
        mensagem_do_bot = await ctx.send(f'Minha latência atual é de {int(self.bot.latency * 1000)}ms !')
        stopwatch_banco = Stopwatch()
        pegar_o_prefixo(None, ctx)  # abre uma conexão, faz um select no banco, e fecha
        stopwatch_banco.stop()
        await mensagem_do_bot.edit(content=f'Latência da API do discord: {int(self.bot.latency * 1000)}ms!\n' +
                                           f'Latência com o banco de dados: {str(stopwatch_banco)}!\n<a:hello:755774680949850173>')


def setup(bot):
    bot.add_cog(Ping(bot))
