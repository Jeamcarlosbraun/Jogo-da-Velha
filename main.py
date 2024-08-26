import pygame
import sys
import math

# Inicializa o Pygame
pygame.init()

# Configurações de tela
screen_width = 300
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo da Velha")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

# Fonte
font = pygame.font.Font(None, 40)

# Constantes
PLAYER_X = 1
PLAYER_O = -1
EMPTY = 0

# Tabuleiro
board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

# Função para desenhar o tabuleiro
def draw_board():
    screen.fill(BLACK)
    for row in range(1, 3):
        pygame.draw.line(screen, WHITE, (0, row * 100), (300, row * 100), 5)
        pygame.draw.line(screen, WHITE, (row * 100, 0), (row * 100, 300), 5)
    
    for row in range(3):
        for col in range(3):
            if board[row][col] == PLAYER_X:
                pygame.draw.line(screen, RED, (col * 100 + 25, row * 100 + 25), (col * 100 + 75, row * 100 + 75), 5)
                pygame.draw.line(screen, RED, (col * 100 + 75, row * 100 + 25), (col * 100 + 25, row * 100 + 75), 5)
            elif board[row][col] == PLAYER_O:
                pygame.draw.circle(screen, WHITE, (col * 100 + 50, row * 100 + 50), 35, 5)

# Função para verificar vitória
def check_win(board):
    for row in range(3):
        if abs(sum(board[row])) == 3:
            return board[row][0]
    
    for col in range(3):
        if abs(board[0][col] + board[1][col] + board[2][col]) == 3:
            return board[0][col]
    
    if abs(board[0][0] + board[1][1] + board[2][2]) == 3:
        return board[0][0]
    
    if abs(board[0][2] + board[1][1] + board[2][0]) == 3:
        return board[0][2]
    
    return None

# Função para verificar se o tabuleiro está cheio
def is_board_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True

# Função Minimax com poda alfa-beta
def minimax(board, depth, alpha, beta, maximizing):
    winner = check_win(board)
    if winner is not None:
        return winner
    if is_board_full(board):
        return 0
    
    if maximizing:
        max_eval = -math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_X
                    eval = minimax(board, depth + 1, alpha, beta, False)
                    board[row][col] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_O
                    eval = minimax(board, depth + 1, alpha, beta, True)
                    board[row][col] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Função para IA fazer a melhor jogada
def ai_move():
    best_score = -math.inf
    best_move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                board[row][col] = PLAYER_X
                score = minimax(board, 0, -math.inf, math.inf, False)
                board[row][col] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    
    if best_move:
        board[best_move[0]][best_move[1]] = PLAYER_X

# Função para criar botões
def create_button(text, x, y, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))

    if text_rect.collidepoint(mouse):
        pygame.draw.rect(screen, active_color, text_rect.inflate(20, 20))
        if click[0] == 1 and action is not None:
            return action
    else:
        pygame.draw.rect(screen, inactive_color, text_rect.inflate(20, 20))

    screen.blit(text_surface, text_rect)
    return None

# Função principal
def main():
    global board
    player = PLAYER_O
    game_over = False
    play_vs_ai = None
    
    # Tela inicial com botões
    while play_vs_ai is None:
        screen.fill(BLACK)
        option1 = create_button("Jogar contra a IA", screen_width // 2, 100, GRAY, RED, action=True)
        option2 = create_button("Jogar contra Pessoa", screen_width // 2, 180, GRAY, RED, action=False)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if option1 is not None:
            play_vs_ai = option1
        elif option2 is not None:
            play_vs_ai = option2
    
    while True:
        draw_board()
        pygame.display.flip()

        winner = check_win(board)
        if winner is not None or is_board_full(board):
            game_over = True
            # Mensagem de fim de jogo
            if winner == PLAYER_X:
                message = "X venceu!"
            elif winner == PLAYER_O:
                message = "O venceu!"
            else:
                message = "Empate!"

            print_message(message)
            pygame.time.wait(2000)
            board = [[EMPTY, EMPTY, EMPTY],
                     [EMPTY, EMPTY, EMPTY],
                     [EMPTY, EMPTY, EMPTY]]
            main()  # Volta ao menu inicial

        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]

                    clicked_row = mouseY // 100
                    clicked_col = mouseX // 100

                    if board[clicked_row][clicked_col] == EMPTY:
                        board[clicked_row][clicked_col] = player
                        player = PLAYER_X if player == PLAYER_O else PLAYER_O

        if play_vs_ai and player == PLAYER_X:
            ai_move()
            player = PLAYER_O

def print_message(message):
    screen.fill(BLACK)
    text_surface = font.render(message, True, WHITE)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

if __name__ == "__main__":
    main()
