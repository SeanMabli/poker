import pygame
import numpy as np

# pygame init
pygame.init()
pygame.display.set_caption('poker')

# pygame variables
display = pygame.display.set_mode((360, 450))
playernamesbox = [pygame.Rect(10, i * 40 + 40, 150, 32) for i in range(10)]
plusbox = pygame.Rect(70, 120, 20, 32)
blindbox = pygame.Rect(200, 40, 150, 32)
startingcashbox = pygame.Rect(200, 160, 150, 32)
active = [False for _ in range(12)]
screen = 'player'
done = False

# game variables
playernames = np.array(['sean', 'zain']) # ['' for _ in range(10)]
blind = np.array([2, 4]) # ''
startingcash = ''
playercash = np.array([200, 200]) # delete in real game
startbox = pygame.Rect(50, 195, 250, 32) # pygame.Rect(200, 240, 150, 32)

# place in game variables
currentplayer = 0
partofgame = 'startofgame'

# poker variables
playercards = np.full([len(playernames), 2, 2], '', dtype='<U10')
dealercards = np.full([5, 2], '')

gamenum = 0
round = 1

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

      # mouse clicks
      if event.type == pygame.MOUSEBUTTONDOWN:
        # player name boxes
        for x in range(int(plusbox.y / 40 - 1)):
          if playernamesbox[x].collidepoint(event.pos):
            active[x] = not active[x]
          else:
            active[x] = False

        # plus box
        if plusbox.collidepoint(event.pos):
          plusbox.y += 40
        
        # blind box
        if blindbox.collidepoint(event.pos):
          active[10] = not active[10]
        else:
          active[10] = False

        # starting cash box
        if startingcashbox.collidepoint(event.pos):
          active[11] = not active[11]
        else:
          active[11] = False
        
        # start button
        if startbox.collidepoint(event.pos):
          for i in reversed(playernames):
            if i == '':
              playernames.pop()
          playernames = np.array(playernames)
          playercash = np.array([int(startingcash)] * len(playernames))
          blind = np.array([int(blind), int(blind) * 2])
          startbox = pygame.Rect(50, 195, 250, 32)
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
      if partofgame == 'startofgame':
        playerbets = np.zeros(playernames.shape, dtype=int)
        playerbets[0], playerbets[1] = blind[0], blind[1]
        aliveplayerbets = playerbets
        playercash -= playerbets

        minbet = blind[1]
        pot = 0

        playerfold = np.full(len(playernames), False, dtype=bool)

        deck = np.array([['A', 'C'], ['2', 'C'], ['3', 'C'], ['4', 'C'], ['5', 'C'], ['6', 'C'], ['7', 'C'],['8', 'C'], ['9', 'C'], ['10', 'C'], ['J', 'C'], ['Q', 'C'], ['K', 'C'], ['A', 'D'], ['2', 'D'], ['3', 'D'], ['4', 'D'], ['5', 'D'], ['6', 'D'], ['7', 'D'],['8', 'D'], ['9', 'D'], ['10', 'D'], ['J', 'D'], ['Q', 'D'], ['K', 'D'], ['A', 'H'], ['2', 'H'], ['3', 'H'], ['4', 'H'], ['5', 'H'], ['6', 'H'], ['7', 'H'],['8', 'H'], ['9', 'H'], ['10', 'H'], ['J', 'H'], ['Q', 'H'], ['K', 'H'], ['A', 'S'], ['2', 'S'], ['3', 'S'], ['4', 'S'], ['5', 'S'], ['6', 'S'], ['7', 'S'],['8', 'S'], ['9', 'S'], ['10', 'S'], ['J', 'S'], ['Q', 'S'], ['K', 'S']])
        np.random.shuffle(deck)

        for i in range(len(playernames)):
          for j in range(2):
            playercards[i, j] = deck[0]
            deck = deck[1:]
        
        for i in range(5):
          dealercards[i] = deck[0]
          deck = deck[1:]

        partofgame = 'turn'

      if partofgame == 'turnscreen':
        display.blit(pygame.font.Font(None, 32).render("start " + playernames[currentplayer] + "'s turn", True, (255, 255, 255)), (80, 200))

        if event.type == pygame.MOUSEBUTTONDOWN:
          if startbox.collidepoint(event.pos):
            partofgame = 'turn'

      if partofgame == 'turn':
        # player information
        display.blit(pygame.font.Font(None, 32).render(playernames[currentplayer] + "'s turn", True, (255, 255, 255)), (10, 10))
        display.blit(pygame.font.Font(None, 32).render('cards: ' + playercards[currentplayer, 0, 0] + playercards[currentplayer, 0, 1] + ', ' + playercards[currentplayer, 1, 0] + playercards[currentplayer, 1, 1], True, (255, 255, 255)), (10, 40))
        if round == 1:
          display.blit(pygame.font.Font(None, 32).render('flop: ' + dealercards[0, 0] + dealercards[0, 1] + ', ' + dealercards[1, 0] + dealercards[1, 1] + ', ' + dealercards[2, 0] + dealercards[2, 1], True, (255, 255, 255)), (10, 70))
        elif round == 2:
          display.blit(pygame.font.Font(None, 32).render('flop: ' + dealercards[0, 0] + dealercards[0, 1] + ', ' + dealercards[1, 0] + dealercards[1, 1] + ', ' + dealercards[2, 0] + dealercards[2, 1] + ', ' + dealercards[3, 0] + dealercards[3, 1], True, (255, 255, 255)), (10, 70))
        elif round == 3:
          display.blit(pygame.font.Font(None, 32).render('flop: ' + dealercards[0, 0] + dealercards[0, 1] + ', ' + dealercards[1, 0] + dealercards[1, 1] + ', ' + dealercards[2, 0] + dealercards[2, 1] + ', ' + dealercards[3, 0] + dealercards[3, 1] + ', ' + dealercards[4, 0] + dealercards[4, 1], True, (255, 255, 255)), (10, 70))
        if round == 0:
          display.blit(pygame.font.Font(None, 32).render('cash: ' + str(playercash[currentplayer]), True, (255, 255, 255)), (10, 70))
          display.blit(pygame.font.Font(None, 32).render('minimum bet: ' + str(minbet), True, (255, 255, 255)), (10, 100))
          display.blit(pygame.font.Font(None, 32).render('current bet: ' + str(playerbets[currentplayer]), True, (255, 255, 255)), (10, 130))
        else:
          display.blit(pygame.font.Font(None, 32).render('cash: ' + str(playercash[currentplayer]), True, (255, 255, 255)), (10, 100))
          display.blit(pygame.font.Font(None, 32).render('minimum bet: ' + str(minbet), True, (255, 255, 255)), (10, 130))
          display.blit(pygame.font.Font(None, 32).render('current bet: ' + str(playerbets[currentplayer]), True, (255, 255, 255)), (10, 160))

        
      

  pygame.display.flip()

pygame.quit()