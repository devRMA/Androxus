# coding=utf-8
# Androxus bot
# Help.py

__author__ = 'Rafael'

import asyncio
from datetime import datetime

import currency_exchange
import discord
from discord.ext import commands
from googletrans import Translator

from discord_bot.Classes import Androxus
from discord_bot.database.Conexao import Conexao
from discord_bot.database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from discord_bot.database.Repositories.ServidorRepository import ServidorRepository
from discord_bot.modelos.embedHelpCategory import embedHelpCategory
from discord_bot.modelos.embedHelpCommand import embedHelpCommand
from discord_bot.utils.Utils import random_color, get_most_similar_item, string_similarity, convert_to_string


class Help(commands.Cog, command_attrs=dict(category='bot_info')):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help',
                      aliases=['ajuda'],
                      description='Mostra mais detalhes sobre um comando.\n**Para obter os meus comandos, '
                                  'digite "cmds"**!',
                      parameters=['[comando/categoria]'],
                      examples=['``{prefix}help``',
                                '``{prefix}ajuda`` ``adicionar_comando``'],
                      cls=Androxus.Command)
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
                    conexao = Conexao()
                    servidor = ServidorRepository().get_servidor(conexao, ctx.guild.id)
                    comandos_personalizados = ComandoPersonalizadoRepository().get_commands(conexao, servidor)
                    conexao.fechar()
                    for cmd_pers in comandos_personalizados:
                        if cmd_pers.comando == comando:
                            e = discord.Embed(title='<a:loop_fun:763809373046702110> Comando personalizado',
                                              colour=discord.Colour(random_color()),
                                              description=f'**Este comando só existe neste servidor!**',
                                              timestamp=datetime.utcnow())
                            e.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
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
                    embed = discord.Embed(title='Comando não encontrado <a:sad:755774681008832623>',
                                          colour=discord.Colour(random_color()),
                                          description=f'Desculpe, mas não achei a ajuda para o comando ``{comando}``',
                                          timestamp=datetime.utcnow())
                    embed.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
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
                e = embedHelpCategory(self.bot, ctx, comando)
            # se não passou pelo return , vai atribuir o comando ao ctx.command
            ctx.command = command
            # o help do comando money é diferente, por isso esta condição
            if (ctx.command is not None) and (ctx.command.name == 'money'):
                embed1 = embedHelpCommand(self.bot, ctx)
                embed1.add_field(name=f'Para saber todas as abreviações das moedas que eu aceito, clique em ➕',
                                 value=f'** **',
                                 inline=True)
                embed2 = discord.Embed(title=f'Todas as moedas que eu aceito no comando "money"',
                                       colour=discord.Colour(random_color()),
                                       description='** **',
                                       timestamp=datetime.utcnow())
                translator = Translator()
                moedas = ''
                for c in currency_exchange.currencies():
                    moedas += f'{c}\n'
                moedas = translator.translate(moedas, dest='pt').text
                for c in moedas.splitlines():
                    abreviacao, moeda = c.split(' - ')
                    embed2.add_field(name=f'**{abreviacao}**',
                                     value=f'{moeda}',
                                     inline=True)

                async def menu_help(ctx, msg):
                    # fica verificando a pagina 1, para ver se é para ir para a pagina 2
                    def check_page1(reaction, user):
                        return (user.id == ctx.author.id) and (str(reaction.emoji) == '➡')

                    # fica verificando a pagina 2, para ver se é para ir para a pagina 1
                    def check_page2(reaction, user):
                        return (user.id == ctx.author.id) and (str(reaction.emoji) == '⬅')

                    async def check_reactions_without_perm(ctx, msg, bot):
                        # mudas as páginas, se o bot não tiver perm pra apagar reações
                        while True:
                            await bot.wait_for('reaction_add', timeout=900.0, check=check_page1)
                            await msg.delete()
                            msg = await ctx.send(embed=embed2)
                            await msg.add_reaction('⬅')
                            await bot.wait_for('reaction_add', timeout=900.0, check=check_page2)
                            await msg.delete()
                            msg = await ctx.send(embed=embed1)
                            await msg.add_reaction('➡')

                    async def check_reactions_with_perm(msg, bot):
                        # mudas as páginas, se o bot tiver perm pra apagar reações
                        while True:
                            await bot.wait_for('reaction_add', timeout=900.0, check=check_page1)
                            await msg.clear_reactions()
                            await msg.add_reaction('⬅')
                            await msg.edit(embed=embed2)
                            await bot.wait_for('reaction_add', timeout=900.0, check=check_page2)
                            await msg.clear_reactions()
                            await msg.add_reaction('➡')
                            await msg.edit(embed=embed1)

                    # se foi usado num servidor:
                    if ctx.guild:
                        # se o bot tiver perm pra usar o "clear_reactions"
                        if ctx.guild.me.guild_permissions.manage_messages:
                            await check_reactions_with_perm(msg, self.bot)
                        else:  # se o bot não tiver permissão:
                            await check_reactions_without_perm(ctx, msg, self.bot)
                    else:  # se não for usado no servidor:
                        await check_reactions_without_perm(ctx, msg, self.bot)

                msg_bot = await ctx.send(embed=embed1)
                await msg_bot.add_reaction('➡')
                try:
                    # vai fica 1 minuto e meio esperando o usuário apertas nas reações
                    await asyncio.wait_for(menu_help(ctx, msg_bot), timeout=90.0)
                except asyncio.TimeoutError:  # se acabar o tempo
                    pass
                return
        if e is None:
            e = embedHelpCommand(self.bot, ctx)
        return await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Help(bot))
