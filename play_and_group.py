from collections import Counter
from itertools import combinations
import copy


def test_valid_run(cards):
    """Input a list of cards and determine
    if the list of cards is a valid run or not"""

    # take the non-Aces cards and sort them according to their values.
    # Take the Aces card and put them into a separate list.
    translate = {'1': 1, '2': 2, '3': 3, '4': 4,
                 '5': 5, '6': 6, '7': 7, '8': 8,
                 '9': 9,
                 'J': 11, 'Q': 12, 'K': 13, '0': 10, 'A': 20}
    translate2 = {'C': 'B', 'S': 'B', 'H': 'R', 'D': 'R'}

    # split the list of cards into two lists, one contain Aces
    # one doesn't contain A
    aces = []
    non_aces = []
    for card in cards:
        if card in ('AS', 'AD', 'AH', 'AC'):
            aces.append((card[0], translate2[card[1]]))
        else:
            non_aces.append((translate[card[0]], translate2[card[1]]))
    non_aces = sorted(non_aces)

    # test for run validation
    if len(cards) < 3:
        return False
    else:
        run = True
        # loop through the list to check a non-Ace card and its preceding card
        # to see if their value difference and colour satisfy the requirement
        # for a run. If not, check if there are Aces that can be used
        # to replace the card. Remove Aces that are used in the run.
        for count in range(len(non_aces) - 1):
            diff = non_aces[count + 1][0] - non_aces[count][0]
            if diff == 0:
                run = False
            else:
                if diff == 1:
                    if non_aces[count][1] == non_aces[count + 1][1]:
                        run = False
                        break
                else:
                    if not aces:
                        run = False
                        break

                    if diff == 2:
                        if non_aces[count][1] != non_aces[count + 1][1]:
                            run = False
                            break
                        existing = False
                        for ace in aces:
                            if ace[1] != non_aces[count][1]:
                                existing = True
                                aces.remove(ace)
                                break
                        if not existing:
                            run = False
                            break

                    elif diff == 3:
                        if non_aces[count][1] == non_aces[count + 1][1]:
                            run = False
                            break
                        if len(aces) < 2:
                            run = False
                            break
                        existing1 = False
                        existing2 = False
                        for ace in aces:
                            if ace[1] != non_aces[count][1]:
                                existing1 = True
                                aces.remove(ace)
                        for ace in aces:
                            if ace[1] == non_aces[count][1]:
                                existing2 = True
                                aces.remove(ace)
                        if not existing1 or not existing2:
                            run = False
                            break

                    elif diff == 4:
                        if non_aces[count][1] != non_aces[count + 1][1]:
                            run = False
                            break
                        if len(aces) < 3:
                            run = False
                            break
                        existing1 = False
                        existing2 = False
                        existing3 = False
                        for ace in aces:
                            if ace[1] != non_aces[count][1]:
                                existing1 = True
                                aces.remove(ace)
                        for ace in aces:
                            if ace[1] == non_aces[count][1]:
                                existing2 = True
                                aces.remove(ace)
                        for ace in aces:
                            if ace[1] != non_aces[count][1]:
                                existing3 = True
                                aces.remove(ace)
                        if not (existing1 and existing2 and existing3):
                            run = False
                            break

                    elif diff == 5:
                        if non_aces[count][1] == non_aces[count + 1][1]:
                            run = False
                            break
                        if len(aces) != 4:
                            run = False
                            break
                        else:
                            aces = []
                    else:
                        run = False
                        break
        # if they are still Aces left in the Aces_list
        if aces:
            run = False
        return run


