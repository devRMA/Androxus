# Androxus
[![MIT License][license-shield]][license-url]

Um bot para o discord feito em python usando <a href="https://github.com/Rapptz/discord.py">discord.py</a> e postgreSQL. O bot tem alguns comandos matemáticos, alguns comandos de diversão.
Caso você fique em dúvida sobre algum comando, acesse a <a href="https://devrma.github.io/Androxus/">documentação</a>.
## 🤔 Como eu consigo criar um bot, com os comandos do Androxus?
### Passos para você conseguir hospedar uma versão do Androxus
1. Clonar este repositório.
2. Você vai precisar do <a href="https://www.python.org/">Python</a> instalado.
3. Você também vai precisar do <a href="https://www.postgresql.org/">PostgreSQL</a> instalado.
4. Vá em <a href="https://github.com/devRMA/Androxus/blob/master/configs.json">configs.json</a> e configure tudo. Você deve colocar o seu id, o id de chat que o bot deve mandar as mensagens que enviam no dm dele. Você deve colocar o token do bot, a string de conexão do banco e todos os emojis personalizados, que o bot vai usar.
5. Acesse o arquivo <a href="https://github.com/devRMA/Androxus/blob/master/database/database.pgsql">database.pgsql</a> e execute todos estes comandos no teu banco de dados.
6. Se você configurou tudo certo, basta ir na pasta principal, e digitar `python main.py`.
#### Observação:
- Caso você não tenha habilitado as Intents, no portal do dev, <a href="https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents">ative</a>! Se essa opção não estiver ativada, o bot não vai funcionar corretamente.

[license-shield]: https://img.shields.io/github/license/devRMA/Androxus
[license-url]: https://github.com/devRMA/Androxus/blob/master/LICENSE