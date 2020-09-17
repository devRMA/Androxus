# coding=utf-8
# Androxus bot
# Clear.py

#imports
import discord
from discord.ext import commands

#class
class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefixo = '..'

    #limpar
    @commands.guild_only()
    @commands.command(aliases=['limpar', 'clear'])
    async def clean(self, ctx, quantia = None):
        aliases = ['limpar', 'clear']
        embed = discord.Embed(title='WolfZ - Ajuda - Clean', url='https://wolfz-bot.glitch.me', description='', color=0x0000ff)
        embed.set_author(name='===By yWolfBR#1330===')
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/755521679337455729/755521704800813246/WolfZ.png')
        embed.add_field(name=':duvida: **Como usar?**', value='**`--clean + Quantidade`**', inline=False)
        for c in range(0, aliases):
            aliases[c] = f'{self.prefixo}{aliases[c]}'
        embed.add_field(name=':igual: **Sinônimos**', value=', '.join(aliases), inline=False)
        embed.set_footer(text='https://wolfz-bot.glitch.me')
        if quantia is None:
            await ctx.send(embed=embed)
            return
        try:
            quantia = int(quantia)  # aqui vai verificar se a pessoa passou um número inteiro
            # se não deu erro, pode continuar
            if quantia <= 300: # um limite, para que a pessoa não consiga pagara 99999 mensagens
                try:
                    await ctx.channel.purge(limit=quantia+1)
                except discord.Forbidden:
                    await ctx.send('O bot não tem permissão para apagar mensagens!')
                except discord.HTTPException:
                    await ctx.send('Ocorreu um erro da API na hora de apagar as mensagens!')
                except Exception as error:
                    await ctx.send(f'Ocorreu o erro ```{error}```')
            else:
                await ctx.send('O limite de mensagens para apagar é 300!')
        except ValueError:
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Clear(client))
