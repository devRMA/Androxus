# coding=utf-8
# Androxus bot
# ComandoPersonalizado.py

__author__ = 'Rafael'

from datetime import datetime
import discord
from discord.ext import commands
from discord_bot.dao.ComandoPersonalizadoDao import ComandoPersonalizadoDao
from discord_bot.utils.Utils import random_color, get_emoji_dance
from discord_bot.utils import permissions
from discord_bot.modelos.EmbedHelp import embedHelp


class ComandoPersonalizado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_add_command', 'help_ac'])
    async def help_adicionar_comando(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.adicionar_comando.name,
                          descricao=self.adicionar_comando.description,
                          parametros=['<"comando">', '<"resposta">', '[ignorar a posição do comando (sim/nao)]'],
                          exemplos=['``{pref}adicionar_comando`` ``"bom dia"`` ``"bom dia!"``',
                                    '``{pref}ac`` ``"hello world!"`` ``"olá mundo!"`` ``não``'],
                          aliases=self.adicionar_comando.aliases.copy(),
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          perm_pessoa='administrador')
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['add_command', 'ac'], description='Adiciona comandos personalizados')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def adicionar_comando(self, ctx, comando=None, resposta=None, inText='t'):
        inText = inText.lower()
        if inText != None:
            if inText in ['t', 'true', 's', 'sim', '1', 'y', 'yes']:
                inText = True
            elif inText in ['f', 'false', 'n', 'não', 'nao', '0', 'n', 'no']:
                inText = False
            else:
                await ctx.send(f'Valor ``{inText}`` inválido! Os valores que eu aceito são: sim, não, yes, no, 0, 1')
                return
        if (comando is None) or (resposta is None):
            await self.help_adicionar_comando(ctx)
            return
        if ComandoPersonalizadoDao().create(ctx.guild.id, comando, resposta, inText):
            inText_str = str(inText).replace('True', 'Sim').replace('False', 'Não')
            embed = discord.Embed(title=f'Comando adicionado com sucesso!', colour=discord.Colour(random_color()),
                                  description='\uFEFF',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            embed.add_field(name=f"Informações",
                            value=f"Comando: {comando}\nResposta: {resposta}\nIgnorar a posição do comando: {inText_str}",
                            inline=False)
            await ctx.send(content=get_emoji_dance(), embed=embed)

    @commands.command(hidden=True, aliases=['help_remove_command', 'help_rc'])
    async def help_remover_comando(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.remover_comando.name,
                          descricao=self.remover_comando.description,
                          parametros=['<"comando">'],
                          exemplos=['``{pref}remover_comando`` ``"bom dia"``',
                                    '``{pref}rc`` ``"hello world!"``'],
                          aliases=self.remover_comando.aliases.copy(),
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          perm_pessoa='administrador')
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['remove_command', 'rc'], description='Remove um comando personalizado')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def remover_comando(self, ctx, comando=None):
        if comando is None:
            await self.help_remover_comando(ctx)
            return
        if ComandoPersonalizadoDao().delete(ctx.guild.id, comando):
            embed = discord.Embed(title=f'Comando removido com sucesso!', colour=discord.Colour(random_color()),
                                  description='\uFEFF',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(content=get_emoji_dance(), embed=embed)

    @commands.command(hidden=True, aliases=['help_update_command', 'help_mc'])
    async def help_modificar_comando(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.modificar_comando.name,
                          descricao=self.modificar_comando.description,
                          parametros=['<"comando">', '<"resposta">', '[ignorar a posição do comando na mensagem (sim/nao). O padrão é sim]'],
                          exemplos=['``{pref}modificar_comando`` ``"bom dia"`` ``"boa noite!"``',
                                    '``{pref}mc`` ``"olá mundo!"`` ``"hello world!"`` ``sim``'],
                          aliases=self.modificar_comando.aliases.copy(),
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          perm_pessoa='administrador')
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['update_command', 'mc'], description='Modifica um comando personalizado')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def modificar_comando(self, ctx, comando=None, resposta=None, inText='t'):
        inText = inText.lower()
        if inText != None:
            if inText in ['t', 'true', 's', 'sim', '1', 'y', 'yes']:
                inText = True
            elif inText in ['f', 'false', 'n', 'não', 'nao', '0', 'n', 'no']:
                inText = False
            else:
                await ctx.send(f'Valor ``{inText}`` inválido! Os valores que eu aceito são: sim, não, yes, no, 0, 1')
                return
        if (comando is None) or (resposta is None):
            await self.help_modificar_comando(ctx)
            return
        if ComandoPersonalizadoDao().update(ctx.guild.id, comando, resposta, inText):
            inText_str = str(inText).replace('True', 'Sim').replace('False', 'Não')
            embed = discord.Embed(title=f'Comando modificado com sucesso!', colour=discord.Colour(random_color()),
                                  description=f"Comando: {comando}\nResposta: {resposta}\n" +
                                              f"Ignorar a posição do comando: {inText_str}",
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(content=get_emoji_dance(), embed=embed)


def setup(bot):
    bot.add_cog(ComandoPersonalizado(bot))
