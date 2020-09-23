# coding=utf-8
# Androxus bot
# Botinfo.py

__author__ = 'Rafael'

from datetime import datetime
from discord.ext import commands
import discord
from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.utils.Utils import random_color, pegar_o_prefixo, get_last_update
from stopwatch import Stopwatch
import psutil
from os import getpid
from sys import version
from discord_bot.dao.InformacoesDao import InformacoesDao
from dateutil.relativedelta import relativedelta  # módulo que vai ser usado para subtrair datetime


class Botinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_info', 'help_detalhes'])
    async def help_botinfo(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.botinfo.name,
                          descricao=self.botinfo.description,
                          exemplos=['``{pref}botinfo``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.botinfo.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['info', 'detalhes'], description='Mostra algumas informações sobre mim!')
    async def botinfo(self, ctx):
        async with ctx.channel.typing():  # vai aparecer "bot está digitando"
            stopwatch_banco = Stopwatch()
            prefixo = pegar_o_prefixo(None, ctx)
            stopwatch_banco.stop()
            embed = discord.Embed(title=f'<:Info:756712227221930102> Detalhes sobre mim!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Caso você queira saber meus outros comandos, use ``{prefixo}help``!',
                                  timestamp=datetime.utcnow())
            embed.set_author(name='Androxus',
                             icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f'{ctx.author}',
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name=':calendar: Data que fui criado:',
                            value=f'``{self.bot.user.created_at.strftime("%d/%m/%Y")}``',
                            inline=True)
            # years months days hours minutes seconds
            idade = relativedelta(datetime.utcnow(), self.bot.user.created_at)
            days = idade.days
            months = idade.months
            years = idade.years
            meses_formatado = ''
            dias_formatados = ''
            if days > 1:
                dias_formatados = f'e {days} dias!'
            elif days == 1:
                dias_formatados = f'e {days} dia!'
            if months > 1:
                meses_formatado = f', {months} meses '
            elif months == 1:
                meses_formatado = f', {months} mês '
            embed.add_field(name=':older_adult: Idade:',
                            value=f'``{years} anos{meses_formatado}{dias_formatados}``',
                            inline=True)
            embed.add_field(name=':robot: Meu perfil:',
                            value=f'``{str(self.bot.user)}``',
                            inline=True)
            embed.add_field(name=':id: Meu id:',
                            value=f'``{self.bot.user.id}``',
                            inline=True)
            embed.add_field(name='<:WumpusCrown:756712226978660392> Meu dono:',
                            value=f'``{self.bot.get_user(self.bot.owner_id)}``',
                            inline=True)
            embed.add_field(name='<a:pato:755774683348992060> Quantos servidores estão me usando:',
                            value=f'``{len(self.bot.guilds)}``',
                            inline=True)
            embed.add_field(name='<a:parrot_dancando:755774679670718575> Quantas pessoas têm acesso a mim:',
                            # observer, que aqui, estamos pegando a lista de membros e jogando para um set
                            # pois, o "set" não permite que haja itens duplicados, ou seja, fazendo desta forma
                            # cada item vai ser único
                            value=f'``{str(len(set(self.bot.get_all_members())))}``',
                            inline=True)
            embed.add_field(name=':ping_pong: Latência da API:',
                            value=f'``{int(self.bot.latency * 1000)}ms``',
                            inline=True)
            embed.add_field(name='<:DatabaseCheck:756712226303508530> Tempo para se conectar ao banco:',
                            value=f'``{stopwatch_banco}``',
                            inline=True)
            this_process = psutil.Process(getpid())
            embed.add_field(name='<a:loading:756715436149702806> Uso da CPU:',
                            value=f'``{this_process.cpu_percent():.2f}%``',
                            inline=True)
            embed.add_field(name=':frog: Memória RAM:',
                            value=f'``{(this_process.memory_info().rss / (1e+6)):.2f}Mb' +
                                  '/512Mb``',
                            inline=True)
            embed.add_field(name='<:WumpusPizza:756712226710356122> Versão do discord.py:',
                            value=f'``{discord.__version__}``',
                            inline=True)
            embed.add_field(name='<:python:756712226210971660> Versão do python:',
                            value=f'``{version[0:5]}``',
                            inline=True)
            embed.add_field(name=':bank: Banco de dados que estou usando:',
                            value=f'``{InformacoesDao().get_version()[:15]}``',
                            inline=True)
            uptime = datetime.utcnow() - self.bot.uptime
            hours_bot, remainder_bot = divmod(int(uptime.total_seconds()), 3600)
            minutes_bot, seconds_bot = divmod(remainder_bot, 60)
            days_bot, hours_bot = divmod(hours_bot, 24)
            embed.add_field(name=':stopwatch: Estou online há:',
                            value=f'``{days_bot} d, {hours_bot} h, {minutes_bot} m, {seconds_bot} s``',
                            inline=True)
            atualizado_ha = datetime.utcnow() - get_last_update()
            hours_att, remainder_att = divmod(int(atualizado_ha.total_seconds()), 3600)
            minutes_att, seconds_att = divmod(remainder_att, 60)
            days_att, hours_att = divmod(hours_att, 24)
            embed.add_field(name=':watch: Ultima atualização há:',
                            value=f'``{days_att} d, {hours_att} h, {minutes_att} m, {seconds_att} s``',
                            inline=True)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Botinfo(bot))
