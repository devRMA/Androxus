# coding=utf-8
# Androxus bot
# Botinfo.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord.modelos.EmbedHelp import embedHelp
from discord.Utils import random_color, pegar_o_prefixo
from stopwatch import Stopwatch
import psutil
from sys import version


class Botinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_info', 'help_detalhes'])
    async def help_botinfo(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando='desativar_comando',
                          descricao=self.botinfo.description,
                          exemplos=['``{pref}botinfo``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.botinfo.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['info', 'detalhes'], description='Mostra algumas informações sobre mim!')
    async def botinfo(self, ctx):
        stopwatch_banco = Stopwatch()
        prefixo = pegar_o_prefixo(None, ctx)
        stopwatch_banco.stop()
        embed = discord.Embed(title=f'<:Info:756712227221930102> Detalhes sobre mim!',
                              colour=discord.Colour(random_color()),
                              description=f'Caso você queira saber meus outros comandos, use ``{prefixo}help``!',
                              timestamp=datetime.utcnow())
        embed.set_author(name='Androxus', icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        embed.add_field(name=':calendar: Criado em:', value=f'``{self.bot.user.created_at.strftime("%d/%m/%Y")}``', inline=True)
        embed.add_field(name=':robot: Meu perfil:', value=f'``{str(self.bot.user)}``', inline=True)
        embed.add_field(name=':id: Meu id:', value=f'``{self.bot.user.id}``', inline=True)
        embed.add_field(name='<:WumpusCrown:756712226978660392> Meu dono:', value=f'``{self.bot.get_user(self.bot.owner_id)}``', inline=True)
        embed.add_field(name='<a:pato:755774683348992060> Quantos servidores estão me usando:',
                        value=f'``{len(self.bot.guilds)}``',
                        inline=True)
        embed.add_field(name=':ping_pong: Latência da API:',
                        value=f'``{int(self.bot.latency * 1000)}ms``',
                        inline=True)
        embed.add_field(name='<:DatabaseCheck:756712226303508530> Tempo para se conectar ao banco:',
                        value=f'``{stopwatch_banco}``',
                        inline=True)
        embed.add_field(name='<a:loading:756715436149702806> Uso da CPU:',
                        value=f'``{psutil.cpu_percent()}%``',
                        inline=True)
        embed.add_field(name=':frog: Quantidade de RAM disponível:',
                        value=f'``{(psutil.virtual_memory().total / (1e+9)):.2f}Gbs``',
                        inline=True)
        embed.add_field(name='<:WumpusPizza:756712226710356122> Versão da API do discord:',
                        value=f'``{discord.__version__}``',
                        inline=True)
        embed.add_field(name='<:python:756712226210971660> Versão do python:',
                        value=f'``{version[0:5]}``',
                        inline=True)
        embed.add_field(name=':bank: Banco de dados que estou usando:',
                        value=f'``Postgresql``',
                        inline=True)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Botinfo(bot))
