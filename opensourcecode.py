import pygame
import sys
import random


pygame.init()
pygame.mixer.init()

WIDTH = 1717
HEIGHT = 916
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("ersiejump")


scene = "menu"

best_score = 0


player = pygame.Rect(
    140,
    710,
    60,
    90
)

enemy = pygame.Rect(
    WIDTH + 300,
    630,
    60,
    90
)

flying_imp = pygame.Rect(
    WIDTH + 300,
    630,
    60,
    90
)


backgrounds = [
    pygame.image.load(
        "assets/bg/bg.png"
    ).convert(),

    pygame.image.load(
        "assets/bg/forestbg.png"
    ).convert()
]


music = [
    pygame.mixer.Sound(
        "assets/music/music.mp3"
    ),

    pygame.mixer.Sound(
        "assets/music/forest.mp3"
    )
]


player_img = pygame.image.load(
    "assets/idle anim/tile000.png"
).convert_alpha()

icon = pygame.image.load(
    "assets/icon/rat.png"
).convert_alpha()

player_img = pygame.transform.scale(
    player_img,
    (200, 200)
)

pygame.display.set_icon(icon)


idle_frames = []

for i in range(10):
    frame = pygame.image.load(
        f"assets/idle anim/tile{i:03}.png"
    ).convert_alpha()

    frame = pygame.transform.scale(
        frame,
        (200, 200)
    )

    idle_frames.append(frame)


run_frames = []

for i in range(10):
    frame = pygame.image.load(
        f"assets/run anim/run{i + 1:03}.png"
    ).convert_alpha()

    frame = pygame.transform.scale(
        frame,
        (200, 200)
    )

    run_frames.append(frame)


jump_frames = []

for i in range(3):
    frame = pygame.image.load(
        f"assets/jump anim/tile{i:03}.png"
    ).convert_alpha()

    frame = pygame.transform.scale(
        frame,
        (200, 200)
    )

    jump_frames.append(frame)


enemy_frames = []

for i in range(4):
    frame = pygame.image.load(
        f"assets/enemy/FLYING_{i + 1:03}.png"
    ).convert_alpha()

    frame = pygame.transform.scale(
        frame,
        (130, 130)
    )

    enemy_frames.append(frame)


new_enemy_frames = []

for i in range(8):
    frame = pygame.image.load(
        f"assets/new_enemy/Enemy3-Fly_{i + 1:02}.png"
    ).convert_alpha()

    frame = pygame.transform.scale(
        frame,
        (130, 130)
    )

    new_enemy_frames.append(frame)


font = pygame.font.SysFont(
    None,
    60
)


frame_index = 0
last_animation = None

velocity_y = 0
is_grounded = True

score = 0

enemy_speed = 8
enemy_frame_index = 0

flying_imp_speed = 8
flying_imp_frame_index = 0

facing_right = True

game_over = False


def reset_game():
    global frame_index
    global last_animation
    global velocity_y
    global is_grounded
    global score
    global enemy_speed
    global enemy_frame_index
    global flying_imp_speed
    global flying_imp_frame_index
    global facing_right
    global game_over

    player.x = 140
    player.y = 710

    enemy.x = WIDTH + 300
    enemy.y = 630

    flying_imp.x = WIDTH + 300
    flying_imp.y = 630

    frame_index = 0
    last_animation = None

    velocity_y = 0
    is_grounded = True

    score = 0

    enemy_speed = 8
    enemy_frame_index = 0

    flying_imp_speed = 8
    flying_imp_frame_index = 0

    facing_right = True

    game_over = False

    enemy.x = WIDTH + random.randint(
        500,
        1000
    )

    enemy.y = random.choice([
        550,
        630,
        500
    ])

    flying_imp.x = WIDTH + random.randint(
        500,
        1000
    )

    flying_imp.y = random.choice([
        500,
        550,
        630
    ])


def main_menu():
    music[0].stop()
    music[1].stop()

    screen.fill(
        (0, 0, 0)
    )

    screen.blit(
        backgrounds[0],
        (0, 0)
    )

    start = font.render(
        "JUMP FOR START",
        True,
        (255, 255, 255)
    )

    screen.blit(
        start,
        (650, 400)
    )


