# This is the main file for running the project

# lets just create a pudgi and see if it fails

import pygame
import constants
import levels
from file_handler import JSONHandler
from pudgi import Pudgi


def main():
    # ----------- pygame objects -----------
    pygame.init()

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Blue Pudgi")

    player = Pudgi()

    level_list = [levels.LevelHouse(player)]

    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    done = False

    clock = pygame.time.Clock()

    # ----------- JSON objects ------------
    # handler = JSONHandler()
    # handler.load_file('./data/decisions.json')
    # data = handler.get_data()
    # print(data)

    # --------------Main While loop---------------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                # if event.key == pygame.K_UP:
                #     player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        active_sprite_list.update()

        current_level.update()

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        clock.tick(30)

        # print(clock.get_fps())

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
