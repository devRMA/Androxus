# coding=utf-8
# Androxus bot
# ChangePrefix.py

__author__ = 'Rafael'

from discord.ext import commands
from discord.dao.ServidorDao import ServidorDao
from discord.Utils import random_color, pegar_o_prefixo, get_emoji_dance
from discord.modelos.EmbedHelp import embedHelp


class ChangePrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_prefixo', 'help_prefix'])
    async def help_change_prefix(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando='change_prefix',
                          descricao=self.change_prefix.description,
                          parametros=['``[prefixo (padrão: "--")]``'],
                          exemplos=['``{pref}change_prefix`` ``!!``',
                                    '``{pref}prefixo``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.change_prefix.aliases.copy(),
                          perm_pessoa='administrador')
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['prefixo', 'prefix'], description='Comando que é usado para mudar o meu prefixo')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def change_prefix(self, ctx, prefixo_novo='--'):
        ServidorDao().update(ctx.guild.id, prefixo_novo)
        if prefixo_novo != '--':
            await ctx.send(
                f'Agora o meu  prefixo é ``{prefixo_novo}``\nCaso queria voltar para o prefixo padrão, basta digitar ' +
                f'``{prefixo_novo}prefixo``\n{get_emoji_dance()}')
        else:
            await ctx.send(f'Agora estou com o prefixo padrão! {get_emoji_dance()}')


def setup(bot):
    bot.add_cog(ChangePrefix(bot))
