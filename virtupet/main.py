# This is the main file for running the project

# lets just create a pudgi and see if it fails

import pygame
import constants
import environments
from file_handler import JSONHandler
from pudgi import Pudgi


def main():

    handler = JSONHandler()
    handler.load_file(constants.BLUEPUDGI)
    json_object = handler.get_data()

    # ----------- pygame objects -----------
    pygame.init()

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption(json_object["name"])

    agent = Pudgi()

    env_list = [environments.EnvironmentHouse(agent)]

    current_env_no = 0
    current_env = env_list[current_env_no]

    active_sprite_list = pygame.sprite.Group()
    agent.env = current_env

    agent.rect.x = 340
    agent.rect.y = constants.SCREEN_HEIGHT - 140
    active_sprite_list.add(agent)

    done = False

    clock = pygame.time.Clock()

    # ----------- JSON objects ------------
    # handler.load_file("./data/metadata.json")
    # data = handler.get_data()
    # number = "001"
    # node = data["root"]
    # for char in number:
    #     node = node[char]

    # --------------Main While loop---------------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    agent.go_left()
                if event.key == pygame.K_RIGHT:
                    agent.go_right()
                # if event.key == pygame.K_UP:
                #     agent.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and agent.change_x < 0:
                    agent.stop()
                if event.key == pygame.K_RIGHT and agent.change_x > 0:
                    agent.stop()

        active_sprite_list.update()

        current_env.update()

        current_env.draw(screen)
        active_sprite_list.draw(screen)

        clock.tick(30)

        # print(clock.get_fps())

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