def first_world():
    global frame_index
    global last_animation
    global velocity_y
    global is_grounded
    global score
    global enemy_speed
    global enemy_frame_index
    global game_over
    global facing_right
    global best_score

    animation_speed = 0.15
    player_speed = 6

    gravity = 0.8
    jump_power = -18
    ground_y = 650

    enemy_animation_speed = 0.2

    screen.fill(
        (0, 0, 0)
    )

    screen.blit(
        backgrounds[0],
        (0, 0)
    )

    dark = pygame.Surface(
        (WIDTH, HEIGHT)
    )

    dark.set_alpha(50)
    dark.fill(
        (0, 0, 0)
    )

    screen.blit(
        dark,
        (0, 0)
    )

    player_hitbox = pygame.Rect(
        player.x + 70,
        player.y + 70,
        60,
        70
    )

    enemy_hitbox = pygame.Rect(
        enemy.x + 20,
        enemy.y + 40,
        50,
        60
    )

    moving = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player.x -= player_speed
        moving = True
        facing_right = False

    if keys[pygame.K_d]:
        player.x += player_speed
        moving = True
        facing_right = True

    if keys[pygame.K_SPACE] and is_grounded:
        velocity_y = jump_power
        is_grounded = False

    velocity_y += gravity
    player.y += velocity_y

    if player.y >= ground_y:
        player.y = ground_y
        velocity_y = 0
        is_grounded = True

    if not is_grounded:
        current_frames = jump_frames

    elif moving:
        current_frames = run_frames

    else:
        current_frames = idle_frames

    if current_frames != last_animation:
        frame_index = 0
        last_animation = current_frames

    if frame_index >= len(current_frames):
        frame_index = 0

    current_frame = current_frames[
        int(frame_index)
    ]

    if not facing_right:
        current_frame = pygame.transform.flip(
            current_frame,
            True,
            False
        )

    screen.blit(
        current_frame,
        (player.x, player.y)
    )

    if player.left < 0:
        player.left = 0

    if player.right > WIDTH:
        player.right = WIDTH

    frame_index += animation_speed

    if not is_grounded:
        if frame_index >= len(jump_frames):
            frame_index = len(jump_frames) - 1

    else:
        if frame_index >= len(current_frames):
            frame_index = 0

    enemy.x -= enemy_speed

    enemy_frame_index += enemy_animation_speed

    if enemy_frame_index >= len(enemy_frames):
        enemy_frame_index = 0

    screen.blit(
        enemy_frames[
            int(enemy_frame_index)
        ],
        (enemy.x, enemy.y)
    )

    if player_hitbox.colliderect(
        enemy_hitbox
    ):
        if score > best_score:
            best_score = score

        game_over = True

    if enemy.right < 0:
        enemy.x = WIDTH + random.randint(
            500,
            1000
        )

        enemy.y = random.choice([
            550,
            630,
            500
        ])

        score += 10
        enemy_speed += 0.20

    score_text = font.render(
        f"SCORE: {score}",
        True,
        (255, 255, 255)
    )

    best_score_text = font.render(
        f"BEST SCORE: {best_score}",
        True,
        (255, 255, 255, 255)
    )

    mute_text = font.render(
        "MUTE MUSIC TAB",
        True,
        (255, 255, 255)
    )

    back_text = font.render(
        "RETURN MENU ESCAPE",
        True,
        (255, 255, 255)
    )

    screen.blit(
        score_text,
        (20, 20)
    )

    screen.blit(
        best_score_text,
        (20, 60)
    )

    screen.blit(
        mute_text,
        (20, 100)
    )

    screen.blit(
        back_text,
        (20, 140)
    )


