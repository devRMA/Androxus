# coding=utf-8
# Androxus bot
# Change_prefix.py

__author__ = 'Rafael'

from discord.ext import commands

from discord.dao.ServidorDao import ServidorDao


class Change_prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['prefixo', 'prefix'])
    async def change_prefix(self, ctx, prefixo_novo='--'):
        ServidorDao().update(ctx.guild.id, prefixo_novo)
        if prefixo_novo != '--':
            await ctx.send(
                f'Agora o meu  prefixo é ``{prefixo_novo}``\nCaso queria voltar para o prefixo padrão, basta digitar ``{prefixo_novo}prefixo``')
        else:
            await ctx.send(f'Agora estou com o prefixo padrão!')


def setup(bot):
    bot.add_cog(Change_prefix(bot))
