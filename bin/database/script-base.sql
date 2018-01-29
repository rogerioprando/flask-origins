
-- enable extensions --
-- full-text search on postgresql
-- enable features
CREATE TEXT SEARCH CONFIGURATION pt ( COPY = portuguese );
CREATE EXTENSION unaccent;

-- default features enabled on 'pt'
ALTER TEXT SEARCH CONFIGURATION pt ALTER MAPPING
FOR hword, hword_part, word WITH unaccent, portuguese_stem;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- table: user
DROP TABLE IF EXISTS xf_user;
CREATE TABLE IF NOT EXISTS xf_user(
    id bigserial not null primary key,
    internal uuid not null unique default uuid_generate_v4(),
    created timestamp not null default now(),
	active boolean not null default false,
	name text not null,
	user_name text not null unique,
	user_email text not null unique,
	user_password text not null,
	is_admin boolean not null default false,
	file_name text,
	file_url text,
	company text,
	occupation text
);

DROP TABLE IF EXISTS xf_login_activities;
CREATE TABLE IF NOT EXISTS xf_login_activities (
    internal uuid not null primary key default uuid_generate_v4(),
    created timestamp not null default now(),
    user_id bigint not null,
    action text not null,
    ip_address text not null,
    ua_header text not null,
    ua_device text not null
);

alter table xf_login_activities add constraint fk_login_user foreign key (user_id) references xf_user(id);

DROP TABLE IF EXISTS xf_auth_api;
CREATE TABLE IF NOT EXISTS xf_auth_api (
    internal uuid not null primary key default uuid_generate_v4(),
	created timestamp not null default now(),
	client_secret text not null unique,
	api_key text not null unique
);

