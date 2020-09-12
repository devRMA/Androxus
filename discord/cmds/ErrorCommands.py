# coding=utf-8
# Androxus bot
# ErrorCommands.py

__author__ = 'Rafael'

from discord.ext import commands
class ErrorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #font: https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound,)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.errors.NotOwner):
            await ctx.send(f'{ctx.author.mention} você não é meu criador ;-;')

def setup(bot):
    bot.add_cog(ErrorCommands(bot))
