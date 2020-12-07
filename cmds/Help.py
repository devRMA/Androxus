# -*- coding: utf-8 -*-
# Androxus bot
# Help.py

__author__ = 'Rafael'

import asyncio
from datetime import datetime

import currency_exchange
import discord
from discord.ext import commands

from Classes import Androxus
from database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from database.Repositories.ServidorRepository import ServidorRepository
from EmbedModels.embedHelpCategory import embed_help_category
from EmbedModels.embedHelpCommand import embed_help_command
from utils.Utils import random_color, get_most_similar_item, string_similarity, convert_to_string


class Help(commands.Cog, command_attrs=dict(category='bot_info')):
    def __init__(self, bot):
        """

        Args:
            bot (Classes.Androxus.Androxus): Instância do bot

        """
        self.bot = bot

    @Androxus.comando(name='help',
                      aliases=['ajuda', 'h'],
                      description='Mostra mais detalhes sobre um comando.\nPara obter os meus comandos, '
                                  'digite "cmds"!',
                      parameters=['[comando/categoria]'],
                      examples=['``{prefix}help``',
                                '``{prefix}ajuda`` ``adicionar_comando``'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def _help(self, ctx, *, comando=None):
        e = None
        # se o comando foi chamado pela pessoa assim: "help ..." e se a pessoa passou alguma coisa
        # se o comando for None, vai mostrar a ajuda do comando "help" ou qualquer outro que vier no ctx
        if (ctx.command.name == 'help') and (comando is not None):
            # vai verificar se o que a pessoa passou não foi uma categoria
            command = None
            if not self.bot.is_category(comando):
                command = self.bot.get_command(comando)
                comandos_personalizados = []
                # se não achar um comando, vai procurar nos comandos personalizados
                if (command is None) and (ctx.guild is not None):
                    servidor = await ServidorRepository().get_servidor(self.bot.db_connection, ctx.guild.id)
                    comandos_personalizados = await ComandoPersonalizadoRepository().get_commands(
                        self.bot.db_connection, servidor)
                    for cmd_pers in comandos_personalizados:
                        if cmd_pers.comando == comando:
                            e = discord.Embed(title=f'{self.bot.emoji("loop_fun")} Comando personalizado',
                                              colour=discord.Colour(random_color()),
                                              description=f'**Este comando só existe neste servidor!**',
                                              timestamp=datetime.utcnow())
                            e.set_author(name=self.bot.user.name, icon_url=f'{self.bot.user.avatar_url}')
                            e.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
                            e.add_field(name=f'Comando: ```{cmd_pers.comando}```\n'
                                             f'Resposta: ```{cmd_pers.resposta}```\n'
                                             f'Ignorar posição: ```{convert_to_string(cmd_pers.in_text)}```',
                                        value='** **',
                                        inline=False)
                            return await ctx.send(embed=e)
                # se achou um comando "escondido"
                if (command is not None) and command.hidden:
                    command = None
                # se o bot não achar o comando com esse nome
                if command is None:
                    embed = discord.Embed(title=f'Comando não encontrado {self.bot.emoji("sad")}',
                                          colour=discord.Colour(0xFF0000),
                                          description=f'Desculpe, mas não achei a ajuda para o comando ``{comando}``',
                                          timestamp=datetime.utcnow())
                    embed.set_author(name=self.bot.user.name, icon_url=f'{self.bot.user.avatar_url}')
                    embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                    msg = '```ini\n[•] Veja se você não digitou algo errado'
                    all_commands = []
                    for command in self.bot.get_all_commands():
                        all_commands.append(command.name)
                        all_commands.append(command.category)
                        for alias in command.aliases:
                            all_commands.append(alias)
                    comando = ctx.message.content.lower()[len(ctx.prefix):].split(' ')
                    if comando[0] == 'help':
                        comando.pop(0)
                    comando = comando[0]
                    if ctx.guild:
                        all_commands = all_commands + [c.comando for c in comandos_personalizados]
                    sugestao = get_most_similar_item(comando, all_commands)
                    # se a sugestão for pelo menos 50% semelhante ao comando
                    if (sugestao is not None) and (string_similarity(comando, sugestao) >= 0.5):
                        msg += f'\n[•] Você quis dizer "{sugestao}"?'
                    embed.add_field(name='**Possiveis soluções:**',
                                    value=f'{msg}```',
                                    inline=False)
                    return await ctx.send(embed=embed)
            else:
                # se a pessoa usou o comando "help diversão" vai mostrar todos os comandos
                # que estão nessa categoria
                e = await embed_help_category(self.bot, ctx, comando)
            # se não passou pelo return , vai atribuir o comando ao ctx.command
            ctx.command = command
        if e is None:
            e = await embed_help_command(self.bot, ctx)
        return await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Help(bot))
