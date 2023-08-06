from os import path

import pygame as pg
import math

# GLOBALS #

# SIZE
PIXEL_SIZE = 10
BALL_STEP = PIXEL_SIZE * 2
PAD_STEP = PIXEL_SIZE
BALL_SIZE = (2 * PIXEL_SIZE, 2 * PIXEL_SIZE)
PAD_SIZE = (2 * PIXEL_SIZE, 16 * PIXEL_SIZE)
SCREEN_SIZE = (1600, 900)
SCORE_IMAGE_SIZE = (64, 64)

# COORDINATES
PAD_START_Y = SCREEN_SIZE[1] / 2 - PAD_SIZE[1] / 2
PAD_X_OFFSET = 6 * PIXEL_SIZE
LEFT_PAD_X = PAD_X_OFFSET
RIGHT_PAD_X = SCREEN_SIZE[0] - PAD_X_OFFSET - PAD_SIZE[0]
BALL_START = (SCREEN_SIZE[0] / 2 - BALL_SIZE[0] / 2,
              SCREEN_SIZE[1] / 2 - BALL_SIZE[1] / 2)
SCREEN_CORNER = (0, 0)
LEFT_SCORE_CORNER = ((SCREEN_SIZE[0] / 2) - 1.5 * SCORE_IMAGE_SIZE[0], SCREEN_SIZE[1] / 10)
COLON_CORNER = ((SCREEN_SIZE[0] / 2) - 0.5 * SCORE_IMAGE_SIZE[0], SCREEN_SIZE[1] / 10)
RIGHT_SCORE_CORNER = ((SCREEN_SIZE[0] / 2) + 0.5 * SCORE_IMAGE_SIZE[0], SCREEN_SIZE[1] / 10)
RIGHT_TEXT_LOCATION = (SCREEN_SIZE[0] * 0.8, SCREEN_SIZE[1] / 3)
LEFT_TEXT_LOCATION = (SCREEN_SIZE[0] * 0.2, SCREEN_SIZE[1] / 3)
PAUSE_TEXT_LOCATION = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 4)
WIN_TEXT_LOCATION = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 3)

# COLORS
LEFT_PAD_COLOR = (0, 255, 64)
RIGHT_PAD_COLOR = (255, 64, 0)
BALL_COLOR = (255, 255, 255)
RIGHT_WIN_COLOR = (255, 0, 0)
LEFT_WIN_COLOR = (0, 255, 0)
BLACK_COLOR = (0, 0, 0)

# KEYS
LEFT_PAD_UP = pg.K_w
LEFT_PAD_DOWN = pg.K_s
RIGHT_PAD_UP = pg.K_UP
RIGHT_PAD_DOWN = pg.K_DOWN
PAUSE = pg.K_SPACE
EXIT = pg.K_ESCAPE

# TIMING
FPS = 120
BALL_SPEED = FPS / 2.0
RIGHT_PAD_SPEED = FPS / 2.0
LEFT_PAD_SPEED = FPS / 2.0
BALL_COUNTER_MAX = FPS / BALL_SPEED
RIGHT_PAD_COUNTER_MAX = FPS / RIGHT_PAD_SPEED
LEFT_PAD_COUNTER_MAX = FPS / LEFT_PAD_SPEED

# DIRECTIONS
EPSILON = 0.01
RIGHT_UPPER_LIMIT = math.pi * 4 / 12
RIGHT_LOWER_LIMIT = math.pi * -4 / 12
LEFT_UPPER_LIMIT = math.pi * 8 / 12
LEFT_LOWER_LIMIT = math.pi * 16 / 12
RIGHT_DIRECTION = 0
LEFT_DIRECTION = math.pi

# IMAGES
ZERO = path.join("sprites", "0.png")
ONE = path.join("sprites", "1.png")
TWO = path.join("sprites", "2.png")
THREE = path.join("sprites", "3.png")
COLON = path.join("sprites", "colon.png")

# SOUNDS
RIGHT_PAD_SOUND = path.join("sfx", "ting.wav")
LEFT_PAD_SOUND = path.join("sfx", "tong.wav")