def comp10001go_play(discard_history, player_no, hand):
    """Discard a card from my hand according to a strategy
    based on the cards I have discarded"""
    round = 11 - len(hand)
    translate = {'1': 1, '2': 2, '3': 3, '4': 4,
                 '5': 5, '6': 6, '7': 7, '8': 8,
                 '9': 9,
                 'J': 11, 'Q': 12, 'K': 13, '0': 10, 'A': 20}
    translate2 = {'C': 'B', 'S': 'B', 'H': 'R', 'D': 'R'}
    # take the non-Aces cards and sort them according to their values.
    non_aces = []
    for card in hand:
        if card not in ('AS', 'AD', 'AH', 'AC'):
            non_aces.append((translate[card[0]], translate2[card[1]]))
    non_aces = sorted(non_aces)

    if round == 1:
        # discard the card 'Q', otherwise the card that has highest value
        for card in hand:
            if card[0] == 'Q':
                return card
        return_list = [card for card in non_aces if card[0] == non_aces[-1][0]]
        value = return_list[0][0]
        for card in hand:
            if translate[card[0]] == value:
                return card

    elif 2 <= round <= 9:
        # create a freq dictionary of all my discarded cards
        my_discard_history = []
        other_player_history = []
        for list_index in range(round - 1):
            for player_index in range(4):
                if player_index == player_no:
                    (my_discard_history
                    .append(discard_history[list_index][player_index]))
                else:
                    (other_player_history
                    .append(discard_history[list_index][player_index]))

        # Prefer the value I discarded before (excluding Aces)
        # that others haven't discarded
        # otherwise, prefer the value I have discarded

        value_lst = [card[0] for card in hand if card in my_discard_history and
                     card[0] != 'A' and card not in other_player_history]
        second_value_list = [card[0] for card in hand if card in
                             my_discard_history and card[0] != 'A']
        d = Counter(value_lst)
        d2 = Counter(second_value_list)

        if 2 <= round <= 9:
            if d:
                for card in hand:
                    for count in range(round):
                        if card[0] == d.most_common(count + 1)[count][0]:
                            return card
            if d2:
                for card in hand:
                    for count in range(round):
                        if card[0] == d2.most_common(count + 1)[count][0]:
                            return card
            # if none of those values appear in my hand,
            # discard the card that has the highest value at the 2-8th
            # round, return the lowest possible value card at 8th round.
            return_list = []
            if round <= 8:
                return_list = [card for card in non_aces
                               if card[0] == non_aces[-1][0]]
            else:
                return_list = [card for card in non_aces
                               if card[0] == non_aces[0][0]]
            if return_list:
                value = return_list[0][0]
                for card in hand:
                    if translate[card[0]] == value:
                        return card
            # if only two Aces are left, I can only pick ace
            else:
                return hand[0]
    # last_round
    else:
        return hand[0]


def comp10001go_group(discard_history, player_no):
    "Group my cards from a big list of discard_history, given my player_no"
    hand = []
    value_list = []
    out = []
    # pick my discarded cards from discard_history
    for lst in discard_history:
        hand.append(lst[player_no])
        value_list.append(lst[player_no][0])
    d = Counter(value_list)

    # group first the n of a kind cards
    for (value, freq) in d.items():
        if freq > 1 and value != 'A':
            n_of_a_kind_lst = [card for card in hand
                               if card[0] == value and card[0] != 'A']
            out.append(n_of_a_kind_lst)
            for card in n_of_a_kind_lst:
                hand.remove(card)

    # group run using the remaining cards in hand
    for count in range(len(hand) - 2):
        if len(hand) - count > 0:
            for possible_runs in combinations(hand, len(hand) - count):
                if test_valid_run(list(possible_runs)):
                    runlist = list(possible_runs)
                    handcopy = copy.deepcopy(hand)
                    valid_run = True
                    for card in runlist:
                        if card in handcopy:
                            handcopy.remove(card)
                        # the remaining cards are not sufficient to form a run
                        # as that card is already used in another run
                        else:
                            valid_run = False
                            break
                    if valid_run:
                        for card in runlist:
                            hand.remove(card)
                        out.append(runlist)

    # group the remaining singlets
    for card in hand:
        out.append([card])
    return out