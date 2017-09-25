select game.wos_id, 
game.name, 
game.year,
game_release.year,
game.publisher, 
game_release.publisher from game
left join game_release
on game.wos_id==game_release.wos_id
WHERE game_release.modded_by IS NOT NULL