import pygame

pygame.init()
pygame.display.set_caption('poker')

display = pygame.display.set_mode((360, 450))
playernamesbox = [pygame.Rect(10, i * 40 + 40, 150, 32) for i in range(10)]
playernames = ['' for _ in range(10)]
plusbox = pygame.Rect(70, 120, 20, 32)
blindbox = pygame.Rect(200, 40, 150, 32)
blind = ''
startingcashbox = pygame.Rect(200, 160, 150, 32)
startingcash = ''
startbox = pygame.Rect(200, 240, 150, 32)
active = [False for _ in range(12)]
screen = 'start'
done = False

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True

    if screen == 'start':
      display.fill((0, 0, 0))

      # player names input
      display.blit(pygame.font.Font(None, 32).render("player names:", True, (255, 255, 255)), (10, 10))
      for x in range(int(plusbox.y / 40 - 1)):
        txt_surface = pygame.font.Font(None, 32).render(playernames[x], True, (255, 255, 255))
        display.blit(txt_surface, (playernamesbox[x].x+5, playernamesbox[x].y+5))
        pygame.draw.rect(display, (255, 255, 255), playernamesbox[x], 2 if active[x] else 1)
      if plusbox.y <= 400:
        display.blit(pygame.font.Font(None, 45).render('+', True, (255, 255, 255)), (75, plusbox.y))
      
      # blind input
      display.blit(pygame.font.Font(None, 32).render("blind:", True, (255, 255, 255)), (200, 10))
      display.blit(pygame.font.Font(None, 32).render(blind, True, (255, 255, 255)), (blindbox.x + 5, blindbox.y + 5))
      pygame.draw.rect(display, (255, 255, 255), blindbox, 2 if active[10] else 1)

      # starting cash input
      display.blit(pygame.font.Font(None, 32).render("starting cash:", True, (255, 255, 255)), (200, 130))
      display.blit(pygame.font.Font(None, 32).render(startingcash, True, (255, 255, 255)), (startingcashbox.x + 5, startingcashbox.y + 5))
      pygame.draw.rect(display, (255, 255, 255), startingcashbox, 2 if active[11] else 1)

      # start button
      pygame.draw.rect(display, (255, 255, 255), startbox, 2)
      display.blit(pygame.font.Font(None, 32).render("start", True, (255, 255, 255)), (248, 245))

      if event.type == pygame.MOUSEBUTTONDOWN:
        for x in range(int(plusbox.y / 40 - 1)):
          if playernamesbox[x].collidepoint(event.pos):
            active[x] = not active[x]
          else:
            active[x] = False

        if plusbox.collidepoint(event.pos):
          plusbox.y += 40
          
        if blindbox.collidepoint(event.pos):
          active[10] = not active[10]
        else:
          active[10] = False

        if startingcashbox.collidepoint(event.pos):
          active[11] = not active[11]
        else:
          active[11] = False
        
        if startbox.collidepoint(event.pos):
          blind = int(blind)
          startingcash = int(startingcash)
          screen = 'player'

      for x in range(int(plusbox.y / 40 - 1)):
        if event.type == pygame.KEYDOWN and active[x]:
          if event.key == pygame.K_BACKSPACE:
            playernames[x] = playernames[x][:-1]
          elif len(playernames[x]) < 12:
            playernames[x] += event.unicode.lower()
      
      if event.type == pygame.KEYDOWN and active[10]:
        if event.key == pygame.K_BACKSPACE:
          blind = blind[:-1]
        elif len(blind) < 12 and event.unicode.isnumeric():
          blind += event.unicode

      if event.type == pygame.KEYDOWN and active[11]:
        if event.key == pygame.K_BACKSPACE:
          startingcash = startingcash[:-1]
        elif len(startingcash) < 12 and event.unicode.isnumeric():
          startingcash += event.unicode
  
    if screen == 'player':
      display.fill((0, 0, 0))
      
      

  pygame.display.flip()

pygame.quit()