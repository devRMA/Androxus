# coding=utf-8
# Androxus bot
# Avatar.py

__author__ = 'Rafael'

from discord.ext import commands
from discord.modelos.EmbedHelp import embedHelp


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def help_avatar(self, ctx):
        embed = embedHelp(self.bot,
                          ctx,
                          comando='avatar',
                          descricao=self.avatar.description,
                          parametros=['<"Mencionar uma pessoa ou um id">'],
                          exemplos=['``{pref}avatar``' + f' {ctx.author.mention}'])
        await ctx.send(content=ctx.author.mention, embed=embed)

    @commands.command(description='Eu vou mandar a foto de perfil da pessoa que você marcar.')
    async def avatar(self, ctx, *args):
        if ctx.message.mentions:  # se tiver alguma menção na mensagem
            await ctx.send(f'{ctx.message.mentions[0].avatar_url}')  # vai pegar a primeira menção, e pega o avatar da pessoa
        else:  # se a pessoa não mencionou ninguém, entra aqui
            if args:  # se a pessoa passou pelo menos alguma coisa
                if len(args) == 1:  # se a pessoa passou mais de um item
                    try:  # vai tentar converter o argumento para int
                        id_de_quem_ver_o_avatar = int(args[0])  # conversão
                        user = self.bot.get_user(id_de_quem_ver_o_avatar)  # se chegou aqui, vai tentar pegar o usuário com esse id
                        if user is not None:  # se achou uma pessoa
                            await ctx.send(f'{user.avatar_url}')  # vai mandar o avatar desta pessoa
                        else:  # se o user for None, é porque o bot não achou esse usuário
                            await ctx.send('<a:sad:755774681008832623> Não consegui encontrar o usuário' +
                                           f' <@{id_de_quem_ver_o_avatar}>\nEu preciso ter pelo menos 1' +
                                           ' servidor em comum com a pessoa, para conseguir encontrar ele.')
                    except ValueError:  # se der erro, é porque a pessoa não passou apenas números
                        await ctx.send(f'<a:atencao:755844029333110815> O valor {args[0]} não é um id!')
                else:  # se a pessoa passou mais de 1 argumento
                    await ctx.send('<a:atencao:755844029333110815> Você me disse muitas coisas,' +
                                   ' eu só preciso, ou do id da pessoa, ou que você mencione ela.')
            else:  # se a pessoa não passou nenhum argumento:
                await ctx.send(f'{ctx.author.avatar_url}')


def setup(bot):
    bot.add_cog(Avatar(bot))
