# coding=utf-8
# Androxus bot
# Say.py

__author__ = 'Rafael'

from discord.ext import commands

from discord_bot.modelos.EmbedHelp import embedHelp


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_fale', 'help_falar'])
    async def help_say(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.say.name,
                          descricao=self.say.description,
                          parametros=['<frase>'],
                          exemplos=['``{pref}say`` ``Hello World!!``', '``{pref}fale`` ``Olá Mundo!``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.say.aliases.copy(),
                          perm_pessoa='gerenciar mensagens')
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['fale', 'falar'], description='Eu vou repetir o que você falar!')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def say(self, ctx, *frase):
        if len(frase) == 0:
            await self.help_say(ctx)
            return
        frase = ' '.join(frase)
        try:
            if ctx.guild.me.guild_permissions.manage_messages:
                await ctx.message.delete()
            if not ctx.author.permissions_in(ctx.message.channel).manage_messages:
                frase += f'\n\n- {ctx.author}'
            # se a pessoa não tiver perm de marca everyone
            if not ctx.author.permissions_in(ctx.message.channel).mention_everyone:
                if ctx.message.mentions:  # se tiver alguma menção na mensagem
                    for mention in ctx.message.mentions:
                        frase = frase.replace(f'<@{mention.id}>', '')
                        frase = frase.replace(f'<@!{mention.id}>', '')
                frase = frase.replace(f'@', '@\uFEFF')
                frase = frase.replace(f'&', '&\uFEFF')
        except:  # se der algum erro, provavelmente é porque o comando foi usado no dm
            pass
        if len(frase) == 0:  # se após os filtros, a mensagem ficou vazia
            frase = '.'
        await ctx.send(frase)


def setup(bot):
    bot.add_cog(Say(bot))