def second_world():
    global frame_index
    global last_animation
    global velocity_y
    global is_grounded
    global score
    global flying_imp_speed
    global flying_imp_frame_index
    global game_over
    global facing_right
    global best_score

    animation_speed = 0.15
    player_speed = 6

    gravity = 0.8
    jump_power = -18
    ground_y = 650

    enemy_animation_speed = 0.2

    screen.fill(
        (0, 0, 0)
    )

    screen.blit(
        backgrounds[1],
        (0, 0)
    )

    dark = pygame.Surface(
        (WIDTH, HEIGHT)
    )

    dark.set_alpha(50)
    dark.fill(
        (0, 0, 0)
    )

    screen.blit(
        dark,
        (0, 0)
    )

    player_hitbox = pygame.Rect(
        player.x + 70,
        player.y + 70,
        60,
        70
    )

    flying_imp_hitbox = pygame.Rect(
        flying_imp.x + 20,
        flying_imp.y + 40,
        50,
        60
    )

    moving = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player.x -= player_speed
        moving = True
        facing_right = False

    if keys[pygame.K_d]:
        player.x += player_speed
        moving = True
        facing_right = True

    if keys[pygame.K_SPACE] and is_grounded:
        velocity_y = jump_power
        is_grounded = False

    velocity_y += gravity
    player.y += velocity_y

    if player.y >= ground_y:
        player.y = ground_y
        velocity_y = 0
        is_grounded = True

    if not is_grounded:
        current_frames = jump_frames

    elif moving:
        current_frames = run_frames

    else:
        current_frames = idle_frames

    if current_frames != last_animation:
        frame_index = 0
        last_animation = current_frames

    if frame_index >= len(current_frames):
        frame_index = 0

    current_frame = current_frames[
        int(frame_index)
    ]

    if not facing_right:
        current_frame = pygame.transform.flip(
            current_frame,
            True,
            False
        )

    screen.blit(
        current_frame,
        (player.x, player.y)
    )

    if player.left < 0:
        player.left = 0

    if player.right > WIDTH:
        player.right = WIDTH

    frame_index += animation_speed

    if not is_grounded:
        if frame_index >= len(jump_frames):
            frame_index = len(jump_frames) - 1

    else:
        if frame_index >= len(current_frames):
            frame_index = 0

    flying_imp.x -= flying_imp_speed

    flying_imp_frame_index += enemy_animation_speed

    if flying_imp_frame_index >= len(new_enemy_frames):
        flying_imp_frame_index = 0

    screen.blit(
        new_enemy_frames[
            int(flying_imp_frame_index)
        ],
        (flying_imp.x, flying_imp.y)
    )

    if player_hitbox.colliderect(
        flying_imp_hitbox
    ):
        if score > best_score:
            best_score = score

        game_over = True

    if flying_imp.right < 0:
        flying_imp.x = WIDTH + random.randint(
            500,
            1000
        )

        flying_imp.y = random.choice([
            500,
            550,
            630
        ])

        score += 10
        flying_imp_speed += 0.20

    score_text = font.render(
        f"SCORE: {score}",
        True,
        (255, 255, 255)
    )

    best_score_text = font.render(
        f"BEST SCORE: {best_score}",
        True,
        (255, 255, 255)
    )

    mute_text = font.render(
        "MUTE MUSIC TAB",
        True,
        (255, 255, 255)
    )

    back_text = font.render(
        "RETURN MENU ESCAPE",
        True,
        (255, 255, 255)
    )

    screen.blit(
        score_text,
        (20, 20)
    )

    screen.blit(
        best_score_text,
        (20, 60)
    )

    screen.blit(
        mute_text,
        (20, 100)
    )

    screen.blit(
        back_text,
        (20, 140)
    )


def game_over_screen():
    screen.fill(
        (0, 0, 0)
    )

    screen.blit(
        backgrounds[0],
        (0, 0)
    )

    dark = pygame.Surface(
        (WIDTH, HEIGHT)
    )

    dark.set_alpha(50)
    dark.fill(
        (0, 0, 0)
    )

    screen.blit(
        dark,
        (0, 0)
    )

    game_over_text = font.render(
        "GAME OVER",
        True,
        (255, 0, 0)
    )

    restart_text = font.render(
        "Press R to Restart",
        True,
        (255, 255, 255)
    )

    screen.blit(
        game_over_text,
        (700, 300)
    )

    screen.blit(
        restart_text,
        (650, 350)
    )


running = True


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if scene == "menu":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    reset_game()

                    music[0].play(-1)
                    music[0].set_volume(0.300)

                    scene = "first_world"

        elif scene == "first_world":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    if score > best_score:
                        best_score = score

                    player.x = 140
                    player.y = 710

                    enemy.x = WIDTH + 300

                    music[0].stop()

                    scene = "menu"

                elif event.key == pygame.K_TAB:

                    music[0].stop()

        elif scene == "second_world":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    if score > best_score:
                        best_score = score

                    player.x = 140
                    player.y = 710

                    flying_imp.x = WIDTH + 300

                    music[1].stop()

                    scene = "menu"

                elif event.key == pygame.K_TAB:

                    music[1].stop()

        elif scene == "game_over":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:

                    music[1].stop()
                    music[0].play(-1)
                    music[0].set_volume(0.300)

                    reset_game()

                    scene = "first_world"


    if scene == "menu":

        main_menu()


    elif scene == "first_world":

        if game_over:

            music[0].stop()
            scene = "game_over"

        else:

            first_world()

            if score >= 100:

                score = 0

                music[0].stop()

                flying_imp.x = WIDTH + random.randint(
                    500,
                    1000
                )

                flying_imp.y = random.choice([
                    500,
                    550,
                    630
                ])

                flying_imp_speed = 8
                flying_imp_frame_index = 0

                music[1].play(-1)
                music[1].set_volume(0.300)

                scene = "second_world"


    elif scene == "second_world":

        if game_over:

            music[1].stop()
            scene = "game_over"

        else:

            second_world()


    elif scene == "game_over":

        game_over_screen()


    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
sys.exit()