# TEXT
SANS = path.join("fonts", "comic.ttf")
WIN_FONT_SIZE = 69
INSTRUCTIONS_FONT_SIZE = 32
LEFT_WIN_TEXT = "left pad wins!"
RIGHT_WIN_TEXT = "right pad wins!"
LEFT_INSTRUCTIONS = "left pad:\nW - go up\nS - go down\nSPACE - pause/start\nESC - exit"
RIGHT_INSTRUCTIONS = "right pad:\nUP - go up\nDOWN - go down\nSPACE - pause/start\nESC - exit"
PAUSE_TEXT = "    game paused.\npress space to continue"

# ETC
MAX_SCORE = 3


def draw_pad(screen, corner, rl):
    rectangle = pg.Rect(*corner, *PAD_SIZE)
    if rl == "right":
        pg.draw.rect(screen, RIGHT_PAD_COLOR, rectangle)
    else:
        pg.draw.rect(screen, LEFT_PAD_COLOR, rectangle)


def draw_ball(screen, corner):
    rectangle = pg.Rect(*corner, *BALL_SIZE)
    pg.draw.rect(screen, BALL_COLOR, rectangle)


def get_next_ball_corner(state_dict):
    next_ball_x = state_dict["ball_corner"][0] + (math.cos(state_dict["ball_radians"]) * BALL_STEP)
    next_ball_y = state_dict["ball_corner"][1] - (math.sin(state_dict["ball_radians"]) * BALL_STEP)

    return next_ball_x, next_ball_y


def draw_score(state_dict, image_dict, screen):
    left = state_dict["left_score"]
    right = state_dict["right_score"]
    assert (left in image_dict and right in image_dict), "bad input to draw_score"

    screen.blit(image_dict[left], LEFT_SCORE_CORNER)
    screen.blit(image_dict["colon"], COLON_CORNER)
    screen.blit(image_dict[right], RIGHT_SCORE_CORNER)


def start_game(screen, image_dict):
    # init dict with defaults
    state_dict = {"done": False,
                  "paused": True,
                  "game_over": False,
                  "left_pad_corner": [LEFT_PAD_X, PAD_START_Y],
                  "right_pad_corner": [RIGHT_PAD_X, PAD_START_Y],
                  "ball_corner": BALL_START,
                  "ball_counter": 0,
                  "right_pad_counter": 0,
                  "left_pad_counter": 0,
                  "ball_moved": False,
                  "right_pad_moved": False,
                  "left_pad_moved": False,
                  "ball_radians": RIGHT_DIRECTION,
                  "ball_goes_right": True,
                  "left_score": 0,
                  "right_score": 0, }

    # draw defaults
    render_screen(screen, state_dict, image_dict)
    draw_pause(image_dict, screen)
    pg.display.flip()

    return state_dict


def tick_game(state_dict, sound_dict):
    pressed = pg.key.get_pressed()

    tick_counters(state_dict)
    move_ball(state_dict, sound_dict)
    move_pads(pressed, state_dict)

    return state_dict


