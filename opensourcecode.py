import pygame
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init()
WIDTH = 1717
HEIGHT = 916
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("ersiejump")

bg = pygame.image.load(
    resource_path("platformer/assets/bg/bg.png")
).convert()

player_img = pygame.image.load(
    resource_path("platformer/assets/idle anim/tile000.png")
).convert_alpha()

icon = pygame.image.load(
    resource_path("platformer/assets/icon/rat.png")
).convert_alpha()

player_img = pygame.transform.scale(player_img, (200, 200))

bg_sound = pygame.mixer.Sound(
    resource_path("platformer/assets/music/music.mp3")
)
pygame.display.set_icon(icon)

player = pygame.Rect(
    140, 710, 60, 90
)

enemy = pygame.Rect(
    WIDTH + 300,
    630,
    60,
    90
)

idle_frames = []

for i in range(10):
    frame = pygame.image.load(
        resource_path(
            f"platformer/assets/idle anim/tile{i:03}.png"
        )
    ).convert_alpha()


    frame = pygame.transform.scale(frame, (200, 200))
    idle_frames.append(frame)

run_frames = []

for i in range(10):
    frame = pygame.image.load(
        resource_path(
            f"platformer/assets/run anim/run{i + 1:03}.png"
        )
    ).convert_alpha()
    frame = pygame.transform.scale(frame, (200, 200))
    run_frames.append(frame)

jump_frames = []

for i in range(3):
    frame = pygame.image.load(
        resource_path(
            f"platformer/assets/jump anim/tile{i:03}.png"
        )
    ).convert_alpha()
    frame = pygame.transform.scale(frame, (200, 200))
    jump_frames.append(frame)

enemy_frames = []

for i in range(4):
    frame = pygame.image.load(
        resource_path(
            f"platformer/assets/enemy/FLYING_{i + 1 :03}.png"
        )
    ).convert_alpha()
    frame = pygame.transform.scale(frame, (130, 130))
    enemy_frames.append(frame)

best_score = 0

def main_menu():
    bg_sound.stop()
    font = pygame.font.SysFont(None, 60)
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    running = True
    while running:


        start = font.render("JUMP FOR START", True, (255, 255, 255))
        screen.blit(start, (650, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play()
                    return

        pygame.display.flip()
        clock.tick(60)


def play():
    global best_score
    frame_index = 0
    animation_speed = 0.15
    player_speed = 6
    running = True
    facing_right = True
    velocity_y = 0
    gravity = 0.8
    jump_power = -18
    ground_y = 650
    is_grounded = True
    last_animation = None
    score = 0
    font = pygame.font.SysFont(None, 60)

    enemy_speed = 8
    enemy_frame_index = 0
    enemy_animation_speed = 0.2
    game_over = False

    bg_sound.play(-1)
    bg_sound.set_volume(0.100)

    while running:
        if game_over:
            bg_sound.stop()
            dark = pygame.Surface((WIDTH, HEIGHT))
            dark.set_alpha(50)
            dark.fill((0, 0, 0))
            screen.blit(dark, (0, 0))

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

            screen.blit(bg, (0, 0))
            screen.blit(game_over_text, (700, 300))
            screen.blit(restart_text, (650, 350))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]:
                bg_sound.play(-1)
                player.x = 140
                player.y = 710

                enemy.x = WIDTH + 300

                velocity_y = 0
                is_grounded = True

                score = 0
                enemy_speed = 8
                game_over = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)

            continue
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        dark = pygame.Surface((WIDTH, HEIGHT))
        dark.set_alpha(50)
        dark.fill((0, 0, 0))
        screen.blit(dark, (0, 0))

        player_hitbox = pygame.Rect(
            player.x + 70,
            player.y + 70,
            60,
            70
        )

        enemy_hitbox = pygame.Rect(
            enemy.x + 5,
            enemy.y + 20,
            60,
            80
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

        current_frame = current_frames[int(frame_index)]
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
            enemy_frames[int(enemy_frame_index)],
            (enemy.x, enemy.y)
        )

        if player_hitbox.colliderect(enemy_hitbox):
            if score > best_score:
                best_score = score
            game_over = True

        if enemy.right < 0:
           enemy.x = WIDTH + 300
           score += 10
           enemy_speed += 0.10

        score_text = font.render(
            f"SCORE: {score}",
            True,
            (255, 255, 255)
        )

        screen.blit(score_text, (20, 20))

        back_text = font.render(
            "RETURN MENU ESCAPE",
            True,
            (255, 255, 255)
        )

        screen.blit(back_text, (20, 140))

        mute_text = font.render(
            "MUTE MUSIC TAB",
            True,
            (255, 255, 255)
        )


        screen.blit(mute_text, (20, 100))

        best_score_text = font.render(
            f"BEST SCORE: {best_score}",
            True,
            (255, 255, 255)
        )

        screen.blit(best_score_text, (20, 60))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if score > best_score:
                        best_score = score
                    player.x = 140
                    player.y = 710

                    enemy.x = WIDTH + 300
                    bg_sound.set_volume(0.0100)
                    main_menu()
                    return
                if event.key == pygame.K_TAB:
                    bg_sound.stop()

        pygame.display.flip()
        clock.tick(60)


def reset_game():
    player.x = 140
    player.y = 710

    enemy.x = WIDTH + 300

    return 0, False

if __name__ == "__main__":
    main_menu()
