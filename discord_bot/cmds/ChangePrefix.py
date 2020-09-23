# coding=utf-8
# Androxus bot
# ChangePrefix.py

__author__ = 'Rafael'

from discord.ext import commands
import discord
from discord_bot.dao.ServidorDao import ServidorDao
from discord_bot.utils.Utils import random_color, pegar_o_prefixo, get_emoji_dance
from discord_bot.utils import permissions
from discord_bot.modelos.EmbedHelp import embedHelp
from datetime import datetime


class ChangePrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_prefixo', 'help_prefix'])
    async def help_change_prefix(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.change_prefix.name,
                          descricao=self.change_prefix.description,
                          parametros=['``[prefixo (padrão: "--")]``'],
                          exemplos=['``{pref}change_prefix`` ``!!``',
                                    '``{pref}prefixo``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.change_prefix.aliases.copy(),
                          perm_pessoa='administrador')
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['prefixo', 'prefix'], description='Comando que é usado para mudar o meu prefixo')
    @permissions.has_permissions(administrator=True)
    @commands.guild_only()
    async def change_prefix(self, ctx, prefixo_novo='--'):
        prefixo_antigo = pegar_o_prefixo(None, ctx)
        ServidorDao().update(ctx.guild.id, prefixo_novo)
        if prefixo_novo != '--':
            embed = discord.Embed(title=f'Prefixo alterado com sucesso!', colour=discord.Colour(random_color()),
                                  description=f'Prefixo antigo: {prefixo_antigo}\n'+
                                              f'Prefixo novo: {prefixo_novo}',
                                  timestamp=datetime.utcnow())
            embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            embed.add_field(name='\uFEFF',
                            value=f'Caso queria voltar para o prefixo padrão, basta digitar ``{prefixo_novo}prefixo``!' +
                                  f'\n{get_emoji_dance()}',
                            inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Agora estou com o prefixo padrão! {get_emoji_dance()}')


def setup(bot):
    bot.add_cog(ChangePrefix(bot))
