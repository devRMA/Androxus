-- Criando a table que vai guardar as pessoas que estão banidas de usar o bot
CREATE TABLE IF NOT EXISTS blacklist(
    pessoaId BIGINT PRIMARY KEY NOT NULL
);

-- na Versão 2.1 foi adicionado o motivo e quando que a pessoa foi banida de usar o bot
ALTER TABLE blacklist
ADD COLUMN motivo TEXT DEFAULT NULL,
ADD COLUMN quando TEXT DEFAULT NULL;

-- Table que vai guardar outras informações do bot (como por exemplo, a última cotação, no comando "money")
CREATE TABLE IF NOT EXISTS bot(
    informacao TEXT PRIMARY KEY NOT NULL,
    dado TEXT NOT NULL
);

-- Table que vai ser usada para guardar TODOS os servidore que o bot está
CREATE TABLE IF NOT EXISTS servidor(
    serverId BIGINT PRIMARY KEY NOT NULL,
    prefixo TEXT NOT NULL
);

-- Na versão 2.09 foi adicionado os logs e as sugestões de comando

ALTER TABLE servidor
ADD COLUMN channelIdLog BIGINT NULL DEFAULT NULL,
ADD COLUMN logMensagemDeletada BOOLEAN DEFAULT FALSE,
ADD COLUMN logMensagemEditada BOOLEAN DEFAULT FALSE,
ADD COLUMN logAvatarAlterado BOOLEAN DEFAULT FALSE,
ADD COLUMN logNomeAlterado BOOLEAN DEFAULT FALSE,
ADD COLUMN logTagAlterado BOOLEAN DEFAULT FALSE,
ADD COLUMN logNickAlterado BOOLEAN DEFAULT FALSE,
ADD COLUMN logRoleAlterado BOOLEAN DEFAULT FALSE,
ADD COLUMN sugestaoDeComando BOOLEAN DEFAULT TRUE;

