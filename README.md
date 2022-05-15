# Androxus - Um bot feito 100% pelo Canas
[![ReadMe Card](https://github-readme-stats.vercel.app/api/pin/?username=devRMA&repo=Androxus&theme=blue-green)](https://github.com/anuraghazra/github-readme-stats)
<br>
[![MIT License][license-shield]][license-url]

Um bot para o discord feito em python, usando <a href="https://github.com/Rapptz/discord.py">discord.py</a> e PostgreSQL. O bot tem alguns comandos matemáticos, alguns comandos de diversão.
Caso você fique em dúvida sobre algum comando, acesse a <a href="https://devrma.github.io/Androxus/">documentação</a>.
## 🤔 Como eu consigo criar um bot, com os comandos do Androxus?
### Passos para você conseguir hospedar uma versão do Androxus
1. Clone este repositório.
2. Instale o <a href="https://www.python.org/">Python</a>.
3. Você também vai precisar instalar o <a href="https://www.postgresql.org/">PostgreSQL</a>.
4. Instale os módulos externos `pip install -r requirements.txt`.
5. Vá em <a href="https://github.com/devRMA/Androxus/blob/master/configs.json">configs.json</a> e configure tudo. Você deve colocar o seu id, o id de chat que o bot deve mandar as mensagens que enviam no dm dele. Você deve colocar o token do bot, a string de conexão do banco e todos os emojis personalizados, que o bot vai usar.
6. Acesse o arquivo <a href="https://github.com/devRMA/Androxus/blob/master/database/database.pgsql">database.pgsql</a> e execute todos estes comandos no teu banco de dados.
7. Acesse <a href="https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html"> este link </a> e baixe o certificado _rds-combined-ca-bundle.pem_ e coloque-o pasta **database/Factories/certificate**.
8. Rode os testes do banco de dados `python database/Test/test.py`.
9. Rode também os testes das funções uteis `python utils/test.py`.
10. Se você configurou tudo certo, basta ir na pasta principal, e digitar `python main.py`.
#### Observação:
- Caso você não tenha habilitado as Intents, no portal do dev, <a href="https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents">ative</a>! Se essa opção não estiver ativada, o bot não vai funcionar corretamente.

[license-shield]: https://img.shields.io/github/license/devRMA/Androxus
[license-url]: https://github.com/devRMA/Androxus/blob/master/LICENSE
