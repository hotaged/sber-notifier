-- upgrade --
CREATE TABLE IF NOT EXISTS "sberaddress" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "address" VARCHAR(64) NOT NULL UNIQUE,
    "last_transaction_id" VARCHAR(64)
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
CREATE TABLE IF NOT EXISTS "telegramuser_sberaddress" (
    "telegramuser_id" INT NOT NULL REFERENCES "telegramuser" ("id") ON DELETE CASCADE,
    "sberaddress_id" INT NOT NULL REFERENCES "sberaddress" ("id") ON DELETE CASCADE
);
