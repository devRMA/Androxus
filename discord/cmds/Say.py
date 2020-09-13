# coding=utf-8
# Androxus bot
# Say.py

__author__ = 'Rafael'

from discord.ext import commands


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['fale', 'falar'], description='Manda o bot falar uma frase xD')
    async def say(self, ctx, *, frase: str):
        try:
            if ctx.guild.me.guild_permissions.manage_messages:
                await ctx.message.delete()
            if not ctx.author.permissions_in(ctx.message.channel).manage_messages:
                frase += f'\n\n- {ctx.author}'
        except:  # se der algum erro, provavelmente é porque o comando foi usado no dm
            pass
        await ctx.send(frase)


def setup(bot):
    bot.add_cog(Say(bot))
