import numpy as np
import os

# def inputwtypo(propt, possibleout):
#   x = input(propt)
#   while x not in possibleout:
#     x = input(propt)
#   return x

deck = np.array([['A', 'C'], ['2', 'C'], ['3', 'C'], ['4', 'C'], ['5', 'C'], ['6', 'C'], ['7', 'C'],['8', 'C'], ['9', 'C'], ['10', 'C'], ['J', 'C'], ['Q', 'C'], ['K', 'C'], ['A', 'D'], ['2', 'D'], ['3', 'D'], ['4', 'D'], ['5', 'D'], ['6', 'D'], ['7', 'D'],['8', 'D'], ['9', 'D'], ['10', 'D'], ['J', 'D'], ['Q', 'D'], ['K', 'D'], ['A', 'H'], ['2', 'H'], ['3', 'H'], ['4', 'H'], ['5', 'H'], ['6', 'H'], ['7', 'H'],['8', 'H'], ['9', 'H'], ['10', 'H'], ['J', 'H'], ['Q', 'H'], ['K', 'H'], ['A', 'S'], ['2', 'S'], ['3', 'S'], ['4', 'S'], ['5', 'S'], ['6', 'S'], ['7', 'S'],['8', 'S'], ['9', 'S'], ['10', 'S'], ['J', 'S'], ['Q', 'S'], ['K', 'S']])
np.random.shuffle(deck)

input('use enter to advance through the game')
os.system('clear')

playernames = np.array(['zain', 'adam', 'sean']) # np.array(input("enter player names (seprated by comma's): ").strip().lower().split(','))
os.system('clear')

smallblind = 1 # int(input('small blind: '))
blind = np.array([smallblind, smallblind * 2])
os.system('clear')

cash = 200 # int(input('player starting cash: '))
playercash = np.array([cash] * len(playernames))
os.system('clear')

playercards = np.empty([len(playernames), 2, 2], str)
dealercards = np.empty([5, 2], str)

playerbets = np.zeros(playernames.shape, dtype=int)
playerbets[0], playerbets[1] = blind[0], blind[1]
playercash -= playerbets
aliveplayerbets = playerbets
minbet = blind[1]
pot = 0

playerfold = np.full(len(playernames), False, dtype=bool)

gamenum = 0
while True:
  playerbets[0], playerbets[1] = blind[0], blind[1]
  playercash -= playerbets

  for i in range(len(playernames)):
    for j in range(2):
      playercards[i, j] = deck[0]
      deck = deck[1:]

  for i in range(5):
    dealercards[i] = deck[0]
    deck = deck[1:]

  for round in range(4):
    loop = False
    while (all(element == aliveplayerbets[0] for element in aliveplayerbets) == False and any(playerfold == False) == True) or loop == False:
      for i in range(len(playernames)):
        if playerfold[i] == False:
          input('start ' + playernames[i] + "'s turn")
          print('cards: ' + playercards[i, 0, 0] + playercards[i, 0, 1] + ', ' + playercards[i, 1, 0] + playercards[i, 1, 1])
          if round == 1:
            print('flop: ' + dealercards[0, 0] + dealercards[0, 1] + ', ' + dealercards[1, 0] + dealercards[1, 1] + ', ' + dealercards[2, 0] + dealercards[2, 1])
          elif round == 2:
            print('flop: ' + dealercards[0, 0] + dealercards[0, 1] + ', ' + dealercards[1, 0] + dealercards[1, 1] + ', ' + dealercards[2, 0] + dealercards[2, 1] + ', ' + dealercards[3, 0] + dealercards[3, 1])
          elif round == 3:
            print('flop: ' + dealercards[0, 0] + dealercards[0, 1] + ', ' + dealercards[1, 0] + dealercards[1, 1] + ', ' + dealercards[2, 0] + dealercards[2, 1] + ', ' + dealercards[3, 0] + dealercards[3, 1] + ', ' + dealercards[4, 0] + dealercards[4, 1])
          print('cash: ' + str(playercash[i]))
          print('minimum bet: ' + str(minbet))
          print('current bet: ' + str(playerbets[i]))
          y = input('(b)et, (c)all, or (f)old: ').lower()
          if y == 'b' or y == 'bet':
            x = int(input('bet: '))
            minbet = x if minbet < x < playercash[i] else 0
            playerbets[i] += minbet
            playercash[i] -= minbet
          elif y == 'c' or y == 'call':
            playercash[i] -= minbet - playerbets[i]
            playerbets[i] = minbet
          elif y == 'f' or y == 'fold':
            playerfold[i] = True
          os.system('clear')

        if np.sum(playerfold) == len(playernames) - 1:
          os.system('clear')
          playercash[playerfold.tolist().index(False)] += np.sum(playerbets)
          playerbets = np.zeros(playernames.shape, dtype=int)
          playerfold = np.full(len(playernames), True, dtype=bool)
          break

      loop = True

      aliveplayerbets = playerbets
      x = 0
      for i in range(len(playernames)):
        if playerfold[i] == True:
          aliveplayerbets = np.delete(aliveplayerbets, i - x)
          x += 1

    pot += np.sum(playerbets)       
    playerbets = np.zeros(playernames.shape, dtype=int)

  # Check for royal flush

  # Check for straight flush

  # Check for 4 of a kind

  # Check for full house

  # Check for flush

  # Check for straight

  # Check for 3 of a kind

  # Check for 2 pair

  # Check for 1 pair

  # Check for high card

  print(playercash)
  gamenum += 1