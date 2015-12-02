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
	fname	text not null
);
INSERT INTO "first_name" VALUES(1,'Elisabeth');
INSERT INTO "first_name" VALUES(2,'Marie');
INSERT INTO "first_name" VALUES(3,'Dupont');
INSERT INTO "first_name" VALUES(4,'valérie');
INSERT INTO "first_name" VALUES(5,'Yvan');
CREATE TABLE password(
	id	integer primary key autoincrement,
	passwd	text not null
);
INSERT INTO "password" VALUES(1,'123456');
INSERT INTO "password" VALUES(2,'p@sswd');
INSERT INTO "password" VALUES(3,'qwerty');
INSERT INTO "password" VALUES(4,'azerty');
CREATE TABLE people(
	cn text primary key,
	email text not null,
	passwd text not null, 
	modified date 
);
INSERT INTO "people" VALUES('Pierre Richard','pr@unicaen.fr','123456',NULL);
INSERT INTO "people" VALUES('lionel Messi','lm@hello.fr','123456','2015-12-02 14:04:58');
INSERT INTO "people" VALUES('Pierre Richards','pr@unicaen.fr','123456','2015-12-02 14:06:15');
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('last_name',6);
INSERT INTO "sqlite_sequence" VALUES('first_name',5);
INSERT INTO "sqlite_sequence" VALUES('password',4);
COMMIT;