def move_ball(state_dict, sound_dict):
    current_ball_corner = state_dict["ball_corner"]
    next_ball_corner = get_next_ball_corner(state_dict)
    right_pad = state_dict["right_pad_corner"]
    left_pad = state_dict["left_pad_corner"]

    # ball touches right pad
    if (state_dict["right_pad_corner"][0] + PAD_SIZE[0] > next_ball_corner[0] + BALL_SIZE[0] - EPSILON >
            state_dict["right_pad_corner"][0]
            and right_pad[1] - BALL_SIZE[1] < current_ball_corner[1] < right_pad[1] + PAD_SIZE[1]):
        sound_dict["right_pad"].play()
        ball_location_on_pad_percentage = ((current_ball_corner[1] + BALL_SIZE[1] / 2) - right_pad[1]) / float(
            (PAD_SIZE[1]))
        if ball_location_on_pad_percentage < 0:
            new_ball_direction = LEFT_UPPER_LIMIT
        elif ball_location_on_pad_percentage > 1:
            new_ball_direction = LEFT_LOWER_LIMIT
        else:
            new_ball_direction = LEFT_UPPER_LIMIT + ball_location_on_pad_percentage * (
                    LEFT_LOWER_LIMIT - LEFT_UPPER_LIMIT)
        state_dict["ball_radians"] = new_ball_direction

    # ball touches left pad
    elif (state_dict["left_pad_corner"][0] < next_ball_corner[0] + EPSILON < state_dict["left_pad_corner"][0] +
          PAD_SIZE[0]
          and left_pad[1] - BALL_SIZE[1] < current_ball_corner[1] < left_pad[1] + PAD_SIZE[1]):
        sound_dict["left_pad"].play()
        ball_location_on_pad_percentage = ((current_ball_corner[1] + BALL_SIZE[1] / 2) - left_pad[1]) / float(
            (PAD_SIZE[1]))
        if ball_location_on_pad_percentage < 0:
            new_ball_direction = RIGHT_UPPER_LIMIT
        elif ball_location_on_pad_percentage > 1:
            new_ball_direction = RIGHT_LOWER_LIMIT
        else:
            new_ball_direction = RIGHT_UPPER_LIMIT + ball_location_on_pad_percentage * (
                    RIGHT_LOWER_LIMIT - RIGHT_UPPER_LIMIT)
        state_dict["ball_radians"] = new_ball_direction

    # ball touches top or bottom edge
    if next_ball_corner[1] < 0 or next_ball_corner[1] + BALL_SIZE[1] > SCREEN_SIZE[1]:
        state_dict["ball_radians"] = -state_dict["ball_radians"]

    # ball touches right edge
    if next_ball_corner[0] + BALL_SIZE[0] < 0:
        state_dict["right_score"] += 1
        if state_dict["right_score"] < MAX_SCORE:
            state_dict["ball_corner"] = BALL_START
            state_dict["ball_radians"] = RIGHT_DIRECTION

    # ball touches left edge
    elif next_ball_corner[0] > SCREEN_SIZE[0]:
        state_dict["left_score"] += 1
        if state_dict["left_score"] < MAX_SCORE:
            state_dict["ball_corner"] = BALL_START
            state_dict["ball_radians"] = LEFT_DIRECTION

    # move ball
    if not state_dict["ball_moved"]:
        state_dict["ball_moved"] = True
        state_dict["ball_corner"] = get_next_ball_corner(state_dict)

    return state_dict


def move_pads(pressed, state_dict):
    # right pad
    if (pressed[RIGHT_PAD_UP] and state_dict["right_pad_corner"][1] > 0
            and not state_dict["right_pad_moved"]):
        state_dict["right_pad_corner"][1] -= PAD_STEP
        state_dict["right_pad_moved"] = True
    if (pressed[RIGHT_PAD_DOWN] and state_dict["right_pad_corner"][1] < (SCREEN_SIZE[1] - PAD_SIZE[1])
            and not state_dict["right_pad_moved"]):
        state_dict["right_pad_corner"][1] += PAD_STEP
        state_dict["right_pad_moved"] = True
    # left pad
    if (pressed[LEFT_PAD_UP] and state_dict["left_pad_corner"][1] > 0
            and not state_dict["left_pad_moved"]):
        state_dict["left_pad_corner"][1] -= PAD_STEP
        state_dict["left_pad_moved"] = True
    if (pressed[LEFT_PAD_DOWN] and state_dict["left_pad_corner"][1] < (SCREEN_SIZE[1] - PAD_SIZE[1])
            and not state_dict["left_pad_moved"]):
        state_dict["left_pad_corner"][1] += PAD_STEP
        state_dict["left_pad_moved"] = True

    return state_dict


def tick_counters(state_dict):
    state_dict["ball_counter"] = (state_dict["ball_counter"] + 1) % BALL_COUNTER_MAX
    state_dict["right_pad_counter"] = (state_dict["right_pad_counter"] + 1) % RIGHT_PAD_COUNTER_MAX
    state_dict["left_pad_counter"] = (state_dict["left_pad_counter"] + 1) % LEFT_PAD_COUNTER_MAX
    if not state_dict["ball_counter"]:
        state_dict["ball_moved"] = False
    if not state_dict["right_pad_counter"]:
        state_dict["right_pad_moved"] = False
    if not state_dict["left_pad_counter"]:
        state_dict["left_pad_moved"] = False

    return state_dict


def empty_screen(screen):
    rectangle = pg.Rect(*SCREEN_CORNER, *SCREEN_SIZE)
    pg.draw.rect(screen, BLACK_COLOR, rectangle)


def render_screen(screen, state_dict, image_dict):
    empty_screen(screen)
    draw_pad(screen, state_dict["right_pad_corner"], "right")
    draw_pad(screen, state_dict["left_pad_corner"], "left")
    draw_ball(screen, state_dict["ball_corner"])
    draw_score(state_dict, image_dict, screen)


