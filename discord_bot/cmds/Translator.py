# coding=utf-8
# Androxus bot
# Translator.py

__author__ = 'Rafael'

from discord.ext import commands
from discord_bot.modelos.EmbedHelp import embedHelp
from googletrans import Translator


class Translator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['help_tradutor', 'help_traduza', 'help_translate', 'help_translator'])
    async def help_traduzir(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando=self.traduzir.name,
                          descricao=self.traduzir.description,
                          parametros=['<língua final>', '<frase>'],
                          exemplos=['``{pref}traduzir`` ``pt`` ``Hello world!``',
                                    '``{pref}translate`` ``en`` ``Olá Mundo!``',
                                    '``{pref}traduza`` ``pt`` ``Здравствуйте!``'],
                          # precisa fazer uma copia da lista, senão, as alterações vão refletir aqui tbm
                          aliases=self.traduzir.aliases.copy())
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(aliases=['tradutor', 'traduza', 'translate', 'translator'],
                      description='Eu vou traduzir alguma frase!')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def traduzir(self, ctx, dest=None, *frase):
        if dest and frase:
            from googletrans.constants import LANGUAGES
            dests = []
            for lang in LANGUAGES.items():
                # vai pegar o dicionario de todas as linguas que o módulo aceita
                # e transformar em uma lista, apenas com a abreviação
                dests.append(lang[0])
            if not dest in dests:  # se o "dest" que a pessoa passou não for válido:
                return await ctx.send(f'Não encontrei nenhuma lingua chamada ``{dest}``!\n<a:sad:755774681008832623>')
            frase = ' '.join(frase)  # transforma a lista numa string única
            # anti mention:
            if ctx.message.mentions:  # se tiver alguma menção na mensagem
                for mention in ctx.message.mentions:
                    frase = frase.replace(f'<@{mention.id}>', '')
                    frase = frase.replace(f'<@!{mention.id}>', '')
            frase = frase.replace(f'@', '@\uFEFF')  # quebra o @everyone e o @here
            # se após a remoção das menções, não sobrar nada, para a execução
            if len(frase.replace(' ', '')) == 0: return
            msg = Translator().translate(frase, dest=dest).text.capitalize()
            await ctx.send(content=f'{ctx.author.mention} {msg}')
        else:
            await self.help_traduzir(ctx)


def setup(bot):
    bot.add_cog(Translator(bot))
