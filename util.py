def scan(game, x, y, dir_x, dir_y, distance=8):
    #dir_x and dir_y are from -1 to 1 and represent the direction we are scanning
    #i.e. (dir_x,dir_y) is a normal vector in the correct direction
    piece = game.get(x,y)
    wtm = game.white_to_move
    is_capturable = lambda str : str.islower() if wtm else str.isupper()
    for i in range(1,distance):
        scanned_square = game.get(x + i*dir_x, y + i*dir_y)
        print(scanned_square)
        if scanned_square == '-':
            game.generate_legal_move(x, y, i*dir_x, i*dir_y, piece)
        else:
            if scanned_square == '0':
                return
            if is_capturable(scanned_square):
                game.generate_legal_move(x, y, i*dir_x, i*dir_y, piece)
            return

