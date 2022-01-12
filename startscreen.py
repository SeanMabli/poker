import pygame

pygame.init()
screen = pygame.display.set_mode((750, 500))
playernamesbox = [pygame.Rect(10, i * 40 + 40, 150, 32) for i in range(10)]
playernames = ['' for _ in range(10)]
active = [False for _ in range(10)]
done = False

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True

    for x in range(10):
      if event.type == pygame.MOUSEBUTTONDOWN:
        if playernamesbox[x].collidepoint(event.pos):
          active[x] = not active[x]
        else:
          active[x] = False

      if event.type == pygame.KEYDOWN and active[x]:
        if event.key == pygame.K_BACKSPACE:
          playernames[x] = playernames[x][:-1]
        elif len(playernames[x]) < 12:
          playernames[x] += event.unicode

  screen.fill((0, 0, 0))
  screen.blit(pygame.font.Font(None, 32).render("player names:", True, (255, 255, 255)), (10, 10))
  for x in range(10):
    txt_surface = pygame.font.Font(None, 32).render(playernames[x], True, (255, 255, 255))
    screen.blit(txt_surface, (playernamesbox[x].x+5, playernamesbox[x].y+5))
    pygame.draw.rect(screen, (255, 255, 255), playernamesbox[x], 2 if active[x] else 1)
  
  pygame.display.flip()

pygame.quit()