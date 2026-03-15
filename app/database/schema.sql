CREATE TABLE "bot_settings" (
  "setting_key" varchar PRIMARY KEY,
  "value" varchar NOT NULL
);

CREATE TABLE "users" (
  "telegram_id" bigint PRIMARY KEY,
  "nickname" varchar,
  "username" varchar,
  "first_name" varchar NOT NULL,
  "last_name" varchar,
  "role_id" integer NOT NULL,
  "accepted_rules" bool NOT NULL DEFAULT false
);

CREATE TABLE "roles" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar UNIQUE NOT NULL
);

CREATE TABLE "banned" (
  "user_id" bigint PRIMARY KEY,
  "banned_at" timestamp,
  "reason" text
);

ALTER TABLE "users" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "banned" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("telegram_id") DEFERRABLE INITIALLY IMMEDIATE;


INSERT INTO "bot_settings" ("setting_key", "value") VALUES ('is_working', 'True');
INSERT INTO "bot_settings" ("setting_key", "value") VALUES ("post_num", "1");

INSERT INTO "roles" ("title") VALUES ("superadmin");
INSERT INTO "roles" ("title") VALUES ("admin");
INSERT INTO "roles" ("title") VALUES ("user");
