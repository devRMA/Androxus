# coding=utf-8
# Androxus bot
# Help.py

__author__ = 'Rafael'

from discord.ext import commands
import discord
from datetime import datetime
from discord.Utils import random_color, pegar_o_prefixo, get_emoji_dance
from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao
from discord.dao.ComandoPersonalizadoDao import ComandoPersonalizadoDao
from discord.modelos.EmbedHelp import embedHelp


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ajuda'], description='Mostra a mensagem de ajuda')
    async def help(self, ctx, *comando):
        if len(comando) == 0:
            cor = random_color()
            embed = embedHelp(self.bot,
                              ctx,
                              comando='help',
                              descricao=self.help.description,
                              parametros=['[comando]'],
                              exemplos=['``{pref}help``', '``{pref}ajuda`` ``adicionar_comando``'],
                              # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                              aliases=self.help.aliases.copy(),
                              cor=cor)
            lista_de_comando = discord.Embed(title=f"Lista de comandos:", colour=discord.Colour(cor),
                                             description="Estes são os comandos que eu tenho (todos abaixo precisam do prefixo)",
                                             timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            lista_de_comando.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            lista_de_comando.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            if ctx.guild is not None:
                comandos_desativados = ComandoDesativadoDao().get_comandos(ctx.guild.id)
            else:
                comandos_desativados = []
            for cog in self.bot.cogs:  # adiciona os comandos padrões no embed
                for command in self.bot.get_cog(cog).get_commands():
                    if (not command.hidden):  # se o comando não estiver privado
                        emoji = '<a:ativado:755774682334101615>'
                        for c in comandos_desativados:
                            if command.name in c:
                                emoji = '<a:desativado:755774682397147226>'
                        if not (ctx.guild is None):  # se a mensagem foi enviar num server
                            lista_de_comando.add_field(name=f'{emoji}``{command.name}``',
                                                       value=str(command.description),
                                                       inline=True)
                        else:  # se foi enviada no dm, vai enviar todos os comandos
                            lista_de_comando.add_field(name=f'{emoji}``{command.name}``',
                                                       value=str(command.description),
                                                       inline=True)
            if ctx.guild is not None:  # comandos personalizados
                comandos_personalizados = ComandoPersonalizadoDao().get_comandos(ctx.guild.id)
                if len(comandos_personalizados) != 0:
                    lista_de_comando.add_field(name='**Comandos personalizados:**',
                                               value='Estes sãos os comandos personalizados deste servidor. **Não precisam do prefixo**',
                                               inline=False)
                    for comando_personalizado in comandos_personalizados:
                        if comando_personalizado[0] is not None:
                            emoji = '<a:ativado:755774682334101615>'
                            for c in comandos_desativados:
                                if comando_personalizado[0] in c:
                                    emoji = '<a:desativado:755774682397147226>'
                            resposta = ComandoPersonalizadoDao().get_resposta(ctx.guild.id, comando_personalizado[0])
                            if resposta[-1]:  # se o inText estiver on:
                                lista_de_comando.add_field(
                                    name=f'{emoji}``{comando_personalizado[0]}``',
                                    value=f'Eu irei responder "{resposta[0]}"', inline=True)
                            else:
                                lista_de_comando.add_field(
                                    name=f'{emoji}``{comando_personalizado[0]}``',
                                    value=f'Eu irei responder "{resposta[0]}" **apenas se a mensagem iniciar com o comando**',
                                    inline=True)
            await ctx.send(embed=embed)
            await ctx.send(embed=lista_de_comando)
        else:
            comando = ' '.join(comando)
            for cog in self.bot.cogs:  # Abre todos os cogs que o bot têm
                for command in self.bot.get_cog(cog).get_commands():  # pega todos os comandos do cog
                    if (str(command) == f'help_{comando.lower()}') or (
                            f'help_{comando.lower()}' in command.aliases):  # se o comando for help_comando
                        await command(ctx)  # chama ele xD
                        return
            cor = random_color()
            embed = discord.Embed(title='Comando não encontrado <a:sad:755774681008832623>', colour=discord.Colour(cor),
                                  description=f'Desculpe, mas não achei a ajuda para o comando ``{comando}``',
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.set_author(name="Androxus", icon_url=f'{self.bot.user.avatar_url}')
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.add_field(name='**Possiveis soluções:**',
                            value='```ini\n[•] Veja se você não digitou algo errado\n[•] A ajuda só funciona para' +
                                  ' comandos padrões, ou seja, comandos personalizados não têm ajuda.```',
                            inline=False)
            await ctx.send(content=ctx.author.mention, embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
