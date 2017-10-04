SELECT 
game_file.tosec_path
FROM game_file
LEFT JOIN game_release
ON 
game_file.game_wos_id = game_release.wos_id
and
game_file.game_release_seq = game_release.release_seq
WHERE game_release.publisher like '19%' 
or game_release.publisher like '20%'
order by tosec_path