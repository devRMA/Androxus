# coding=utf-8
# Androxus bot
# Botinfo.py

__author__ = 'Rafael'

from datetime import datetime
from os import getpid
from sys import version

import discord
import psutil
from discord.ext import commands
from stopwatch import Stopwatch

from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.InformacoesRepository import InformacoesRepository
from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.utils.Utils import get_last_commit
from discord_bot.utils.Utils import get_last_update, datetime_format
from discord_bot.utils.Utils import random_color


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
        await ctx.send(embed=embed)

    @commands.command(aliases=['info', 'detalhes'], description='Mostra algumas informações sobre mim!')
    async def botinfo(self, ctx):
        async with ctx.typing():  # vai aparecer "bot está digitando"
            stopwatch_banco = Stopwatch()
            conexao = Conexao()
            stopwatch_banco.stop()
            embed = discord.Embed(title=f'<:Info:756712227221930102> Detalhes sobre mim!',
                                  colour=discord.Colour(random_color()),
                                  description=f'Caso você queira saber meus outros comandos, use ``{ctx.prefix}help``!',
                                  timestamp=datetime.utcnow())
            embed.set_author(name='Androxus',
                             icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f'{ctx.author}',
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name=':calendar: Data que fui criado:',
                            value=f'``{self.bot.user.created_at.strftime("%d/%m/%Y")}``',
                            inline=True)
            embed.add_field(name=':older_adult: Idade:',
                            value=f'``{datetime_format(self.bot.user.created_at)}``',
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
                            value=f'``{InformacoesRepository().get_sql_version(conexao)[:15]}``',
                            inline=True)
            comandos = 0
            for cog in self.bot.cogs:  # adiciona os comandos padrões no embed
                for command in self.bot.get_cog(cog).get_commands():
                    if not command.hidden:  # se o comando não estiver privado
                        comandos += 1
            embed.add_field(name=':desktop: Quantos comandos eu tenho:',
                            value=f'``{comandos}``')
            embed.add_field(name=':stopwatch: Quando eu liguei:',
                            value=f'``{datetime_format(self.bot.uptime)}``',
                            inline=True)
            embed.add_field(name=':watch: Última atualização que tive foi:',
                            value=f'``{datetime_format(get_last_update())}``',
                            inline=True)
        await ctx.send(embed=embed)
        conexao.fechar()

    @commands.command(hidden=True, aliases=['help_github', 'help_programação'])
    async def help_source(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.source.name,
                          descricao=self.source.description,
                          exemplos=['``{pref}source``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.source.aliases.copy())
        await ctx.send(embed=embed)

    @commands.command(aliases=['github', 'programação'], description='Mostra o meu código fonte!')
    async def source(self, ctx):
        embed = discord.Embed(title=f'Olá {ctx.author.name}, eu sou um bot feito em python, com ' +
                                    'a API do discord e um banco de dados!',
                              colour=discord.Colour(random_color()),
                              description='Caso você queira ver o meu código fonte, clique [aqui]' +
                                          '(https://github.com/devRMA/Androxus/tree/master/discord_bot)\n' +
                                          'Caso você queira ver a documentação da API do discord ' +
                                          'para python, clique [aqui](https://discordpy.readthedo' +
                                          'cs.io/en/latest/index.html).',
                              timestamp=datetime.utcnow())
        embed.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @commands.command(hidden=True, aliases=['help_latency', 'help_latência'])
    async def help_ping(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.ping.name,
                          descricao=self.ping.description,
                          exemplos=['``{pref}ping``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.ping.aliases.copy())
        await ctx.send(embed=embed)

    @commands.command(aliases=['latency', 'latência'], description='Mostra a minha latência atual.')
    async def ping(self, ctx):
        from stopwatch import Stopwatch
        mensagem_do_bot = await ctx.send(f'Minha latência atual é de {int(self.bot.latency * 1000)}ms !')
        stopwatch_banco = Stopwatch()
        conexao = Conexao()
        stopwatch_banco.stop()
        conexao.fechar()
        await mensagem_do_bot.edit(content=f'Latência da API do discord: {int(self.bot.latency * 1000)}ms!\n' +
                                           f'Latência com o banco de dados: {str(stopwatch_banco)}!\n<a:hello:755774680949850173>')

    @commands.command(hidden=True, aliases=['help_convidar', 'help_convite'])
    async def help_invite(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.invite.name,
                          descricao=self.invite.description,
                          exemplos=['``{pref}invite``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.invite.aliases.copy())
        await ctx.send(embed=embed)

    @commands.command(aliases=['convidar', 'convite'],
                      description='Mostra o link que você usa para me adicionar em seu servidor')
    async def invite(self, ctx):
        await ctx.send(
            f'https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=604892375')

    @commands.command(hidden=True, aliases=['help_ultima_att', 'help_última_att', 'help_att_log'])
    async def help_changelog(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.changelog.name,
                          descricao='Mostra quando foi a minha última atualização e ainda mostra o que foi alterado.',
                          exemplos=['``{pref}changelog``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.changelog.aliases.copy())
        await ctx.send(embed=embed)

    @commands.command(aliases=['ultima_att', 'última_att', 'att_log'],
                      description='Mostra qual foi a última atualização que eu tive!')
    async def changelog(self, ctx):
        async with ctx.channel.typing():  # vai aparecer "bot está digitando"
            embed = discord.Embed(title=f'Ultima atualização que eu tive:',
                                  colour=discord.Colour(random_color()),
                                  description=f'```{get_last_commit()}```',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}',
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name='Atualização feita em:',
                            value=f'{datetime_format(get_last_update())}',
                            inline=True)
        await ctx.send(embed=embed)

    @commands.command(hidden=True, aliases=['help_tempo_on'])
    async def help_uptime(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.uptime.name,
                          descricao=self.uptime.description,
                          exemplos=['``{pref}uptime``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.uptime.aliases.copy())
        await ctx.send(embed=embed)

    @commands.command(aliases=['tempo_on'], description='Mostra a quanto tempo eu estou online!')
    async def uptime(self, ctx):
        embed = discord.Embed(title=f':timer: Quando eu liguei:',
                              description=f'``{datetime_format(self.bot.uptime)}``',
                              colour=discord.Colour(random_color()),
                              timestamp=datetime.utcnow())
        embed.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Botinfo(bot))
