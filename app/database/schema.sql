CREATE TABLE "bot_settings" (
  "key" varchar PRIMARY KEY,
  "value" varchar NOT NULL
);

CREATE TABLE "users" (
  "telegram_id" bigint PRIMARY KEY,
  "nickname" varchar,
  "username" varchar,
  "first_name" varchar NOT NULL,
  "last_name" varchar,
  "role_id" integer NOT NULL
);

CREATE TABLE "roles" (
  "id" integer PRIMARY KEY,
  "title" varchar UNIQUE NOT NULL
);

CREATE TABLE "banned" (
  "user_id" bigint PRIMARY KEY,
  "banned_at" timestamp,
  "reason" text
);

ALTER TABLE "users" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "banned" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("telegram_id") DEFERRABLE INITIALLY IMMEDIATE;
