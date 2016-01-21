PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE last_name(
	id	integer primary key autoincrement,
	lname	text not null
);
INSERT INTO "last_name" VALUES(1,'Jean');
INSERT INTO "last_name" VALUES(2,'Baptiste');
INSERT INTO "last_name" VALUES(3,'André');
INSERT INTO "last_name" VALUES(4,'Pierre');
INSERT INTO "last_name" VALUES(5,'Simon');
INSERT INTO "last_name" VALUES(6,'Richard');
CREATE TABLE first_name(
	id	integer primary key autoincrement,
	fname	text not null,
	gender	text not null
);
INSERT INTO "first_name" VALUES(1,'Elisabeth','F');
INSERT INTO "first_name" VALUES(2,'Marie','F');
INSERT INTO "first_name" VALUES(3,'Dupont','M');
INSERT INTO "first_name" VALUES(4,'valérie','F');
INSERT INTO "first_name" VALUES(5,'Yvan','M');
CREATE TABLE password(
	id	integer primary key autoincrement,
	passwd	text not null
);
INSERT INTO "password" VALUES(1,'123456');
INSERT INTO "password" VALUES(2,'p@sswd');
INSERT INTO "password" VALUES(3,'qwerty');
INSERT INTO "password" VALUES(4,'azerty');
CREATE TABLE person(
	cn text primary key,
	fname text not null,
	lname text not null,
	email text not null,
	passwd text not null,
	birth date not null,
	gender text not null,
	modified date);
INSERT INTO "person" VALUES('hello world','hello','world','hello.world@test.fr','azerty','2015-11-25','M','2015-12-09 12:29:43');
CREATE TABLE broker(
id integer primary key,
url text not null,
insert_date date not null,
schedule_date date default null,
processed boolean not null);
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('last_name',6);
INSERT INTO "sqlite_sequence" VALUES('first_name',5);
INSERT INTO "sqlite_sequence" VALUES('password',4);
COMMIT;
