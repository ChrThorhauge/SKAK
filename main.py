import pygame as p
import Engine


WIDTH = 1024
HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

#hello

piece_images = {}



## global variable to store images of pieces

def load_images():
    pieces = ["bB", "bK", "bN", "bQ", "bR", "bp", "wB", "wK", "wN", "wQ", "wR", "wp"]
    for piece in pieces:
        piece_images[piece] = p.transform.scale(p.image.load("images_classic/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


## main driver

def main(): 
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("white"))
   
    clock = p.time.Clock()
    gs = Engine.Game_state()

    load_images()
    running = True

    square_selected = () # no square is selected initially
    player_clicks = []
    
    valid_moves = gs.get_valid_moves()
    move_made = False 

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                if square_selected == (row, col):
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)
                if len(player_clicks) == 2:
                    move = Engine.move(player_clicks[0], player_clicks[1], gs.board)
                    if move in valid_moves: 
                        gs.make_move(move)
                        move_made = True
                        print(move.get_chess_notation())
                        square_selected = ()
                        player_clicks = []
                    else:
                        player_clicks = [square_selected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True

        if move_made:
            move_made = False
            valid_moves = gs.get_valid_moves()


        clock.tick(MAX_FPS)
        draw_game_state(screen, gs)
        p.display.flip()


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)



def draw_board(screen):
    colors = [p.Color((238, 238, 210)), p.Color((118, 150, 86))]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(piece_images[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



main()
print("hello")