-- Table que vai guardar todos os comandos desativados
CREATE TABLE IF NOT EXISTS comandos_off(
    serverId BIGINT NOT NULL,
    comando TEXT NOT NULL,
    PRIMARY KEY (serverId, comando),
    FOREIGN KEY (serverId)
        REFERENCES servidor (serverId)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

-- Table que vai guardar todos os comandos personalizados de um servidor
CREATE TABLE IF NOT EXISTS comandos_personalizados(
    serverId BIGINT NOT NULL,
    comando TEXT NOT NULL,
    resposta TEXT NOT NULL,
    inText BOOLEAN NOT NULL,
    PRIMARY KEY (serverId, comando),
    FOREIGN KEY (serverId)
        REFERENCES servidor (serverId)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

-- Create, Read e Delete da table blacklist

-- procedure que vai adicionar um valor
CREATE PROCEDURE blacklist_add
(
    BIGINT,
    TEXT,
    TEXT
)
AS
$$
    INSERT INTO blacklist VALUES( $1, $2, $3 )
$$
LANGUAGE SQL;

-- function que vai fazer o select
CREATE FUNCTION blacklist_get_pessoa
(
    BIGINT
)
RETURNS
    TABLE
    (
        pessoaId BIGINT,
        motivo TEXT,
        quando TEXT

    )
AS
$$
    SELECT * FROM blacklist WHERE pessoaId = $1
$$
LANGUAGE SQL;

-- procedure que vai vai fazer o delete
CREATE PROCEDURE blacklist_remove
(
    BIGINT
)
AS
$$
    DELETE FROM blacklist WHERE pessoaId = $1
$$
LANGUAGE SQL;

-- CRUD (Create, Read, Update e Delete) da table comandos_off
CREATE PROCEDURE cmd_desativado_add
(
    BIGINT,
    TEXT
)
AS
$$
    INSERT INTO comandos_off(serverId, comando) VALUES($1, $2)
$$
LANGUAGE SQL;


CREATE FUNCTION cmd_desativado_get_comandos
(
    serverId BIGINT
)
RETURNS
    TABLE
    (
        comando TEXT
    )
AS
$$
    SELECT comando FROM comandos_off WHERE serverId = $1
$$
LANGUAGE SQL;

CREATE PROCEDURE cmd_desativado_remove
(
    BIGINT,
    TEXT
)
AS
$$
    DELETE FROM comandos_off WHERE serverId = $1 AND comando = $2
$$
LANGUAGE SQL;

-- CRUD (Create, Read, Update e Delete) da table comandos_personalizados

CREATE PROCEDURE cmd_personalizado_add
(
    BIGINT,
    TEXT,
    TEXT,
    BOOLEAN
)
AS
$$
    INSERT INTO comandos_personalizados(serverId, comando, resposta, inText) VALUES($1, $2, $3, $4)
$$
LANGUAGE SQL;

CREATE FUNCTION get_cmds_personalizados
(
    BIGINT
)
RETURNS
    TABLE
    (
        comando TEXT,
        resposta TEXT,
        inText BOOLEAN
    )
AS
$$
    SELECT comando, resposta, inText FROM comandos_personalizados WHERE serverId = $1
$$
LANGUAGE SQL;

CREATE PROCEDURE cmd_personalizado_update
(
    TEXT,
    BOOLEAN,
    BIGINT,
    TEXT
)
AS 
$$
    UPDATE comandos_personalizados SET resposta = $1, inText = $2 WHERE serverId = $3 AND comando = $4
$$
LANGUAGE SQL;

CREATE PROCEDURE cmd_personalizado_remove
(
    BIGINT,
    TEXT
)
AS
$$
    DELETE FROM comandos_personalizados WHERE serverId = $1 AND comando = $2
$$
LANGUAGE SQL;

-- CRUD (Create, Read, Update e Delete) da table bot

CREATE PROCEDURE info_add
(
    TEXT,
    TEXT
)
AS
$$
    INSERT INTO bot(informacao, dado) VALUES($1, $2)
$$
LANGUAGE SQL;


CREATE FUNCTION info_get
(
    TEXT
)
RETURNS
    TABLE
    (
        dado TEXT
    )
AS
$$
    SELECT dado FROM bot WHERE informacao = $1
$$
LANGUAGE SQL;

CREATE PROCEDURE info_update
(
    TEXT,
    TEXT
)
AS
$$
    UPDATE bot SET dado = $1 WHERE informacao = $2
$$
LANGUAGE SQL;

CREATE PROCEDURE info_remove
(
    TEXT
)
AS
$$
    DELETE FROM bot WHERE informacao = $1
$$
LANGUAGE SQL;

-- CRUD (Create, Read, Update e Delete) da table servidor

CREATE PROCEDURE server_add
(
    BIGINT,
    TEXT
)
AS
$$
    INSERT INTO servidor VALUES($1, $2)
$$
LANGUAGE SQL;

CREATE FUNCTION get_server
(
    BIGINT
)
RETURNS
    TABLE
    (
        prefixo TEXT,
        channelIdLog BIGINT,
        logMensagemDeletada BOOLEAN,
        logMensagemEditada BOOLEAN,
        logAvatarAlterado BOOLEAN,
        logNomeAlterado BOOLEAN,
        logTagAlterado BOOLEAN,
        logNickAlterado BOOLEAN,
        logRoleAlterado BOOLEAN,
        sugestaoDeComando BOOLEAN
    )
AS
$$
    SELECT
        prefixo, 
        channelIdLog,
        logMensagemDeletada,
        logMensagemEditada,
        logAvatarAlterado,
        logNomeAlterado,
        logTagAlterado,
        logNickAlterado,
        logRoleAlterado,
        sugestaoDeComando
    FROM
        servidor
    WHERE
        serverId = $1;
$$
LANGUAGE SQL;

CREATE PROCEDURE server_update
(
    TEXT, -- 1 - prefixo
    BIGINT, -- 2 - channelIdLog
    BOOLEAN, -- 3- logMensagemDeletada
    BOOLEAN, -- 4 - logMensagemEditada
    BOOLEAN, -- 5 - logAvatarAlterado
    BOOLEAN, -- 6 - logNomeAlterado
    BOOLEAN, -- 7 - logTagAlterado
    BOOLEAN, -- 8 - logNickAlterado
    BOOLEAN, -- 9 - logRoleAlterado
    BOOLEAN, -- 10 - sugestaoDeComando
    BIGINT -- 11 - serverId
)
AS
$$
    UPDATE servidor 
        SET
            prefixo = $1,
            channelIdLog = $2,
            logMensagemDeletada = $3,
            logMensagemEditada = $4,
            logAvatarAlterado = $5,
            logNomeAlterado = $6,
            logTagAlterado = $7,
            logNickAlterado = $8,
            logRoleAlterado = $9,
            sugestaoDeComando = $10
    WHERE
        serverId = $11;
$$
LANGUAGE SQL;

CREATE PROCEDURE server_remove
(
    BIGINT
)
AS
$$
    DELETE FROM servidor WHERE serverId = $1;
    DELETE FROM comandos_personalizados WHERE serverId = $1;
    DELETE FROM comandos_off WHERE serverId = $1;
$$
LANGUAGE SQL;

-- para fazer um select, em vez de fazer a query no bot, ele só 
-- chama a function, e em vez de criar, atualizar e deletar no bot
-- ele só chama a procedure.
