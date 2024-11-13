import pygame
from agent import Agent
from environment import Environment

def main():
    env = Environment(800, 600)
    agent = Agent(0, 0, 2, env)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(agent)
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            agent.move("left")
        if keys[pygame.K_RIGHT]:
           agent.move("right")
        if keys[pygame.K_UP]:
            agent.move("up")
        if keys[pygame.K_DOWN]:
            agent.move("down")

        env.screen.fill(env.BACKGROUND_COLOR)
        all_sprites.draw(env.screen)

        frame_text = env.font.render(f"Position: ({agent.rect.x}, {agent.rect.y})", True, env.TEXT_COLOR)
        frame_text2 = env.font.render(f"Speed: {agent.speed}", True, env.TEXT_COLOR)
        
        env.screen.blit(frame_text, (10, 10))
        env.screen.blit(frame_text2, (550, 10))

        pygame.display.flip()
        

if __name__ == "__main__":
    main()