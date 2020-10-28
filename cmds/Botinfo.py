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

from Classes import Androxus
from database.Conexao import Conexao
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.InformacoesRepository import InformacoesRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils.Utils import get_last_commit, capitalize, pegar_o_prefixo, prettify_number
from utils.Utils import get_last_update, datetime_format
from utils.Utils import random_color


class Botinfo(commands.Cog, command_attrs=dict(category='bot_info')):
    def __init__(self, bot):
        self.bot = bot

    @Androxus.comando(name='botinfo',
                      aliases=['info', 'detalhes'],
                      description='Mostra algumas informações sobre mim!',
                      examples=['``{prefix}botinfo``'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _botinfo(self, ctx):
        stopwatch_banco = Stopwatch()
        conexao = Conexao()
        stopwatch_banco.stop()
        # se a pessoa usou o comando, mencionando o bot:
        if ctx.prefix.replace("!", "").replace(" ", "") == self.bot.user.mention:
            # vai pegar o prefixo que está no banco
            prefixo = pegar_o_prefixo(self.bot, ctx, False, conexao)
        else:
            # se a pessoa não marcou o bot:
            prefixo = ctx.prefix
        embed = discord.Embed(title=f'{self.bot.configs["emojis"]["info"]} Detalhes sobre mim!',
                              colour=discord.Colour(random_color()),
                              description=f'Caso você queira saber meus outros comandos, use ``{prefixo}cmds``!',
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
        embed.add_field(name=f'{self.bot.configs["emojis"]["owner"]} Meu dono:',
                        value=f'``{self.bot.get_user(self.bot.owner_id)}``',
                        inline=True)
        embed.add_field(name=f'{self.bot.configs["emojis"]["dances"]["pato"]} Quantos servidores estão me usando:',
                        value=f'``{prettify_number(len(self.bot.guilds))}``',
                        inline=True)
        embed.add_field(name=f'{self.bot.configs["emojis"]["dances"]["parrot"]} Quantas pessoas têm acesso a mim:',
                        # observer, que aqui, estamos pegando a lista de membros e jogando para um set
                        # pois, o "set" não permite que haja itens duplicados, ou seja, fazendo desta forma
                        # cada item vai ser único
                        value=f'``{prettify_number(len(set(self.bot.get_all_members())))}``',
                        inline=True)
        embed.add_field(name=':ping_pong: Latência da API:',
                        value=f'``{prettify_number(int(self.bot.latency * 1000))}ms``',
                        inline=True)
        embed.add_field(name=f'{self.bot.configs["emojis"]["database"]} Tempo para se conectar ao banco:',
                        value=f'``{stopwatch_banco}``',
                        inline=True)
        this_process = psutil.Process(getpid())
        embed.add_field(name=f'{self.bot.configs["emojis"]["loading"]} Uso da CPU:',
                        value=f'``{this_process.cpu_percent():.2f}%``',
                        inline=True)
        embed.add_field(name=':frog: Memória RAM:',
                        value=f'``{(this_process.memory_info().rss / (1e+6)):.2f}Mb' +
                              '/512Mb``',
                        inline=True)
        embed.add_field(name=f'{self.bot.configs["emojis"]["pizza"]} Versão do discord.py:',
                        value=f'``{discord.__version__}``',
                        inline=True)
        embed.add_field(name=f'{self.bot.configs["emojis"]["python"]} Versão do python:',
                        value=f'``{version[0:5]}``',
                        inline=True)
        embed.add_field(name=':bank: Banco de dados que estou usando:',
                        value=f'``{InformacoesRepository().get_sql_version(conexao)[:15]}``',
                        inline=True)
        embed.add_field(name=':desktop: Quantos comandos eu tenho:',
                        value=f'``{prettify_number(len(self.bot.get_all_commands()))}``')
        embed.add_field(name=':stopwatch: Quando eu liguei:',
                        value=f'``{datetime_format(self.bot.uptime)}``',
                        inline=True)
        embed.add_field(name=':watch: Última atualização que tive foi:',
                        value=f'``{datetime_format(get_last_update())}``',
                        inline=True)
        await ctx.send(embed=embed)
        conexao.fechar()

    @Androxus.comando(name='source',
                      aliases=['github', 'programação'],
                      description='Mostra o meu código fonte!',
                      examples=['``{prefix}source``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _source(self, ctx):
        embed = discord.Embed(title=f'Olá {ctx.author.name}, eu sou um bot feito em python, com ' +
                                    'a API do discord e um banco de dados!',
                              colour=discord.Colour(random_color()),
                              description='Caso você queira ver o meu código fonte, clique [aqui]' +
                                          '(https://github.com/devRMA/Androxus)\n' +
                                          'Caso você queira ver a documentação da API do discord ' +
                                          'para python, clique [aqui](https://discordpy.readthedo' +
                                          'cs.io/en/latest/index.html).',
                              timestamp=datetime.utcnow())
        embed.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @Androxus.comando(name='ping',
                      aliases=['latency', 'latência'],
                      description='Mostra a minha latência atual.',
                      examples=['``{prefix}ping``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _ping(self, ctx):
        from stopwatch import Stopwatch
        stopwatch_banco = Stopwatch()
        conexao = Conexao()
        stopwatch_banco.stop()
        conexao.fechar()
        stopwatch_message = Stopwatch()
        mensagem_do_bot = await ctx.send(f'Calculando ping...')
        stopwatch_message.stop()
        await mensagem_do_bot.edit(
            content=f'Latência da API do discord: {prettify_number(int(self.bot.latency * 1000))}ms!\n'
                    f'Tempo para se conectar ao banco de dados: {str(stopwatch_banco)}!\n'
                    f'Tempo para enviar uma mensagem: {str(stopwatch_message)}!\n'
                    f'{self.bot.configs["emojis"]["hello"]}')

    @Androxus.comando(name='invite',
                      aliases=['convidar', 'convite'],
                      description='Mostra o link que você usa para me adicionar em seu servidor',
                      examples=['``{prefix}invite``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _invite(self, ctx):
        e = discord.Embed(title=f'Invite',
                          colour=discord.Colour(random_color()),
                          description=f'Clique [aqui](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}'
                                      '&scope=bot&permissions=604892375) para me adicionar em outro servidor!'
                                      f'{self.bot.configs["emojis"]["love"]}',
                          timestamp=datetime.utcnow())
        await ctx.send(embed=e)

    @Androxus.comando(name='changelog',
                      aliases=['ultima_att', 'última_att', 'att_log'],
                      description='Mostra quando foi a minha última atualização e ainda mostra o que foi alterado.',
                      examples=['``{prefix}changelog``'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _changelog(self, ctx):
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

    @Androxus.comando(name='uptime',
                      aliases=['tempo_on'],
                      description='Mostra a quanto tempo eu estou online!',
                      examples=['``{prefix}uptime``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _uptime(self, ctx):
        embed = discord.Embed(title=f':timer: Quando eu liguei:',
                              description=f'``{datetime_format(self.bot.uptime)}``',
                              colour=discord.Colour(random_color()),
                              timestamp=datetime.utcnow())
        embed.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @Androxus.comando(name='cmds',
                      aliases=['comandos', 'listar_comandos', 'list_cmds'],
                      description='A lista com todos os comandos que eu tenho!',
                      examples=['``{prefix}cmds``', '``{prefix}comandos``'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _cmds(self, ctx):
        conexao = Conexao()
        e = discord.Embed(title='Todos os meus comandos',
                          colour=discord.Colour(random_color()),
                          description=f'Caso você queira saber mais informações sobre um comando, '
                                      'digite \'help comando\'',
                          timestamp=datetime.utcnow())
        e.set_author(name='Androxus', icon_url=self.bot.user.avatar_url)
        e.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        categories = self.bot.get_all_categories()
        servidor = None
        if ctx.guild:
            servidor = ServidorRepository().get_servidor(conexao, ctx.guild.id)
            comandos_desativados = [c.comando for c in ComandoDesativadoRepository().get_commands(conexao, servidor)]
        for category in categories:
            commands = self.bot.get_commands_from_category(category)
            if len(commands) != 0:
                for i in range(len(commands)):
                    commands[i] = f'``{commands[i]}``'
                if servidor:
                    # vai remover todos os comandos desativados, da lista que vai aparecer na mensagem
                    for cmds_off in comandos_desativados:
                        if cmds_off in commands:
                            try:
                                commands = commands.remove(cmds_off)
                            except:
                                pass
                e.add_field(
                    name=f'{self.bot.get_emoji_from_category(category)} {capitalize(category)} ({len(commands)})',
                    value=f'{", ".join(commands)}.',
                    inline=False)
        if servidor:
            cmds_personalizados = ComandoPersonalizadoRepository().get_commands(conexao, servidor)
            commands = []
            if len(cmds_personalizados) >= 1:
                for comando_personalizado in cmds_personalizados:
                    commands.append(f'``{comando_personalizado.comando}``')
                commands.sort()
                e.add_field(name=f'{self.bot.get_emoji_from_category("personalizado")} Comandos personalizados (são '
                                 'comandos exclusivos deste servidor, e não precisam do prefixo)'
                                 f'({len(commands)})',
                            value=f'{", ".join(commands)}.',
                            inline=False)
        conexao.fechar()
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Botinfo(bot))
