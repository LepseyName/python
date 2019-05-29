SIZEx = 2
ALL_SIZE={"step": (5, 5), "padding":(10, 10), "plain":(720, 600), "segment":(20, 20), "pause":(300, 300), "label":(240, 40)}
ALL_TEXT={"play":"press pause", "not_records":"Records not found!", "not_saves":"Saves not found!", "title":"My PySneak for university", "pause":("Continue", "Exit","Save"),"menu":("Game", "Saves", "Records", "Exit", "ob")}
ALL_COLO={"ok":(0,2,0), "body":(0, 0, 255), "pause":(255,0,12),"menu_shadow":(0,255,0), "menu":(80,90,150),"sneak":(255,255,255), "sneak_head":(89,125,35), "wall":(50,128,25), "eat":(255,5,255), "beetles":(0,0,0)}
ALL_TIME={"FPS":0.2, "beetles_move":0.15, "eat": 4, "beetles": 6, "win":2}
ALL_FILE={"sound_exit" : "sound_exit.wav", "sound_win": "sound_win.wav", "sound_bittles": "sound_bittles.wav", "sound_wall": "sound_wall.wav", "music_game": "music_game.mp3", "music_ground": "music_ground.mp3", "sound_eat":"sound_eat.wav", "bild_eat": "eat.png", "bild_place": "place.png", "saves": "saves.poshel_ot_sjuda", "records": "records.poshel_ot_sjuda", "info":"j.png", "bild_sneak":"a.png", "bild_sneak_head":"sneak_head.png", "bild_beetle":"beetle.png", "bild_wall":"bar.png"}
ALL_LIFE={"eat":4, "beetles":3}
ALL_BILD={}
ALL_SOUN={}
GAME = True
QUIT = False

RIGHT=( 1, 0)
LEFT =(-1, 0)
UP   =( 0,-1)
DOWN =( 0, 1)
VECT = (LEFT, RIGHT, UP, DOWN)

ALL_SIZE["body"] = (ALL_SIZE["plain"][0], ALL_SIZE["plain"][1] + ALL_SIZE["label"][1])
