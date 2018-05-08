# This is the main file for running the project

# lets just create a pudgi and see if it fails

import pygame
import constants
import environments
from clock import Clock
from pudgi import Pudgi
import random


def main():

    death_count = 0

    time_clock = Clock()

    # ----------- pygame objects -----------
    pygame.init()

    pygame.font.init()

    font = pygame.font.SysFont('Comic Sans MS', 30)

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    active_agent_list = []

    agent = Pudgi()
    agent2 = Pudgi()

    active_agent_list.append(agent)
    agent.export_to_json()
    active_agent_list.append(agent2)
    agent2.export_to_json()

    pygame.display.set_caption("Pudgi Simulation")

    env_list = [environments.EnvironmentHouse(agent)]

    current_env_no = 0
    current_env = env_list[current_env_no]

    active_sprite_list = pygame.sprite.Group()
    agent.env = current_env

    agent.rect.x = 340
    agent.rect.y = constants.SCREEN_HEIGHT - 140
    agent2.rect.x = 100
    agent2.rect.y = constants.SCREEN_HEIGHT - 140

    # for parents in high_happiness:
    #     pudgi = Pudgi(parents)
    #     active_sprite_list.add(pudgi)
    #     active_agent_list.append(pudgi)

    active_sprite_list.add(agent)
    active_sprite_list.add(agent2)

    done = False

    game_clock = pygame.time.Clock()

    # ----------- JSON objects ------------
    # handler.load_file("./data/metadata.json")
    # data = handler.get_data()
    # number = "001"
    # node = data["root"]
    # for char in number:
    #     node = node[char]

    frames_run = 0
    movement = {}
    movement_time = 0
    movement_direction = ""

    movement[agent.name] = {"time": movement_time, "direction": movement_direction}
    movement[agent2.name] = {"time": movement_time, "direction": movement_direction}

    # --------------Main While loop---------------
    while not done:

        high_happiness = Pudgi.select_parents(active_agent_list)

        for parents in high_happiness:
            pudgi = Pudgi(parents)
            active_sprite_list.add(pudgi)
            active_agent_list.append(pudgi)
            pudgi.export_to_json()
            pudgi.rect.y = constants.SCREEN_HEIGHT - 140
            pudgi.rect.x = random.randint(100, 800)
            movement[pudgi.name] = {"time": movement_time, "direction": movement_direction}

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop


            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         agent.go_left()
            #     if event.key == pygame.K_RIGHT:
            #         agent.go_right()
            #     # if event.key == pygame.K_UP:
            #     #     agent.jump()
            #
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_LEFT and agent.change_x < 0:
            #         agent.stop()
            #     if event.key == pygame.K_RIGHT and agent.change_x > 0:
            #         agent.stop()

        for pudgi in active_agent_list:
            if pudgi.age >= pudgi.lifespan:
                active_agent_list.remove(pudgi)
                active_sprite_list.remove(pudgi)
                death_count += 1

                print("---------------------------------------------")
                print("<<<---" + pudgi.name + " died of old age--->>>")
                print("Death Count: " + str(death_count))
                print("---------------------------------------------")
            if pudgi.sleeping:
                movement[pudgi.name]["direction"] = "S"
                pudgi.direction = "S"
            else:
                if movement[pudgi.name]["time"] <= 0:
                    movement[pudgi.name]["time"] = random.randint(30, 90)
                    movement[pudgi.name]["direction"] = random.choice(["L", "R", ""])

            movement[pudgi.name]["time"] -= 1
            pudgi.movement(movement[pudgi.name]["direction"])

        active_sprite_list.update()

        current_env.update()

        current_env.draw(screen)
        active_sprite_list.draw(screen)

        time_clock.update_time()
        clockSurface = font.render(time_clock.time_stamp(), True, constants.BLACK, constants.WHITE)
        clockRect = clockSurface.get_rect()
        clockRect.x = screen.get_rect().centerx - 120
        clockRect.y = 2
        clockBorder = pygame.draw.rect(screen, constants.BLACK, (clockRect.x - 2, clockRect.y - 2, clockRect.width + 4, clockRect.height + 4))
        screen.blit(clockSurface, clockRect)

        deathCountSurface = font.render("Deaths: " + str(death_count), True, constants.BLACK, constants.WHITE)
        deathCountRect = deathCountSurface.get_rect()
        deathCountRect.x = clockRect.x + 120
        deathCountRect.y = 2
        deathCountBorder = pygame.draw.rect(screen, constants.BLACK,
                                       (deathCountRect.x - 2, deathCountRect.y - 2, deathCountRect.width + 4, deathCountRect.height + 4))
        screen.blit(deathCountSurface, deathCountRect)

        game_clock.tick(30)

        if frames_run == 0:
            for pudgi in active_agent_list:
                if pudgi.vitality <= 0:
                    active_agent_list.remove(pudgi)
                    active_sprite_list.remove(pudgi)
                    death_count += 1
                    print("---------------------------------------------")
                    print("<<<---" + pudgi.name + " died in childbirth--->>>")
                    print("Death Count: " + str(death_count))
                    print("---------------------------------------------")
                if int(time_clock.get_minutes()) % 15 == 0:
                    pudgi.make_decision()

        pygame.display.flip()

        frames_run += 1

        if frames_run > 30:
            frames_run = 0

    for pudgi in active_agent_list:
        pudgi.export_to_json()

    pygame.quit()


if __name__ == "__main__":
    main()
