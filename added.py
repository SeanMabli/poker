  if np.sum(playerfold) == len(playernames) - 1:
    playercash[playerfold.tolist().index(False)] += pot
  else:
    print('dealer cards: ' + dealercards[0, 0] + dealercards[0, 1] + ', ' + dealercards[1, 0] + dealercards[1, 1] + ', ' + dealercards[2, 0] + dealercards[2, 1] + ', ' + dealercards[3, 0] + dealercards[3, 1] + ', ' + dealercards[4, 0] + dealercards[4, 1])
    for player, cards in enumerate(playercards):
      print(playernames[player] + "'s cards: " + cards[0, 0] + cards[0, 1] + ', ' + cards[1, 0] + cards[1, 1])

    winner = input('who won? ').strip().lower()
    for i, player in enumerate(playernames):
      if winner == player:
        playercash[i] += pot

  for i, player in enumerate(playernames):
    print(player + "'s cash: " + str(playercash[i]))
  input('press enter to continue to next game')
  os.system('cls')
  gamenum += 1