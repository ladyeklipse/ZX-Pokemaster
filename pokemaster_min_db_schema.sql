BEGIN TRANSACTION;
DROP TABLE IF EXISTS `game_release`;
CREATE TABLE IF NOT EXISTS `game_release` (
	`zxdb_id`	INTEGER,
	`release_seq`	INTEGER,
	`name`	TEXT,
	`year`	INTEGER,
	`publisher`	TEXT,
	`country`	TEXT
);
DROP TABLE IF EXISTS `game_file`;
CREATE TABLE IF NOT EXISTS `game_file` (
	`game_zxdb_id`	INT NOT NULL,
	`game_release_seq`	INTEGER,
	`machine_type`	TEXT,
	`format`	TEXT,
	`size`	INTEGER,
	`content_desc`	TEXT,
	`is_demo`	INTEGER,
	`release_date`	TEXT,
	`part`	INTEGER DEFAULT 1,
	`side`	INTEGER,
	`language`	CHAR ( 2 ),
	`mod_flags`	VARCHAR ( 255 ),
	`notes`	VARCHAR ( 255 ),
	--`priority` INTEGER DEFAULT 0,
	`md5`	CHAR ( 32 ),
	`crc32`	TEXT,
	`sha1`	TEXT
);
DROP TABLE IF EXISTS `game`;
CREATE TABLE IF NOT EXISTS `game` (
	`zxdb_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`name`	VARCHAR ( 255 ),
	`publisher`	VARCHAR ( 255 ),
	`author`	TEXT,
	`year`	INTEGER,
	`genre`	VARCHAR ( 255 ),
	`x_rated`	INTEGER DEFAULT 0,
	`number_of_players`	INTEGER DEFAULT 1,
	`machine_type`	VARCHAR ( 20 ),
	`language`	CHAR ( 2 ),
	`availability`	CHAR ( 1 ),
	`pok_file_contents`	BLOB
	`publisher_url` TEXT,
	`price` VARCHAR(20)
);
COMMIT;
