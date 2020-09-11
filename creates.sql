CREATE TABLE IF NOT EXISTS servers (
    serverId BIGINT PRIMARY KEY NOT NULL,
    prefixo TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS blacklist (
    pessoaId BIGINT PRIMARY KEY NOT NULL
);
CREATE TABLE IF NOT EXISTS comandos_personalizados (
    serverId BIGINT NOT NULL,
    comando TEXT NOT NULL,
    resposta TEXT NOT NULL,
    inText BOOLEAN NOT NULL,
    PRIMARY KEY (serverId, comando),
    FOREIGN KEY (serverId)
        REFERENCES servers (serverId)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);
CREATE TABLE IF NOT EXISTS comandos_desativados (
    serverId BIGINT NOT NULL,
    comando TEXT NOT NULL,
    PRIMARY KEY (serverId, comando),
    FOREIGN KEY (serverId)
        REFERENCES servers (serverId)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);
CREATE TABLE IF NOT EXISTS informacoes_do_bot (
    informacao TEXT PRIMARY KEY NOT NULL,
    dado TEXT NOT NULL
);