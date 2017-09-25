SELECT * FROM game 
LEFT JOIN game_file
ON game_file.game_wos_id=game.wos_id
WHERE game.pok_file_contents IS NOT NULL and
game.pok_file_contents!='' and
game_file.crc32 IS NULL