-- upgrade --
ALTER TABLE "sberaddress" ALTER COLUMN "address" TYPE VARCHAR(256) USING "address"::VARCHAR(256);
ALTER TABLE "sberaddress" ALTER COLUMN "last_transaction_id" TYPE VARCHAR(256) USING "last_transaction_id"::VARCHAR(256);
-- downgrade --
ALTER TABLE "sberaddress" ALTER COLUMN "address" TYPE VARCHAR(64) USING "address"::VARCHAR(64);
ALTER TABLE "sberaddress" ALTER COLUMN "last_transaction_id" TYPE VARCHAR(64) USING "last_transaction_id"::VARCHAR(64);
