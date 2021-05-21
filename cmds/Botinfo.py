# -*- coding: utf-8 -*-
# Androxus bot
# Botinfo.py

__author__ = 'Rafael'

import asyncio
from datetime import datetime
from os import getpid
from sys import version

import DiscordUtils
import discord
import psutil
from discord.ext import commands
from stopwatch import Stopwatch

from Classes import Androxus
from EmbedModels.embedHelpCategory import embed_help_category
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.InformacoesRepository import InformacoesRepository
from database.Repositories.ServidorRepository import ServidorRepository
from utils.Utils import get_last_commit, pegar_o_prefixo, prettify_number
from utils.Utils import get_last_update, datetime_format


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
                              colour=discord.Colour.random(),
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
        await ctx.reply(embed=embed, mention_author=False)

    @Androxus.comando(name='source',
                      aliases=['github', 'programação', 's'],
                      description='Mostra o meu código fonte!',
                      examples=['``{prefix}source``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _source(self, ctx):
        embed = discord.Embed(title=f'{self.bot.emoji("python")} Olá {ctx.author.display_name}, eu sou um bot feito em '
                                    'python, com a API do discord e um banco de dados!',
                              colour=discord.Colour.random(),
                              description='Caso você queira ver o meu código fonte, clique [aqui]'
                                          '(https://github.com/devRMA/Androxus)\n'
                                          'Caso você queira ver a documentação da API do discord '
                                          'para python, clique [aqui](https://discordpy.readthedo'
                                          'cs.io/en/latest/index.html).',
                              timestamp=datetime.utcnow())
        embed.set_author(name=self.bot.user.name, icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.reply(embed=embed, mention_author=False)

    @Androxus.comando(name='ping',
                      aliases=['latency', 'latência', 'p'],
                      description='Mostra a minha latência atual.',
                      examples=['``{prefix}ping``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _ping(self, ctx):
        messages = await self.bot.translate(ctx, values_={
            'loading': self.bot.emoji('loading'),
            'database': self.bot.emoji('database'),
            'api_ping': '',
            'db_ping': '',
            'dc_ping': ''
        })
        stopwatch_banco = Stopwatch()
        async with self.bot.db_connection.acquire() as conn:
            await conn.fetch('select version();')
        stopwatch_banco.stop()
        stopwatch_message = Stopwatch()
        mensagem_do_bot = await ctx.send(**messages[0])
        stopwatch_message.stop()
        messages = await self.bot.translate(ctx, values_={
            'loading': self.bot.emoji('loading'),
            'database': self.bot.emoji('database'),
            'api_ping': prettify_number(int(self.bot.latency * 1000)),
            'db_ping': str(stopwatch_banco),
            'dc_ping': str(stopwatch_message)
        })
        await asyncio.sleep(stopwatch_message.duration * 2)
        await mensagem_do_bot.edit(**messages[1])

    @Androxus.comando(name='invite',
                      aliases=['convidar', 'convite', 'i'],
                      description='Mostra o link que você usa para me adicionar em seu servidor',
                      examples=['``{prefix}invite``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _invite(self, ctx):
        e = discord.Embed(title=f'Invite',
                          colour=discord.Colour.random(),
                          description=f'Clique [aqui](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}'
                                      '&scope=bot&permissions=604892375) para me adicionar em outro servidor!'
                                      f'{self.bot.emoji("love")}',
                          timestamp=datetime.utcnow())
        e.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.reply(embed=e, mention_author=False)

    @Androxus.comando(name='changelog',
                      aliases=['ultima_att', 'última_att', 'att_log'],
                      description='Mostra quando foi a minha última atualização e ainda mostra o que foi alterado.',
                      examples=['``{prefix}changelog``'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _changelog(self, ctx):
        embed = discord.Embed(title=f'Ultima atualização que eu tive:',
                              colour=discord.Colour.random(),
                              description=f'```{get_last_commit()}```',
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.author}',
                         icon_url=ctx.author.avatar_url)
        embed.add_field(name='Atualização feita há:',
                        value=f'{datetime_format(get_last_update())}',
                        inline=True)
        await ctx.reply(embed=embed, mention_author=False)

    @Androxus.comando(name='uptime',
                      aliases=['tempo_on', 'ut', 'u'],
                      description='Mostra a quanto tempo eu estou online!',
                      examples=['``{prefix}uptime``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _uptime(self, ctx):
        embed = discord.Embed(title=f':timer: Quando eu liguei:',
                              description=f'``{datetime_format(self.bot.uptime)}``',
                              colour=discord.Colour.random(),
                              timestamp=datetime.utcnow())
        embed.set_author(name=self.bot.user.name, icon_url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.reply(embed=embed, mention_author=False)

    @Androxus.comando(name='cmds',
                      aliases=['comandos', 'listar_comandos', 'list_cmds'],
                      description='A lista com todos os comandos que eu tenho!',
                      examples=['``{prefix}cmds``', '``{prefix}comandos``'])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _cmds(self, ctx):
        categories = [c for c in self.bot.get_all_categories() if len(self.bot.get_commands_from_category(c)) > 0]
        paginas = len(categories) + 1
        servidor = None
        cmds_personalizados = None
        if ctx.guild:
            servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
            cmds_personalizados = await ComandoPersonalizadoRepository().get_commands(self.bot.db_connection,
                                                                                      servidor)
            if len(cmds_personalizados) >= 1:
                paginas += 1
                categories.append('personalizado')
        cor = 0x6AffED
        embeds = []
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx=ctx,
                                                                 timeout=60,
                                                                 auto_footer=False,
                                                                 remove_reactions=ctx.channel.permissions_for(
                                                                     ctx.me).manage_messages)
        embed_home = discord.Embed(title='Todos os meus comandos',
                                   colour=discord.Colour(cor),
                                   description=f'Atualmente eu tenho `{len(self.bot.get_all_commands())}` comandos, e '
                                               'caso você queira saber mais informações '
                                               'sobre um comando, digite \'help comando\'.',
                                   timestamp=datetime.utcnow())
        embed_home.add_field(name='Categorias',
                             value='\n'.join(f'{self.bot.get_emoji_from_category(categories[c])} ── '
                                             f'{categories[c].capitalize()}' for c in range(paginas - 1)),
                             inline=True)
        for c in range(paginas - 1):
            emoji = self.bot.get_emoji(categories[c])
            paginator.add_reaction(emoji, f'page {c + 1}')
        embed_home.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed_home.set_footer(text=f'{ctx.author} ─ 1/{paginas}', icon_url=ctx.author.avatar_url)
        embeds.append(embed_home)
        for category in categories:
            if category.lower() != 'personalizado':
                e = await embed_help_category(self.bot, ctx, category, cor)
                e.set_footer(text=f'{ctx.author} ─ {categories.index(category) + 2}/{paginas}',
                             icon_url=ctx.author.avatar_url)
                embeds.append(e)
        if servidor:
            comandos_str = []
            if len(cmds_personalizados) >= 1:
                for comando_personalizado in cmds_personalizados:
                    comandos_str.append(f'``{comando_personalizado.comando}``')
                comandos_str.sort()
                e = discord.Embed(title=f'{self.bot.get_emoji_from_category("personalizado")} Comandos personalizados',
                                  colour=discord.Colour(cor),
                                  description='São comandos exclusivos deste servidor. Não precisam do prefixo.',
                                  timestamp=datetime.utcnow())
                e.add_field(name=f'📖 Comandos ({len(comandos_str)}):',
                            value=', '.join(comandos_str),
                            inline=False)
                e.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                e.set_footer(text=f'{ctx.author} ─ {paginas}/{paginas}',
                             icon_url=ctx.author.avatar_url)
                embeds.append(e)
        embed_paginator_help = discord.Embed(title='Ajuda com as páginas',
                                             description='Enquanto um comando estiver com os emojis para você navegar '
                                                         'entre as páginas, você não pode usar o comando de novo!',
                                             colour=discord.Colour(cor),
                                             timestamp=datetime.utcnow())
        embed_paginator_help.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed_paginator_help.set_footer(text=f'{ctx.author} ─ Página de ajuda',
                                        icon_url=ctx.author.avatar_url)
        emoji_stop = self.bot.get_emoji('stop')
        emoji_arrow_red = self.bot.get_emoji('red_arrow_left')
        embed_paginator_help.add_field(name='Aqui está a legenda do que cada emoji faz.',
                                       value=f'{emoji_arrow_red} ─ Para voltar ao início.\n'
                                             f'{emoji_stop} ─ Para a execução do comando (a execução para '
                                             f'automaticamente em 60 segundos).\n'
                                             ':grey_question: ─ Vem para está página de ajuda.',
                                       inline=True)
        embeds.append(embed_paginator_help)
        paginator.add_reaction(emoji_arrow_red, 'page 0')
        paginator.add_reaction(emoji_stop, 'lock')
        paginator.add_reaction('❔', f'page {len(embeds)}')
        msg = await paginator.run(embeds)
        for reaction in msg.reactions:
            if reaction.me:
                await reaction.remove(ctx.me)


def setup(bot):
    bot.add_cog(Botinfo(bot))