def check_exit(state_dict, events):
    for event in events:
        if event.type == pg.QUIT:
            state_dict["done"] = True

    mod_bits = pg.key.get_mods()
    pressed = pg.key.get_pressed()

    if (mod_bits & pg.KMOD_ALT and pressed[pg.K_F4]) or pressed[pg.K_ESCAPE]:
        state_dict["done"] = True


def get_images():
    big_sans = pg.font.Font(SANS, WIN_FONT_SIZE)
    small_sans = pg.font.Font(SANS, INSTRUCTIONS_FONT_SIZE)

    left_wins_text = [big_sans.render(LEFT_WIN_TEXT, True, LEFT_WIN_COLOR)]
    right_wins_text = [big_sans.render(RIGHT_WIN_TEXT, True, RIGHT_WIN_COLOR)]

    left_instructions_texts = []
    for t in LEFT_INSTRUCTIONS.splitlines():
        left_instructions_texts.append(small_sans.render(t, True, LEFT_WIN_COLOR))

    right_instructions_texts = []
    for t in RIGHT_INSTRUCTIONS.splitlines():
        right_instructions_texts.append(small_sans.render(t, True, RIGHT_WIN_COLOR))

    pause_texts = []
    for t in PAUSE_TEXT.splitlines():
        pause_texts.append(small_sans.render(t, True, BALL_COLOR))

    d = {0: pg.image.load(ZERO), 1: pg.image.load(ONE), 2: pg.image.load(TWO),
         3: pg.image.load(THREE), "colon": pg.image.load(COLON), "left win": left_wins_text,
         "right win": right_wins_text, "left instructions": left_instructions_texts,
         "right instructions": right_instructions_texts, "pause": pause_texts}

    return d


def blit_text(screen, images, location_above):
    assert len(images) > 0, "bad input to blit_text"

    height = images[0].get_height()
    max_width = max(i.get_width() for i in images)
    corner = (location_above[0] - max_width/2, location_above[1])

    for i, text in enumerate(images):
        my_corner = (corner[0], corner[1] + i * height)
        screen.blit(text, my_corner)


def draw_pause(image_dict, screen):
    blit_text(screen, image_dict["right instructions"], RIGHT_TEXT_LOCATION)
    blit_text(screen, image_dict["left instructions"], LEFT_TEXT_LOCATION)
    blit_text(screen, image_dict["pause"], PAUSE_TEXT_LOCATION)


def check_pause(state_dict, events, screen, image_dict):
    for event in events:
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            state_dict["paused"] = not state_dict["paused"]
            draw_pause(image_dict, screen)
            pg.display.flip()

            if state_dict["game_over"]:
                # reset game after game over
                state_dict = start_game(screen, image_dict)
    return state_dict


def check_winner(state_dict, screen, image_dict):
    if state_dict["left_score"] == MAX_SCORE:
        state_dict["paused"] = state_dict["game_over"] = True
        blit_text(screen, image_dict["left win"], WIN_TEXT_LOCATION)
        pg.display.flip()

    elif state_dict["right_score"] == MAX_SCORE:
        state_dict["paused"] = state_dict["game_over"] = True
        blit_text(screen, image_dict["right win"], WIN_TEXT_LOCATION)
        pg.display.flip()


def get_sounds():
    d = {"left_pad": pg.mixer.Sound(LEFT_PAD_SOUND),
         "right_pad": pg.mixer.Sound(RIGHT_PAD_SOUND), }
    return d


def main():
    """
    play the nong game.
    :return:
    """

    pg.mixer.pre_init(22050, -16, 2, 1024)  # no idea why this works
    pg.init()
    pg.display.set_caption("nong")
    pg.mixer.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode(SCREEN_SIZE)
    image_dict = get_images()
    sound_dict = get_sounds()
    state_dict = start_game(screen, image_dict)

    while not state_dict["done"]:
        # event stuff
        events = pg.event.get()
        check_exit(state_dict, events)
        state_dict = check_pause(state_dict, events, screen, image_dict)
        check_winner(state_dict, screen, image_dict)

        # update state
        clock.tick(FPS)
        if not state_dict["paused"]:
            tick_game(state_dict, sound_dict)
            render_screen(screen, state_dict, image_dict)
            pg.display.flip()

    print("goodbye")


if __name__ == "__main__":
    main()
