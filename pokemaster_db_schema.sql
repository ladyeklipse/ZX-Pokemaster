BEGIN TRANSACTION;
CREATE TABLE "game" (
	`wos_id`	INTEGER NOT NULL AUTO_INCREMENT, -- ZXDB entries.entry_id
	`name`	VARCHAR(255), -- ZXDB entries.title
	`publisher`	VARCHAR(255), -- ZXDB labels.name WHERE labels.id=publishers.label_id AND publishers.entry_id=entries.id AND releases.release_seq == 0
	`year`	INTEGER, -- ZXDB releases.release_year WHERE releases.release_seq == 0
	`genre`	VARCHAR(255), -- ZXDB genretypes.text WHERE genretypes.id=entries.genretype_id
	`x_rated`	INTEGER DEFAULT 0, -- ZXDB entries.is_xrated
	`number_of_players`	INTEGER DEFAULT 1, -- ZXDB entries.max_players
	`multiplayer_type` CHAR(1), -- ZXDB entries.multiplaytype_id
	`machine_type`	VARCHAR(20), -- ZXDB machinetypes.text WHERE download_machinetype.id=downloads.machinetype_id
	`language`	CHAR(2), -- ZXDB entries.idiom_id
	`availability`	CHAR(1), -- ZXDB entries.availabletype_id
	`tipshop_page`	TEXT, -- Retrieved by scraping the-tipshop.co.uk Database Index: "0123.htm" and "%s.html" where %s=[a-z]
	`pok_file_contents`	BLOB, -- Retrieved by scraping the-tipshop.co.uk and manual correction
	`tipshop_multiface_pokes_section` BLOB, -- Retrieved by scraping the-tipshop.co.uk with the only purpose of making manual checking easier.
	PRIMARY KEY(`wos_id`)
);
INSERT INTO game VALUES (9000000, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
DELETE FROM game WHERE wos_id = 9000000;
CREATE TABLE "game_release" (
	`wos_id`	INTEGER, -- ZXDB entries.entry_id
	`release_seq`	INTEGER, -- ZXDB releases.release_seq
	`name`	TEXT, -- ZXDB aliases.title WHERE aliases.entry_id=entries.id AND aliases.release_seq=releases.release_seq
	`year`	INTEGER, -- ZXDB releases.release_year
	`publisher`	TEXT, -- ZXDB labels.name WHERE labels.id=publishers.label_id AND publishers.entry_id=entries.id AND releases.release_seq == publishers.release_seq
	`country`	TEXT, -- ZXDB labels.country
	`ingame_screen_gif_filepath`	TEXT, -- ZXDB downloads.file_link WHERE formattypes.text = "Picture" AND filetypes.text = "Loading screen"
	`ingame_screen_gif_filesize`	INTEGER, -- ZXDB downloads.file_size for abovementioned row
	`ingame_screen_scr_filepath`	TEXT, -- ZXDB downloads.file_link WHERE formattypes.text = "Screen Dump" AND filetypes.text = "Loading screen"
	`ingame_screen_scr_filesize`	INTEGER, -- ZXDB downloads.file_size for abovementioned row
	`loading_screen_gif_filepath`	TEXT, -- ZXDB downloads.file_link WHERE formattypes.text = "Picture" AND filetypes.text = "In-game screen"
	`loading_screen_gif_filesize`	INTEGER, -- ZXDB downloads.file_size for abovementioned row
	`loading_screen_scr_filepath`	TEXT, -- ZXDB downloads.file_link WHERE formattypes.text = "Screen Dump" AND filetypes.text = "In-game screen"
	`loading_screen_scr_filesize`	INTEGER, -- ZXDB downloads.file_size for abovementioned row
	`manual_filepath`	TEXT, -- ZXDB downloads.file_link WHERE download.file_link.endswith('.txt') AND filetypes.text = "In-game screen"
	`manual_filesize`	INTEGER -- ZXDB downloads.file_size for abovementioned row
);
CREATE TABLE "game_file" (
	`game_wos_id`	INT NOT NULL,  -- ZXDB entries.entry_id
	`game_release_seq`	INTEGER, -- ZXDB releases.release_seq
	`wos_name`	VARCHAR(255), -- name of UNZIPPED file retrieved by reading the zipped file downloaded from FTP mirror.
	`wos_path`	VARCHAR(255), -- ZXDB downloads.file_link WHERE formattypes.text contains "snapshot", "disk" or "tape".
	`tosec_path`	TEXT, -- TOSEC path, assigned to selected wos_id and release_seq by complex algorythm and manually hardcodd exceptions for cases where it fails
	`machine_type`	INTEGER, -- ZXDB entry_machinetype.text WHERE download_machinetype.id=downloads.machinetype_id OR (if wos_path==NULL) - from TOSEC filename ([128K], [48K] or [48/128K])
	`format`	TEXT, -- extension of UNZIPPED file, always lower case, retrieved by reading the file.
	`size`	INTEGER, -- size of UNZIPPED file retrieved by reading the file
	`size_zipped`	INTEGER, -- size of .zip file from FTP or TOSEC. This field is DEPRECATED
	`is_demo` INTEGER, -- TOSEC - 1 if (demo) in name, else 0
	`part`	INTEGER DEFAULT 1, -- TOSEC - %d if (Part %d) in name or (Disk %d) in name, 0 by default
	`side`	INTEGER, -- TOSEC - 1 if (Side A) in name, 2 if (Side B) in name, 0 by default.
	`language`	CHAR(2), -- TOSEC - 2-letter language code in round brackets "()"
	`mod_flags`	VARCHAR(255), -- TOSEC - Data in square brackets, starting with c, m, f, h, b
	`notes`	VARCHAR(255), -- TOSEC - All data in square brackets "[]" except machine_type and those in mod_flags
	`md5`	CHAR(32) UNIQUE, -- MD5 of unzipped file, retrieved by reading the file
	`crc32`	TEXT, -- CRC32 of unzipped file, retrieved by reading the file
	`sha1`	TEXT -- SHA1 of unzipped file, retrieved by reading the file
);
CREATE UNIQUE INDEX `unique_release` ON `game_release` (`wos_id` ,`release_seq` );
-- CREATE UNIQUE INDEX `unique_alias` ON `game_alias` (`wos_id` ,`release_id` ,`name` );
CREATE VIEW `game_id_file_checker` AS select wos_id, game.name, game_file.tosec_path,
game_file.wos_name, game_file.wos_path from game
left join game_file on game_file.game_wos_id=game.wos_id
order by game.name;
COMMIT;
