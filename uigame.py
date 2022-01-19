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
startbox = pygame.Rect(200, 240, 150, 32)
betbox = pygame.Rect(70, 200, 90, 32)
callbox = pygame.Rect(10, 240, 150, 32)
foldbox = pygame.Rect(10, 280, 150, 32)
nextbox = pygame.Rect(10, 320, 150, 32)
nextgamebox = pygame.Rect(200, 10, 150, 32)
whowonbox = pygame.Rect(200, 360, 150, 32)

active = [False for _ in range(16)]
screen = 'start'
done = False

# poker variables
playernames = ['' for _ in range(10)]
blind = ''
startingcash = ''
bet = ''

playercards = np.full([len(playernames), 2, 2], '', dtype='<U10')
dealercards = np.full([5, 2], '')

gamenum = 0

while not done:
  for event in pygame.event.get(): # get user imput from pygame
    if event.type == pygame.QUIT: # check if user closes tab
      done = True
    
    if screen == 'start': # only run if the player is on the start scren
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
          screen = 'newgame'

      # text box input for player names
      for x in range(int(plusbox.y / 40 - 1)):
        if event.type == pygame.KEYDOWN and active[x]:
          if event.key == pygame.K_BACKSPACE:
            playernames[x] = playernames[x][:-1]
          elif len(playernames[x]) < 12:
            playernames[x] += event.unicode.lower()
      
      # text box input for blind
      if event.type == pygame.KEYDOWN and active[10]:
        if event.key == pygame.K_BACKSPACE:
          blind = blind[:-1]
        elif len(blind) < 12 and event.unicode.isnumeric():
          blind += event.unicode

      # text box input for starting cash
      if event.type == pygame.KEYDOWN and active[11]:
        if event.key == pygame.K_BACKSPACE:
          startingcash = startingcash[:-1]
        elif len(startingcash) < 12 and event.unicode.isnumeric():
          startingcash += event.unicode
  
    if screen == 'newgame': # run at the beginning of each game
      playerbets = np.zeros(playernames.shape, dtype=int)
      playerbets[0], playerbets[1] = blind[0], blind[1]
      aliveplayerbets = playerbets
      playercash -= playerbets

      minbet = blind[1]
      pot = 0

      playerfold = np.full(len(playernames), False, dtype=bool)

      # distribute deck to players and dealer
      deck = np.array([['A', 'C'], ['2', 'C'], ['3', 'C'], ['4', 'C'], ['5', 'C'], ['6', 'C'], ['7', 'C'],['8', 'C'], ['9', 'C'], ['10', 'C'], ['J', 'C'], ['Q', 'C'], ['K', 'C'], ['A', 'D'], ['2', 'D'], ['3', 'D'], ['4', 'D'], ['5', 'D'], ['6', 'D'], ['7', 'D'],['8', 'D'], ['9', 'D'], ['10', 'D'], ['J', 'D'], ['Q', 'D'], ['K', 'D'], ['A', 'H'], ['2', 'H'], ['3', 'H'], ['4', 'H'], ['5', 'H'], ['6', 'H'], ['7', 'H'],['8', 'H'], ['9', 'H'], ['10', 'H'], ['J', 'H'], ['Q', 'H'], ['K', 'H'], ['A', 'S'], ['2', 'S'], ['3', 'S'], ['4', 'S'], ['5', 'S'], ['6', 'S'], ['7', 'S'],['8', 'S'], ['9', 'S'], ['10', 'S'], ['J', 'S'], ['Q', 'S'], ['K', 'S']])
      np.random.shuffle(deck)

      for i in range(len(playernames)):
        for j in range(2):
          playercards[i, j] = deck[0]
          deck = deck[1:]
      playercards = playercards[: i + 1]
      
      for i in range(5):
        dealercards[i] = deck[0]
        deck = deck[1:]

    
      round = 0
      loop = False
      winner = ''
      currentplayer = 0

      screen = 'playerstart'

    if screen == 'playerstart': # a screen to confirm the player
      display.fill((0, 0, 0))
      display.blit(pygame.font.Font(None, 32).render("start " + playernames[currentplayer] + "'s turn", True, (255, 255, 255)), (80, 200))

      if event.type == pygame.MOUSEBUTTONDOWN:
        if startbox.collidepoint(event.pos):
          screen = 'playerturn'

    if screen == 'playerturn': # this screen gives the player information about the game
      display.fill((0, 0, 0))
      # player information
      display.blit(pygame.font.Font(None, 32).render(playernames[currentplayer] + "'s turn", True, (255, 255, 255)), (10, 10))
      display.blit(pygame.font.Font(None, 32).render('cards: ' + playercards[currentplayer, 0, 0] + playercards[currentplayer, 0, 1] + ', ' + playercards[currentplayer, 1, 0] + playercards[currentplayer, 1, 1], True, (255, 255, 255)), (10, 45))
      if round == 1:
        display.blit(pygame.font.Font(None, 32).render('flop: ' + dealercards[0, 0] + dealercards[0, 1] + ', ' + dealercards[1, 0] + dealercards[1, 1] + ', ' + dealercards[2, 0] + dealercards[2, 1], True, (255, 255, 255)), (10, 85))
      elif round == 2:
        display.blit(pygame.font.Font(None, 32).render('flop: ' + dealercards[0, 0] + dealercards[0, 1] + ', ' + dealercards[1, 0] + dealercards[1, 1] + ', ' + dealercards[2, 0] + dealercards[2, 1] + ', ' + dealercards[3, 0] + dealercards[3, 1], True, (255, 255, 255)), (10, 85))
      elif round == 3:
        display.blit(pygame.font.Font(None, 32).render('flop: ' + dealercards[0, 0] + dealercards[0, 1] + ', ' + dealercards[1, 0] + dealercards[1, 1] + ', ' + dealercards[2, 0] + dealercards[2, 1] + ', ' + dealercards[3, 0] + dealercards[3, 1] + ', ' + dealercards[4, 0] + dealercards[4, 1], True, (255, 255, 255)), (10, 85))
      if round == 0:

        display.blit(pygame.font.Font(None, 32).render('cash: ' + str(playercash[currentplayer]), True, (255, 255, 255)), (10, 85))
        display.blit(pygame.font.Font(None, 32).render('minimum bet: ' + str(minbet), True, (255, 255, 255)), (10, 125))
        display.blit(pygame.font.Font(None, 32).render('current bet: ' + str(playerbets[currentplayer]), True, (255, 255, 255)), (10, 165))

        betbox.y, callbox.y, foldbox.y, nextbox.y = 200, 240, 280, 360

        display.blit(pygame.font.Font(None, 32).render('bet:    ' + bet, True, (255, 255, 255)), (15, 205))
        display.blit(pygame.font.Font(None, 32).render('call', True, (255, 255, 255)), (65, 245))
        display.blit(pygame.font.Font(None, 32).render('fold', True, (255, 255, 255)), (65, 285))
        display.blit(pygame.font.Font(None, 32).render('next', True, (255, 255, 255)), (65, 365))

        pygame.draw.rect(display, (255, 255, 255), betbox, 2 if active[12] else 1)
        pygame.draw.rect(display, (255, 255, 255), callbox, 2 if active[13] else 1)
        pygame.draw.rect(display, (255, 255, 255), foldbox, 2 if active[14] else 1)
        pygame.draw.rect(display, (255, 255, 255), nextbox, 2)

      else:
        display.blit(pygame.font.Font(None, 32).render('cash: ' + str(playercash[currentplayer]), True, (255, 255, 255)), (10, 125))
        display.blit(pygame.font.Font(None, 32).render('minimum bet: ' + str(minbet), True, (255, 255, 255)), (10, 165))
        display.blit(pygame.font.Font(None, 32).render('current bet: ' + str(playerbets[currentplayer]), True, (255, 255, 255)), (10, 205))

        betbox.y, callbox.y, foldbox.y, nextbox.y = 240, 280, 320, 400

        display.blit(pygame.font.Font(None, 32).render('bet:    ' + bet, True, (255, 255, 255)), (15, 245))
        display.blit(pygame.font.Font(None, 32).render('call', True, (255, 255, 255)), (65, 285))
        display.blit(pygame.font.Font(None, 32).render('fold', True, (255, 255, 255)), (65, 325))
        display.blit(pygame.font.Font(None, 32).render('next', True, (255, 255, 255)), (65, 405))

        pygame.draw.rect(display, (255, 255, 255), betbox, 2 if active[12] else 1)
        pygame.draw.rect(display, (255, 255, 255), callbox, 2 if active[13] else 1)
        pygame.draw.rect(display, (255, 255, 255), foldbox, 2 if active[14] else 1)
        pygame.draw.rect(display, (255, 255, 255), nextbox, 2)


      if event.type == pygame.MOUSEBUTTONDOWN:
        if betbox.collidepoint(event.pos):
          active[12] = not active[12]
        else:
          active[12] = False
        
        if callbox.collidepoint(event.pos):
          active[13] = not active[13]
        elif not nextbox.collidepoint(event.pos):
          active[13] = False
  
        if foldbox.collidepoint(event.pos):
          active[14] = not active[14]
        elif not nextbox.collidepoint(event.pos):
          active[14] = False
  
        if nextbox.collidepoint(event.pos) and (bet != '' or active[13] or active[14]):
          # at the end of this turn this script runs to make adjustments to the money variables
          if len(bet) > 0 and int(bet) < playercash[currentplayer]:
            playerbets[currentplayer] += int(bet)
            playercash[currentplayer] -= int(bet)
            minbet = int(bet)
            bet = ''
          if active[13]:
            playercash[currentplayer] -= minbet - playerbets[currentplayer]
            playerbets[currentplayer] = minbet
            active[13] = False
          if active[14]:
            playerfold[currentplayer] = True

          screen = 'playerstart'

          if np.sum(playerfold) == len(playernames) - 1:
            pot += np.sum(playerbets)
            playerbets = np.zeros(playernames.shape, dtype=int)
            screen = 'whowon'

          if currentplayer != len(playernames) - 1:
            currentplayer += 1
            while playerfold[currentplayer]  == True:
              currentplayer += 1
          else:
            currentplayer = 0
            while playerfold[currentplayer]  == True:
              currentplayer += 1

            aliveplayerbets = playerbets
            x = 0
            for i in range(len(playernames)):
              if playerfold[i] == True:
                aliveplayerbets = np.delete(aliveplayerbets, i - x)
                x += 1
            
            if all(element == aliveplayerbets[0] for element in aliveplayerbets) == True or loop == False:
              pot += np.sum(playerbets)
              playerbets = np.zeros(playernames.shape, dtype=int)
              round += 1
              if round == 4:
                screen = 'whowon'
              loop = False

            loop = True
      
      if event.type == pygame.KEYDOWN and active[12]:
        if event.key == pygame.K_BACKSPACE:
          bet = bet[:-1]
        elif len(bet) < 6 and event.unicode.isnumeric():
          bet += event.unicode

    if screen == 'whowon': # since i couldn't figure out who won with a script this script asks the player who won
      display.fill((0, 0, 0))
      if np.sum(playerfold) == len(playernames) - 1:
        playercash[playerfold.tolist().index(False)] += pot
        winner = playernames[playerfold.tolist().index(False)]
        screen = 'winner'
      else:
        display.blit(pygame.font.Font(None, 32).render('dealer cards: ' + dealercards[0, 0] + dealercards[0, 1] + ', ' + dealercards[1, 0] + dealercards[1, 1] + ', ' + dealercards[2, 0] + dealercards[2, 1] + ', ' + dealercards[3, 0] + dealercards[3, 1] + ', ' + dealercards[4, 0] + dealercards[4, 1], True, (255, 255, 255)), (10, 10))
        for player, cards in enumerate(playercards):
          display.blit(pygame.font.Font(None, 32).render(playernames[player] + "'s cards: " + cards[0, 0] + cards[0, 1] + ', ' + cards[1, 0] + cards[1, 1], True, (255, 255, 255)), (10, 45 + player * 40))

        display.blit(pygame.font.Font(None, 32).render('who won?', True, (255, 255, 255)), (200, 325))
        pygame.draw.rect(display, (255, 255, 255), whowonbox, 2 if active[15] else 1)
        display.blit(pygame.font.Font(None, 32).render(winner, True, (255, 255, 255)), (whowonbox.x + 5, whowonbox.y + 5))


        display.blit(pygame.font.Font(None, 32).render('next', True, (255, 255, 255)), (250, 405))
        nextgamebox.y = 400
        pygame.draw.rect(display, (255, 255, 255), nextgamebox, 2)


        if event.type == pygame.MOUSEBUTTONDOWN:
          if whowonbox.collidepoint(event.pos):
            active[15] = not active[15]
          else:
            active[15] = False
          
          if nextgamebox.collidepoint(event.pos) and winner in playernames:
            for i, player in enumerate(playernames):
              if winner == player:
                playercash[i] += pot

            screen = 'winner'

        if event.type == pygame.KEYDOWN and active[15]:
          if event.key == pygame.K_BACKSPACE:
            winner = winner[:-1]
          elif len(winner) < 12:
            winner += event.unicode

    if screen == 'winner': # this displays the winner, current player cash and starts the next game
      display.fill((0, 0, 0))
      display.blit(pygame.font.Font(None, 32).render(winner + ' won', True, (255, 255, 255)), (10, 10))
      for i, player in enumerate(playernames):
        display.blit(pygame.font.Font(None, 32).render(player + "'s cash: " + str(playercash[i]), True, (255, 255, 255)), (10, 45 + i * 40))

      display.blit(pygame.font.Font(None, 32).render('next game', True, (255, 255, 255)), (220, 15))
      nextgamebox.y = 10
      pygame.draw.rect(display, (255, 255, 255), nextgamebox, 2)


      if event.type == pygame.MOUSEBUTTONDOWN:
        if nextgamebox.collidepoint(event.pos):
          screen = 'newgame'

  pygame.display.flip()

pygame.quit()