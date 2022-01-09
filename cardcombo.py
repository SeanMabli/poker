
  # for i in range(len(playernames)):
  #   combinedcards = np.vstack((playercards[i], dealercards))
# 
  #   if any([combinedcards[:, 1].tolist().count(i) >= 5 for i in ['C', 'D', 'H', 'S']]):
  #     playercombos[i, 4] = 1 # flush
# 
  #   if any([combinedcards[:, 0].tolist().count(i) >= 4 for i in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]):
  #     playercombos[i, 2] = 1 # 4 of a kind
  #   elif any([combinedcards[:, 0].tolist().count(i) >= 3 for i in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]):
  #     playercombos[i, 6] = 1 # 3 of a kind
# 
  #   if np.sum([combinedcards[:, 0].tolist().count(i) >= 2 for i in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]) == 2:
  #     playercombos[i, 7] = 1 # 2 pair
  #   elif any([combinedcards[:, 0].tolist().count(i) >= 2 for i in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]) and playercombos[i, 6] != 1:
  #     playercombos[i, 8] = 1 # pair
# 
  #   if (playercombos[i, 6] ==  1 or playercombos[i, 2] ==  1) and (playercombos[i, 8] == 1 or playercombos[i, 7] == 1): # (3 of a kind or 4 of a kind) and (pair or # two pair)
  #     playercombos[i, 3] = 1  # full house

    # 0, royal flush
    # 1, straight flush
    # 5, Check for straight
    # 9, Check for high card

  # High card
  # for i in reversed(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']):
  #   if playercards.flatten().tolist().count(i) > 0:
  #     if playercards.flatten().tolist().count(i) == 2 and playercards[np.where(playercards == i)[0]].flatten().tolist().count(i) != 2: break
  #     playercombos[np.where(playercards == i)[0], 9] = 1
  #     break

  # for i, player in enumerate(playercombos):
  #   print(playercards[i])
  #   print(dealercards)
  #   if player[0] == 1: print('royal flush')
  #   if player[1] == 1: print('straight flush')
  #   if player[2] == 1: print('4 of a kind')
  #   if player[3] == 1: print('full house')
  #   if player[4] == 1: print('flush')
  #   if player[5] == 1: print('straight')
  #   if player[6] == 1: print('3 of a kind')
  #   if player[7] == 1: print('two pair')
  #   if player[8] == 1: print('pair')
  #   if player[9] == 1: print('high card')
