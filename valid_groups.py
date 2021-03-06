def comp10001go_valid_groups(groups):
    """input a list of groups to determine
    if all groups in the list are valid"""
    
    if not groups:
        return True
    valid = True
    translate = {'1': 1, '2': 2, '3': 3, '4': 4,
                 '5': 5, '6': 6, '7': 7, '8': 8,
                 '9': 9,
                 'J': 11, 'Q': 12, 'K': 13, '0': 10}
    translate2 = {'C': 'B', 'S': 'B', 'H': 'R', 'D': 'R'}
    for group in groups:
        # if group is empty or is singlet 
        if len(group) == 0 or len(group) == 1:
            valid = True
        else:
            # split the lists of cards into an aces list and a non_aces list
            aces = []
            non_aces = []
            for card in group:
                if card in ('AS', 'AD', 'AH', 'AC'):
                    aces.append((card[0], translate2[card[1]]))
                else:
                    non_aces.append((translate[card[0]], translate2[card[1]]))
            non_aces = sorted(non_aces)
            # n of a kind validation
            n_of_a_kind = False
            if len(non_aces) >= 2 and not aces:
                for card in non_aces:
                    if card[0] != non_aces[0][0]:
                        n_of_a_kind = False
                        break
                    else:
                        n_of_a_kind = True
            if n_of_a_kind:
                valid = True
                
            # n of a kind is False, check run
            else:
                valid = False
                if len(group) < 3:
                    return False
                else:
                    run = True
                    # loop through the list to check a non-Ace card and its
                    # preceding card to see if their value difference and 
                    # colour satisfy the requirement for a run. If not,
                    # check if there are Aces that can be used to 
                    # replace the card. Remove Aces that are used in the run.
                    for count in range(len(non_aces) - 1):
                        diff = non_aces[count + 1][0] - non_aces[count][0]
                        if diff == 0:
                            run = False
                        elif diff == 1:
                            if non_aces[count][1] == non_aces[count + 1][1]:
                                run = False
                                break
                        else:
                            if not aces:
                                run = False
                                break
                            if diff == 2:
                                if (non_aces[count][1] != 
                                    non_aces[count + 1][1]):
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
                                if (non_aces[count][1] == 
                                    non_aces[count + 1][1]):
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
                                if (non_aces[count][1] != 
                                    non_aces[count + 1][1]):
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
                                if (non_aces[count][1] == 
                                non_aces[count + 1][1]):
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
                    if aces:
                        run = False
                    if not run:
                        return False
                    else:
                        valid = True
    return valid