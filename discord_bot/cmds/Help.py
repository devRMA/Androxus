# coding=utf-8
# Androxus bot
# Help.py

__author__ = 'Rafael'

from datetime import datetime

import discord
from discord.ext import commands
from discord_bot.database.Repositories.ComandoDesativadoRepository import ComandoDesativadoRepository
from discord_bot.database.Repositories.ComandoPersonalizadoRepository import ComandoPersonalizadoRepository
from discord_bot.database.Conexao import Conexao
from discord_bot.database.Servidor import Servidor

from discord_bot.modelos.EmbedHelp import embedHelp
from discord_bot.utils.Utils import random_color


class Help(commands.Cog):
    # TODO
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_ajuda'])
    async def help_help(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.help.name,
                          descricao=self.help.description,
                          parametros=['[comando]'],
                          exemplos=['``{pref}help``', '``{pref}ajuda`` ``adicionar_comando``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.help.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['ajuda'], description='Mostra a mensagem de ajuda de um comando.')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def help(self, ctx, *comando):
        if len(comando) == 0:
            conexao = Conexao()
            async with ctx.channel.typing():  # vai aparecer "bot está digitando"
                if ctx.guild:
                    servidor = Servidor(ctx.guild.id, ctx.prefix)
                cor = random_color()
                embed = embedHelp(self.bot,
                                  ctx,
                                  comando=self.help.name,
                                  descricao=self.help.description,
                                  parametros=['[comando]'],
                                  exemplos=['``{pref}help``', '``{pref}ajuda`` ``adicionar_comando``'],
                                  # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                                  aliases=self.help.aliases.copy(),
                                  cor=cor)
                lista_de_comando = discord.Embed(title=f'Lista de comandos:',
                                                 colour=discord.Colour(cor),
                                                 description='Estes são os comandos que eu tenho (todos abaixo ' +
                                                             f'precisam do prefixo ``{ctx.prefix}``)',
                                                 timestamp=datetime.utcnow())
                lista_de_comando.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
                lista_de_comando.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                if servidor:
                    comandos_desativados = ComandoDesativadoRepository().get_commands(conexao, servidor)
                else:
                    comandos_desativados = []
                for cog in self.bot.cogs:  # adiciona os comandos padrões no embed
                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:  # se o comando não estiver privado
                            emoji = '<a:ativado:755774682334101615>'
                            if comandos_desativados:
                                for comando_desativado in comandos_desativados:
                                    if command.name.lower() in comando_desativado.comando.lower():
                                        emoji = '<a:desativado:755774682397147226>'
                                for aliases in command.aliases:  # também verifica os "sinônimos"
                                    if aliases.lower() in comando_desativado.comando.lower():
                                        emoji = '<a:desativado:755774682397147226>'
                            lista_de_comando.add_field(name=f'{emoji}``{command.name}``',
                                                       value=str(command.description),
                                                       inline=True)
                if servidor:  # adiciona os comandos personalizados na lista
                    comandos_personalizados = ComandoPersonalizadoRepository().get_commands(conexao, servidor)
                    if len(comandos_personalizados) != 0:
                        lista_de_comando.add_field(name='**Comandos personalizados:**',
                                                   value='Estes sãos os comandos personalizados deste servidor.' +
                                                         ' **Não precisam do prefixo**',
                                                   inline=False)
                        for comando_personalizado in comandos_personalizados:
                            emoji_personalizado = '<a:check:755775267275931799>'
                            for comando_desativado in comandos_desativados:
                                if comando_personalizado.comando.lower() in comando_desativado.comando.lower():
                                    emoji_personalizado = '<a:desativado:755774682397147226>'
                            if comando_personalizado.inText:  # se o inText estiver on:
                                lista_de_comando.add_field(
                                    name=f'{emoji_personalizado}``{comando_personalizado.comando}``',
                                    value=f'Eu irei responder **independente da posição do comando na mensagem**.',
                                    inline=True)
                            else:
                                lista_de_comando.add_field(
                                    name=f'{emoji_personalizado}``{comando_personalizado.comando}``',
                                    value=f'Eu irei responder **apenas se a mensagem iniciar com o comando**',
                                    inline=True)
            await ctx.send(embed=embed)
            await ctx.send(embed=lista_de_comando)
            conexao.fechar()
        else:
            async with ctx.channel.typing():  # vai aparecer "bot está digitando"
                comando = ' '.join(comando)
                for cog in self.bot.cogs:  # Abre todos os cogs que o bot têm
                    for command in self.bot.get_cog(cog).get_commands():  # pega todos os comandos do cog
                        if (str(command) == f'help_{comando.lower()}') or (
                                f'help_{comando.lower()}' in command.aliases):  # se o comando for help_comando
                            await command(ctx)  # chama ele xD
                            return
                cor = random_color()
                embed = discord.Embed(title='Comando não encontrado <a:sad:755774681008832623>',
                                      colour=discord.Colour(cor),
                                      description=f'Desculpe, mas não achei a ajuda para o comando ``{comando}``',
                                      timestamp=datetime.utcnow())
                embed.set_author(name='Androxus', icon_url=f'{self.bot.user.avatar_url}')
                embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                embed.add_field(name='**Possiveis soluções:**',
                                value='```ini\n[•] Veja se você não digitou algo errado\n[•] A ajuda só funciona para' +
                                      ' comandos padrões, ou seja, comandos personalizados não têm ajuda.```',
                                inline=False)
            await ctx.send(content=ctx.author.mention, embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
