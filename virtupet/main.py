# This is the main file for running the project

# lets just create a pudgi and see if it fails

import pygame
import constants
import environments
from file_handler import JSONHandler
from clock import Clock
from pudgi import Pudgi


def main():
    handler = JSONHandler()
    handler.load_file(constants.DEFAULT_PUDGI)
    json_object = handler.get_data()

    time_clock = Clock()

    # ----------- pygame objects -----------
    pygame.init()

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption(json_object["name"])

    active_agent_list = []
    # parents = ["0x9c08", "0x11e66"]
    # agent = Pudgi(parents)
    # agent = Pudgi(None, "./data/pudgies/0x9c08.json")
    agent = Pudgi()
    agent2 = Pudgi()
    active_agent_list.append(agent)
    agent.export_to_json()
    active_agent_list.append(agent2)
    agent2.export_to_json()
    env_list = [environments.EnvironmentHouse(agent)]

    current_env_no = 0
    current_env = env_list[current_env_no]

    active_sprite_list = pygame.sprite.Group()
    agent.env = current_env

    agent.rect.x = 340
    agent.rect.y = constants.SCREEN_HEIGHT - 140
    agent2.rect.x = 100
    agent2.rect.y = constants.SCREEN_HEIGHT - 140
    high_happiness = Pudgi.select_parents(active_agent_list)
    for parents in high_happiness:
        pudgi = Pudgi(parents)
        active_sprite_list.add(pudgi)
        active_agent_list.append(pudgi)

    active_sprite_list.add(agent)
    active_sprite_list.add(agent2)

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

        if time_clock.elapsed_time() > time_clock.cur_time:
            time_clock.update_time()
            print(time_clock.time_stamp())

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

    # agent.export_to_json()
    pygame.quit()


if __name__ == "__main__":
    main()
