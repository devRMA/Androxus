# -*- coding: utf-8 -*-
# Androxus bot
# Botinfo.py

__author__ = 'Rafael'

import asyncio
from datetime import datetime
from os import getpid
from sys import version

import discord
import psutil
from discord.ext import commands
from stopwatch import Stopwatch

from Classes import Androxus
from database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.InformacoesRepository import InformacoesRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils.Utils import get_last_commit, capitalize, pegar_o_prefixo, prettify_number
from utils.Utils import get_last_update, datetime_format
from utils.Utils import random_color


class Botinfo(commands.Cog, command_attrs=dict(category='bot_info')):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.Androxus.Androxus): Instância do bot

        """
        self.bot = bot

    @Androxus.comando(name='botinfo',
                      aliases=['info', 'detalhes', 'bi'],
                      description='Mostra algumas informações sobre mim!',
                      examples=['``{prefix}botinfo``'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _botinfo(self, ctx):
        stopwatch_banco = Stopwatch()
        sql_version = await InformacoesRepository().get_sql_version(self.bot.db_connection)
        stopwatch_banco.stop()
        # se a pessoa usou o comando, mencionando o bot:
        if ctx.prefix.replace("!", "").replace(" ", "") == self.bot.user.mention:
            # vai pegar o prefixo que está no banco
            prefixo = await pegar_o_prefixo(self.bot, ctx)
        else:
            # se a pessoa não marcou o bot:
            prefixo = ctx.prefix
        embed = discord.Embed(title=f'{self.bot.emoji("info")} Detalhes sobre mim!',
                              colour=discord.Colour(random_color()),
                              description=f'Caso você queira saber meus outros comandos, use ``{prefixo}cmds``!',
                              timestamp=datetime.utcnow())
        embed.set_author(name=self.bot.user.name,
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
        embed.add_field(name=f'{self.bot.emoji("owner")} Meu dono:',
                        value=f'``{self.bot.get_user(self.bot.owner_id)}``',
                        inline=True)
        embed.add_field(name=f'{self.bot.emoji("pato")} Quantos servidores estão me usando:',
                        value=f'``{prettify_number(len(self.bot.guilds))}``',
                        inline=True)
        embed.add_field(name=f'{self.bot.emoji("parrot")} Quantas pessoas têm acesso a mim:',
                        # observer, que aqui, estamos pegando a lista de membros e jogando para um set
                        # pois, o "set" não permite que haja itens duplicados, ou seja, fazendo desta forma
                        # cada item vai ser único
                        value=f'``{prettify_number(len(set(self.bot.get_all_members())))}``',
                        inline=True)
        embed.add_field(name=':ping_pong: Latência da API:',
                        value=f'``{prettify_number(int(self.bot.latency * 1000))}ms``',
                        inline=True)
        embed.add_field(name=f'{self.bot.emoji("database")} Latência com o banco de dados:',
                        value=f'``{stopwatch_banco}``',
                        inline=True)
        this_process = psutil.Process(getpid())
        embed.add_field(name=f'{self.bot.emoji("loading")} Uso da CPU:',
                        value=f'``{prettify_number(psutil.cpu_percent())}%``',
                        inline=True)
        embed.add_field(name=':frog: Memória RAM:',
                        value=f'``{(this_process.memory_info().rss / (1e+6)):.2f}Mb' +
                              '/512Mb``',
                        inline=True)
        embed.add_field(name=f'{self.bot.emoji("pizza")} Versão do discord.py:',
                        value=f'``{discord.__version__}``',
                        inline=True)
        embed.add_field(name=f'{self.bot.emoji("python")} Versão do python:',
                        value=f'``{version[0:5]}``',
                        inline=True)
        embed.add_field(name=':bank: Banco de dados que estou usando:',
                        value=f'``{sql_version[:15]}``',
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

    @Androxus.comando(name='source',
                      aliases=['github', 'programação', 's'],
                      description='Mostra o meu código fonte!',
                      examples=['``{prefix}source``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _source(self, ctx):
        embed = discord.Embed(title=f'{self.bot.emoji("python")} Olá {ctx.author.name}, eu sou um bot feito em ' +
                                    'python, com a API do discord e um banco de dados!',
                              colour=discord.Colour(random_color()),
                              description='Caso você queira ver o meu código fonte, clique [aqui]' +
                                          '(https://github.com/devRMA/Androxus)\n' +
                                          'Caso você queira ver a documentação da API do discord ' +
                                          'para python, clique [aqui](https://discordpy.readthedo' +
                                          'cs.io/en/latest/index.html).',
                              timestamp=datetime.utcnow())
        embed.set_author(name=self.bot.user.name, icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @Androxus.comando(name='ping',
                      aliases=['latency', 'latência', 'p'],
                      description='Mostra a minha latência atual.',
                      examples=['``{prefix}ping``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _ping(self, ctx):
        stopwatch_banco = Stopwatch()
        async with self.bot.db_connection.acquire() as conn:
            await conn.fetch('select version();')
        stopwatch_banco.stop()
        e1 = discord.Embed(title=f'Calculando ping {self.bot.emoji("loading")}',
                           colour=discord.Colour(random_color()),
                           description='** **',
                           timestamp=datetime.utcnow())
        e1.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        stopwatch_message = Stopwatch()
        mensagem_do_bot = await ctx.send(embed=e1)
        stopwatch_message.stop()
        e2 = discord.Embed(title=f'🏓 Latência da API: {prettify_number(int(self.bot.latency * 1000))}ms!\n'
                                 f'{self.bot.emoji("database")} Tempo de resposta do banco: {stopwatch_banco}!\n'
                                 f'{self.bot.emoji("bob")} Tempo de resposta no discord: {stopwatch_message}!',
                           colour=discord.Colour(random_color()),
                           description='** **',
                           timestamp=datetime.utcnow())
        e2.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await asyncio.sleep(stopwatch_message.duration * 2)
        await mensagem_do_bot.edit(embed=e2)

    @Androxus.comando(name='invite',
                      aliases=['convidar', 'convite', 'i'],
                      description='Mostra o link que você usa para me adicionar em seu servidor',
                      examples=['``{prefix}invite``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _invite(self, ctx):
        e = discord.Embed(title=f'Invite',
                          colour=discord.Colour(random_color()),
                          description=f'Clique [aqui](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}'
                                      '&scope=bot&permissions=604892375) para me adicionar em outro servidor!'
                                      f'{self.bot.emoji("love")}',
                          timestamp=datetime.utcnow())
        e.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
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
                      aliases=['tempo_on', 'ut', 'u'],
                      description='Mostra a quanto tempo eu estou online!',
                      examples=['``{prefix}uptime``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _uptime(self, ctx):
        embed = discord.Embed(title=f':timer: Quando eu liguei:',
                              description=f'``{datetime_format(self.bot.uptime)}``',
                              colour=discord.Colour(random_color()),
                              timestamp=datetime.utcnow())
        embed.set_author(name=self.bot.user.name, icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @Androxus.comando(name='cmds',
                      aliases=['comandos', 'listar_comandos', 'list_cmds'],
                      description='A lista com todos os comandos que eu tenho!',
                      examples=['``{prefix}cmds``', '``{prefix}comandos``'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _cmds(self, ctx):
        e = discord.Embed(title='Todos os meus comandos',
                          colour=discord.Colour(random_color()),
                          description=f'Caso você queira saber mais informações sobre um comando, '
                                      'digite \'help comando\'',
                          timestamp=datetime.utcnow())
        e.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        e.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        categories = self.bot.get_all_categories()
        servidor = None
        if ctx.guild:
            servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
            comandos_desativados = [c.comando for c in
                                    await ComandoDesativadoRepository().get_commands(self.bot.db_connection, servidor)]
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
            cmds_personalizados = await ComandoPersonalizadoRepository().get_commands(self.bot.db_connection, servidor)
            commands = []
            if len(cmds_personalizados) >= 1:
                for comando_personalizado in cmds_personalizados:
                    commands.append(f'``{comando_personalizado.comando}``')
                commands.sort()
                e.add_field(name=f'{self.bot.get_emoji_from_category("personalizado")} Comandos personalizados (são '
                                 'comandos exclusivos deste servidor e não precisam do prefixo)'
                                 f'({len(commands)})',
                            value=f'{", ".join(commands)}.',
                            inline=False)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Botinfo(bot))
