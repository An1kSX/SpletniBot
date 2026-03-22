CREATE TABLE IF NOT EXISTS "bot_settings" (
  "setting_key" varchar PRIMARY KEY,
  "value" varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS "users" (
  "telegram_id" bigint PRIMARY KEY ON DELETE CASCADE,
  "nickname" varchar,
  "username" varchar,
  "first_name" varchar NOT NULL,
  "last_name" varchar,
  "role_id" integer NOT NULL REFERENCES "roles" ("id") DEFAULT 3,
  "accepted_rules" bool NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS "roles" (
  "id" SERIAL PRIMARY KEY on DELETE CASCADE,
  "title" varchar UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS "banned" (
  "user_id" bigint PRIMARY KEY REFERENCES "users" ("telegram_id") ON DELETE CASCADE,
  "banned_at" timestamp,
  "reason" text
);


INSERT INTO "bot_settings" ("setting_key", "value")
VALUES ('is_working', 'True')
ON CONFLICT ("setting_key") DO NOTHING;

INSERT INTO "bot_settings" ("setting_key", "value")
VALUES ('post_num', '1')
ON CONFLICT ("setting_key") DO NOTHING;

INSERT INTO "roles" ("title")
VALUES ('superadmin')
ON CONFLICT ("title") DO NOTHING;

INSERT INTO "roles" ("title")
VALUES ('admin')
ON CONFLICT ("title") DO NOTHING;

INSERT INTO "roles" ("title")
VALUES ('user')
ON CONFLICT ("title") DO NOTHING;