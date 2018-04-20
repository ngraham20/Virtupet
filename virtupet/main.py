# This is the main file for running the project

# lets just create a pudgi and see if it fails

import pygame
import constants
import environments
from clock import Clock
from pudgi import Pudgi


def main():
    time_clock = Clock()

    # ----------- pygame objects -----------
    pygame.init()

    pygame.font.init()

    font = pygame.font.SysFont('Comic Sans MS', 30)

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Pudgi Simulation")

    parents = ["0x9c08", "0x11e66"]
    # agent = Pudgi(parents)
    agent = Pudgi(None, "./data/pudgies/0x8653.json")
    # agent = Pudgi()
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

        time_clock.update_time()
        clockSurface = font.render(time_clock.time_stamp(), True, constants.BLACK, constants.WHITE)
        clockRect = clockSurface.get_rect()
        clockRect.centerx = screen.get_rect().centerx
        clockRect.y = 2
        clockBorder = pygame.draw.rect(screen, constants.BLACK, (clockRect.x - 2, clockRect.y - 2, clockRect.width + 4, clockRect.height + 4))
        screen.blit(clockSurface, clockRect)

        screen.blit(clockSurface, clockRect)

        clock.tick(30)

        pygame.display.flip()

    agent.export_to_json()
    pygame.quit()


if __name__ == "__main__":
    main()
