select * from game
left join game_file
on game.wos_id = game_file.game_wos_id
where game.wos_id>9000000 and
game.genre='' or game.genre is null
order by tosec_path