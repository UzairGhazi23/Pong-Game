# Menu Screen
menu = input("In Which Difficulty do you want to play game:\nEasy\nMedium\nHard\n")
player_1=input("Enter the Name of Player 1: ")
player_2=input("Enter the Name of Player 2: ")
player_1 = player_1 + " "
player_2 = player_2 + " "
if menu == "easy" or menu == 'Easy':
    import pygame

    # Initialize the pygame:
    pygame.init()

    # Screen Customization:
    WIDTH, HEIGHT = 700, 500
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    # Screen title :
    pygame.display.set_caption("Ping Pong (Easy)")

    FPS = 60

    # Colors used in this game:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    AQUA = (0, 128, 128)

    # Paddle width and Height:
    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

    # ball radius : r = D/2
    BALL_RADIUS = 12

    # Font type and size:
    SCORE_FONT = pygame.font.SysFont("Calibre", 40)

    # Total Game Score:
    WINNING_SCORE = 5


    # Defining and initializing the paddle:

    class Paddle:  # defines and structures all of the object
        COLOR = WHITE
        # Max velocity of the paddle when ball strikes
        VEL = 8

        def __init__(paddle, x, y, width, height):
            paddle.x = paddle.original_x = x
            paddle.y = paddle.original_y = y
            paddle.width = width
            paddle.height = height

        def draw(paddle, win):
            pygame.draw.rect(
                win, paddle.COLOR, (paddle.x, paddle.y, paddle.width, paddle.height))

        def move(paddle, up=True):
            if up:
                paddle.y -= paddle.VEL
            else:
                paddle.y += paddle.VEL

        def reset(paddle):
            paddle.x = paddle.original_x
            paddle.y = paddle.original_y


    # Defining and initializing the ball:
    class Ball:

        # Max velocity of a ball:
        MAX_VEL = 5
        COLOR = WHITE

        def __init__(ball, x, y, radius):
            ball.x = ball.original_x = x
            ball.y = ball.original_y = y
            ball.radius = radius
            ball.x_vel = ball.MAX_VEL
            ball.y_vel = 0

        def draw(ball, win):
            pygame.draw.circle(win, ball.COLOR, (ball.x, ball.y), ball.radius)

        def move(ball):
            ball.x += ball.x_vel
            ball.y += ball.y_vel

        def reset(ball):
            ball.x = ball.original_x
            ball.y = ball.original_y
            ball.y_vel = 0
            ball.x_vel *= -1


    # DRAWING OF THE ELEMENTS IN THE SCREEN WITH RESPECT TO POSITION:
    def draw(win, paddles, ball, left_score, right_score):
        win.fill(AQUA)

        left_score_text = SCORE_FONT.render(player_1+"Score: "+f"{left_score}", 1, WHITE)
        right_score_text= SCORE_FONT.render(player_2+"Score: "+f"{right_score}", 1, WHITE)
        win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
        win.blit(right_score_text, (WIDTH * (3 / 4) -
                                    right_score_text.get_width() // 2, 20))

        for paddle in paddles:
            paddle.draw(win)

        for i in range(10, HEIGHT, HEIGHT // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

        ball.draw(win)
        pygame.display.update()


    # HANDLING THE COLLISION OF THE BALL WITH PADDLE:
    def handle_collision(ball, left_paddle, right_paddle):
        if ball.y + ball.radius >= HEIGHT:
            ball.y_vel *= -1
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1

        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                    ball.x_vel *= -1

                    middle_y = left_paddle.y + left_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                if ball.x + ball.radius >= right_paddle.x:
                    ball.x_vel *= -1

                    middle_y = right_paddle.y + right_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel


    # CONTROLING THE MOVEMENT OF PADDLES:

    def handle_paddle_movement(keys, left_paddle, right_paddle):
        if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(up=True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
            left_paddle.move(up=False)

        if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
            right_paddle.move(up=False)


    # DEFINING MAIN FUNCTION AND CALLING THE FUNCTIONS TO EXECUTE THE GAME:
    def main():
        run = True

        clock = pygame.time.Clock()

        left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT //
                             2, PADDLE_WIDTH, PADDLE_HEIGHT)
        right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                              2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

        left_score = 0
        right_score = 0

        while run:
            WIN.fill(BLACK)
            clock.tick(FPS)
            draw(WIN, (left_paddle, right_paddle), ball, left_score, right_score)
            # WIN.blit(background,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            handle_paddle_movement(keys, left_paddle, right_paddle)

            ball.move()
            handle_collision(ball, left_paddle, right_paddle)

            if ball.x < 0:
                right_score += 1
                ball.reset()
            elif ball.x > WIDTH:
                left_score += 1
                ball.reset()

            won = False
            if left_score >= WINNING_SCORE:
                won = True
                win_text = "Left Player Won!"
            elif right_score >= WINNING_SCORE:
                won = True
                win_text = "Right Player Won!"

            if won:
                text = SCORE_FONT.render(win_text, 1, WHITE)
                WIN.blit(text, (WIDTH // 2 - text.get_width() //
                                2, HEIGHT // 2 - text.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(5000)
                ball.reset()
                left_paddle.reset()
                right_paddle.reset()
                left_score = 0
                right_score = 0
                break

        pygame.quit()


    if __name__ == '__main__':
        main()


elif menu == "Medium" or menu == "medium":
    import pygame

    # Initialize the pygame:
    pygame.init()

    # Screen Customization:
    WIDTH, HEIGHT = 700, 500
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    # Screen title :
    pygame.display.set_caption("Ping Pong (Medium)")

    FPS = 60

    # Colors used in this game:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREY = (128, 128, 128)

    # Paddle width and Height:
    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

    # ball radius : r = D/2
    BALL_RADIUS = 10

    # Font type and size:
    SCORE_FONT = pygame.font.SysFont("Times New Roman", 40)

    # Total Game Score:
    WINNING_SCORE = 5


    # Defining and initializing the paddle:

    class Paddle:  # defines and structures all of the object
        COLOR = WHITE
        # Max velocity of the paddle when ball strikes
        VEL = 5

        def __init__(paddle, x, y, width, height):
            paddle.x = paddle.original_x = x
            paddle.y = paddle.original_y = y
            paddle.width = width
            paddle.height = height

        def draw(paddle, win):
            pygame.draw.rect(
                win, paddle.COLOR, (paddle.x, paddle.y, paddle.width, paddle.height))

        def move(paddle, up=True):
            if up:
                paddle.y -= paddle.VEL
            else:
                paddle.y += paddle.VEL

        def reset(paddle):
            paddle.x = paddle.original_x
            paddle.y = paddle.original_y


    # Defining and initializing the ball:
    class Ball:

        # Max velocity of a ball:
        MAX_VEL = 8
        COLOR = YELLOW

        def __init__(ball, x, y, radius):
            ball.x = ball.original_x = x
            ball.y = ball.original_y = y
            ball.radius = radius
            ball.x_vel = ball.MAX_VEL
            ball.y_vel = 0

        def draw(ball, win):
            pygame.draw.circle(win, ball.COLOR, (ball.x, ball.y), ball.radius)

        def move(ball):
            ball.x += ball.x_vel
            ball.y += ball.y_vel

        def reset(ball):
            ball.x = ball.original_x
            ball.y = ball.original_y
            ball.y_vel = 0
            ball.x_vel *= -1


    # DRAWING OF THE ELEMENTS IN THE SCREEN WITH RESPECT TO POSITION:
    def draw(win, paddles, ball, left_score, right_score):
        win.fill(GREY)

        left_score_text = SCORE_FONT.render("Left Score:"f"{left_score}", 1, WHITE)
        right_score_text = SCORE_FONT.render("Right Score:"f"{right_score}", 1, WHITE)
        win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
        win.blit(right_score_text, (WIDTH * (3 / 4) -
                                    right_score_text.get_width() // 2, 20))

        for paddle in paddles:
            paddle.draw(win)

        for i in range(10, HEIGHT, HEIGHT // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

        ball.draw(win)
        pygame.display.update()


    # HANDLING THE COLLISION OF THE BALL WITH PADDLE:
    def handle_collision(ball, left_paddle, right_paddle):
        if ball.y + ball.radius >= HEIGHT:
            ball.y_vel *= -1
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1

        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                    ball.x_vel *= -1

                    middle_y = left_paddle.y + left_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                if ball.x + ball.radius >= right_paddle.x:
                    ball.x_vel *= -1

                    middle_y = right_paddle.y + right_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel


    # CONTROLING THE MOVEMENT OF PADDLES:

    def handle_paddle_movement(keys, left_paddle, right_paddle):
        if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(up=True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
            left_paddle.move(up=False)

        if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
            right_paddle.move(up=False)


    # DEFINING MAIN FUNCTION AND CALLING THE FUNCTIONS TO EXECUTE THE GAME:
    def main():
        run = True

        clock = pygame.time.Clock()

        left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT //
                             2, PADDLE_WIDTH, PADDLE_HEIGHT)
        right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                              2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

        left_score = 0
        right_score = 0

        while run:
            WIN.fill(BLACK)
            clock.tick(FPS)
            draw(WIN, (left_paddle, right_paddle), ball, left_score, right_score)
            # WIN.blit(background,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            handle_paddle_movement(keys, left_paddle, right_paddle)

            ball.move()
            handle_collision(ball, left_paddle, right_paddle)

            if ball.x < 0:
                right_score += 1
                ball.reset()
            elif ball.x > WIDTH:
                left_score += 1
                ball.reset()

            won = False
            if left_score >= WINNING_SCORE:
                won = True
                win_text = "Left Player Won!"
            elif right_score >= WINNING_SCORE:
                won = True
                win_text = "Right Player Won!"

            if won:
                text = SCORE_FONT.render(win_text, 1, WHITE)
                WIN.blit(text, (WIDTH // 2 - text.get_width() //
                                2, HEIGHT // 2 - text.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(5000)
                ball.reset()
                left_paddle.reset()
                right_paddle.reset()
                left_score = 0
                right_score = 0
                break

        pygame.quit()


    if __name__ == '__main__':
        main()


elif menu == "Hard" or menu == "hard":
    import pygame

    # Initialize the pygame:
    pygame.init()

    # Screen Customization:
    WIDTH, HEIGHT = 700, 500
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    # Screen title :
    pygame.display.set_caption("Ping Pong (Hard)")

    FPS = 60

    # Colors used in this game:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    N_BLUE = (0, 0, 128)

    # Paddle width and Height:
    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

    # ball radius : r = D/2
    BALL_RADIUS = 7

    # Font type and size:
    SCORE_FONT = pygame.font.SysFont("Times New Roman", 40)

    # Total Game Score:
    WINNING_SCORE = 15


    # Defining and initializing the paddle:

    class Paddle:  # defines and structures all of the object
        COLOR = WHITE
        # Max velocity of the paddle when ball strikes
        VEL = 5

        def __init__(paddle, x, y, width, height):
            paddle.x = paddle.original_x = x
            paddle.y = paddle.original_y = y
            paddle.width = width
            paddle.height = height

        def draw(paddle, win):
            pygame.draw.rect(
                win, paddle.COLOR, (paddle.x, paddle.y, paddle.width, paddle.height))

        def move(paddle, up=True):
            if up:
                paddle.y -= paddle.VEL
            else:
                paddle.y += paddle.VEL

        def reset(paddle):
            paddle.x = paddle.original_x
            paddle.y = paddle.original_y


    # Defining and initializing the ball:
    class Ball:

        # Max velocity of a ball:
        MAX_VEL = 12
        COLOR = RED

        def __init__(ball, x, y, radius):
            ball.x = ball.original_x = x
            ball.y = ball.original_y = y
            ball.radius = radius
            ball.x_vel = ball.MAX_VEL
            ball.y_vel = 0

        def draw(ball, win):
            pygame.draw.circle(win, ball.COLOR, (ball.x, ball.y), ball.radius)

        def move(ball):
            ball.x += ball.x_vel
            ball.y += ball.y_vel

        def reset(ball):
            ball.x = ball.original_x
            ball.y = ball.original_y
            ball.y_vel = 0
            ball.x_vel *= -1


    # DRAWING OF THE ELEMENTS IN THE SCREEN WITH RESPECT TO POSITION:
    def draw(win, paddles, ball, left_score, right_score):
        win.fill(BLACK)

        left_score_text = SCORE_FONT.render("Left Score:"f"{left_score}", 1, WHITE)
        right_score_text = SCORE_FONT.render("Right Score:"f"{right_score}", 1, WHITE)
        win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
        win.blit(right_score_text, (WIDTH * (3 / 4) -
                                    right_score_text.get_width() // 2, 20))

        for paddle in paddles:
            paddle.draw(win)

        for i in range(10, HEIGHT, HEIGHT // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

        ball.draw(win)
        pygame.display.update()


    # HANDLING THE COLLISION OF THE BALL WITH PADDLE:
    def handle_collision(ball, left_paddle, right_paddle):
        if ball.y + ball.radius >= HEIGHT:
            ball.y_vel *= -1
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1

        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                    ball.x_vel *= -1

                    middle_y = left_paddle.y + left_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                if ball.x + ball.radius >= right_paddle.x:
                    ball.x_vel *= -1

                    middle_y = right_paddle.y + right_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel


    # CONTROLING THE MOVEMENT OF PADDLES:

    def handle_paddle_movement(keys, left_paddle, right_paddle):
        if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(up=True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
            left_paddle.move(up=False)

        if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
            right_paddle.move(up=False)


    # DEFINING MAIN FUNCTION AND CALLING THE FUNCTIONS TO EXECUTE THE GAME:
    def main():
        run = True

        clock = pygame.time.Clock()

        left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT //
                             2, PADDLE_WIDTH, PADDLE_HEIGHT)
        right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                              2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

        left_score = 0
        right_score = 0

        while run:
            WIN.fill(BLACK)
            clock.tick(FPS)
            draw(WIN, (left_paddle, right_paddle), ball, left_score, right_score)
            # WIN.blit(background,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            handle_paddle_movement(keys, left_paddle, right_paddle)

            ball.move()
            handle_collision(ball, left_paddle, right_paddle)

            if ball.x < 0:
                right_score += 1
                ball.reset()
            elif ball.x > WIDTH:
                left_score += 1
                ball.reset()

            won = False
            if left_score >= WINNING_SCORE:
                won = True
                win_text = "Left Player Won!"
            elif right_score >= WINNING_SCORE:
                won = True
                win_text = "Right Player Won!"

            if won:
                text = SCORE_FONT.render(win_text, 1, WHITE)
                WIN.blit(text, (WIDTH // 2 - text.get_width() //
                                2, HEIGHT // 2 - text.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(5000)
                ball.reset()
                left_paddle.reset()
                right_paddle.reset()
                left_score = 0
                right_score = 0
                break

        pygame.quit()


    if __name__ == '__main__':
        main()