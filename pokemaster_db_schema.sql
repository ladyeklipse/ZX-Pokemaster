BEGIN TRANSACTION;
CREATE TABLE "game_release" (
	`wos_id`	INTEGER,
	`release_seq`	INTEGER,
	`name`	TEXT,
	`year`	INTEGER,
	`publisher`	TEXT,
	`country`	TEXT,
	`ingame_screen_gif_filepath`	TEXT,
	`ingame_screen_gif_filesize`	INTEGER,
	`ingame_screen_scr_filepath`	TEXT,
	`ingame_screen_scr_filesize`	INTEGER,
	`loading_screen_gif_filepath`	TEXT,
	`loading_screen_gif_filesize`	INTEGER,
	`loading_screen_scr_filepath`	TEXT,
	`loading_screen_scr_filesize`	INTEGER,
	`manual_filepath`	TEXT,
	`manual_filesize`	INTEGER
);
CREATE TABLE "game_file" (
	`game_wos_id`	INT NOT NULL,
	`game_release_seq`	INTEGER,
	`wos_name`	VARCHAR(255),
	`wos_path`	VARCHAR(255),
	`tosec_path`	TEXT,
	`machine_type`	INTEGER,
	`format`	TEXT,
	`size`	INTEGER,
	`size_zipped`	INTEGER,
	`part`	INTEGER DEFAULT 1,
	`side`	INTEGER,
	`language`	CHAR(2),
	`mod_flags`	VARCHAR(255),
	`md5`	CHAR(32) UNIQUE,
	`md5_zipped`	CHAR(32),
	`crc32`	TEXT,
	`sha1`	TEXT
);
CREATE TABLE `game_alias` (
	`wos_id`	INTEGER,
	`release_id`	INTEGER,
	`name`	INTEGER
);
CREATE TABLE "game" (
	`wos_id`	INTEGER NOT NULL,
	`name`	VARCHAR(255),
	`publisher`	VARCHAR(255),
	`year`	INTEGER,
	`genre`	VARCHAR(255),
	`x_rated`	INTEGER DEFAULT 0,
	`number_of_players`	INTEGER DEFAULT 1,
	`multiplayer_type` CHAR(1),
	`machine_type`	VARCHAR(20),
	`language`	CHAR(2),
	`availability`	CHAR(1),
	`tipshop_page`	TEXT,
	`pok_file_contents`	BLOB,
	`tipshop_multiface_pokes_section`	BLOB,
	PRIMARY KEY(`wos_id`)
);
CREATE UNIQUE INDEX `unique_release` ON `game_release` (`wos_id` ,`release_seq` );
CREATE UNIQUE INDEX `unique_alias` ON `game_alias` (`wos_id` ,`release_id` ,`name` );
CREATE VIEW `game_id_file_checker` AS select wos_id, game.name, game_file.tosec_path,
game_file.wos_name, game_file.wos_path from game
left join game_file on game_file.game_wos_id=game.wos_id
order by game.name;
COMMIT;
