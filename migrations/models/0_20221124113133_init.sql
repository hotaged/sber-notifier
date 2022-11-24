-- upgrade --
CREATE TABLE IF NOT EXISTS "blockchainaddress" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "address" VARCHAR(256) NOT NULL UNIQUE,
    "last_transaction_id" VARCHAR(256),
    "chain" VARCHAR(16)
);
CREATE TABLE IF NOT EXISTS "telegramuser" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "telegram_id" BIGINT NOT NULL UNIQUE,
    "is_admin" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "telegramuser_blockchainaddress" (
    "telegramuser_id" INT NOT NULL REFERENCES "telegramuser" ("id") ON DELETE CASCADE,
    "blockchainaddress_id" INT NOT NULL REFERENCES "blockchainaddress" ("id") ON DELETE CASCADE
);
