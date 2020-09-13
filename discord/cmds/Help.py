# coding=utf-8
# Androxus bot
# Help.py

__author__ = 'Rafael'

from discord.ext import commands
import discord
from datetime import datetime
from discord.Utils import random_color, pegar_o_prefixo
from discord.dao.ComandoDesativadoDao import ComandoDesativadoDao
from discord.dao.ComandoPersonalizadoDao import ComandoPersonalizadoDao


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ajuda'], description='Mostra a mensagem de ajuda')
    async def help(self, ctx, comando = None):
        if comando is None:
            cor = random_color()
            prefixo = pegar_o_prefixo(None, ctx)
            embed = discord.Embed(title=f"``{prefixo}help``", colour=discord.Colour(cor),
                                  description="Mostra essa mensagem de ajuda!",
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            embed.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            embed.add_field(name="**Como usar?**",
                            value=f"``{prefixo}help`` ``[comando_completo]``",
                            inline=False)
            embed.add_field(
                name="Tudo que estiver entre **<>** são obrigatorio, e tudo que estiver entre **[]** são opcionais.",
                value="<a:jotarodance:754702437901664338>", inline=False)
            embed.add_field(name="Exemplos:",
                            value=f"``{prefixo}help``\n(Vai mostrar essa mensagem)",
                            inline=False)
            embed.add_field(name="Outro exemplo:",
                            value=f"``{prefixo}help`` ``adicionar_comando``\n(Vai mostrar a mensagem de ajuda, do comando \"adicionar_comando\")",
                            inline=False)
            embed.add_field(name=":twisted_rightwards_arrows: Sinônimos:",
                            value=f"``{prefixo}ajuda``", inline=False)
            lista_de_comando = discord.Embed(title=f"Lista de comandos:", colour=discord.Colour(cor),
                                  description="Estes são os comandos que eu tenho (todos abaixo precisam do prefixo)",
                                  timestamp=datetime.utcfromtimestamp(datetime.now().timestamp()))
            lista_de_comando.set_author(name="Androxus", icon_url=f"{self.bot.user.avatar_url}")
            lista_de_comando.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            for cog in self.bot.cogs:  # adiciona os comandos padrões no embed
                for command in self.bot.get_cog(cog).get_commands():
                    if (not command.hidden):  # se o comando não estiver privado
                        emoji = '<:desativado:754819961376997407>'
                        print(ComandoDesativadoDao().get_comandos(ctx.guild.id))
                        if not (ctx.guild is None):  # se a mensagem foi enviar num server
                            if not (command.name in ComandoDesativadoDao().get_comandos(ctx.guild.id)):  # verifica se o comando está ativo
                                lista_de_comando.add_field(name=f'<a:check:754719579648950342>``{command.name}``',
                                                           value=str(command.description),
                                                           inline=True)
                        else:  # se foi enviada no dm, vai enviar todos os comandos
                            lista_de_comando.add_field(name=f'<a:check:754719579648950342>``{command.name}``',
                                                       value=str(command.description),
                                                       inline=True)
            if not (ctx.guild is None):  # comandos personalizados
                comandos_personalizados = ComandoPersonalizadoDao().get_comandos(ctx.guild.id)
                if len(comandos_personalizados) != 0:
                    lista_de_comando.add_field(name='**Comandos personalizados:**',
                                               value='Estes sãos os comandos personalizados deste servidor. **Não precisam do prefixo**',
                                               inline=False)
                    for comando_personalizado in comandos_personalizados:
                        if comando_personalizado[0] is not None:
                            resposta = ComandoPersonalizadoDao().get_resposta(ctx.guild.id, comando_personalizado[0])
                            if resposta[-1]:  # se o inText estiver on:
                                lista_de_comando.add_field(
                                    name=f'<a:check:754719579648950342>``{comando_personalizado[0]}``',
                                    value=f'Eu irei responder "{resposta[0]}"', inline=True)
                            else:
                                lista_de_comando.add_field(
                                    name=f'<a:check:754719579648950342>``{comando_personalizado[0]}``',
                                    value=f'Eu irei responder "{resposta[0]}" **apenas se a mensagem iniciar com o comando**',
                                    inline=True)
            await ctx.send(embed=embed)
            await ctx.send(embed=lista_de_comando)
        else:
            for cog in self.bot.cogs:  # Abre todos os cogs que o bot têm
                for command in self.bot.get_cog(cog).get_commands(): # pega todos os comandos do cog
                    if str(command) == f'help_{comando.lower()}':  # se o comando for help_comando
                        await command(ctx) # chama ele xD
                        return
            await ctx.send(f'Comando não encontrado')
            return


def setup(bot):
    bot.add_cog(Help(bot))
