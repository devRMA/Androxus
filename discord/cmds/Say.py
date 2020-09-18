# coding=utf-8
# Androxus bot
# Say.py

__author__ = 'Rafael'

from discord.ext import commands
from discord.modelos.EmbedHelp import embedHelp


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_fale', 'help_falar'])
    async def help_say(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando='say',
                          descricao=self.say.description,
                          parametros=['<frase>'],
                          exemplos=['``{pref}say`` ``Hello World!!``', '``{pref}fale`` ``Olá Mundo!``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.say.aliases.copy(),
                          perm_pessoa='gerenciar mensagens')
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['fale', 'falar'], description='Eu vou repetir o que você falar!')
    async def say(self, ctx, *, frase: str):
        try:
            if ctx.guild.me.guild_permissions.manage_messages:
                await ctx.message.delete()
            if not ctx.author.permissions_in(ctx.message.channel).manage_messages:
                frase += f'\n\n- {ctx.author}'
        except:  # se der algum erro, provavelmente é porque o comando foi usado no dm
            pass
        frase = frase.replace('@everyone', '<a:no_no:755774680325029889>')
        frase = frase.replace('@here', '<a:no_no:755774680325029889>')
        await ctx.send(frase)


def setup(bot):
    bot.add_cog(Say(bot))
