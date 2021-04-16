# MATH 3808 W21 - Final Project
# Author: Nabeel Warsalee
# Date: 14/04/2021
# 
# Class - Player
# Represents the player of the Blackjack game which uses the basic strategy


import definitions

class Player:
    """Class that represents the Player of a BlackJack game (excl. Dealer)
    Player will make a decision on their Blackjack hand according to the Basic Strategy.
    
    Parameters:

    dev_mode (bool): Flag that indicates developer mode. In developer mode all debug and print statements will display.

    """
    def __init__(dev_mode=False):
        Player.dev_mode = dev_mode

    
    def is_soft(hand):
        """Checks whether an Ace is contained within the given hand, meaning the current hand is a soft hand

        Parameters:

        hand (list of ints): The hand that the player was given, represented as a list of integers

        Returns:

        bool:Whether given hand is soft or not
        """

        return 1 in hand

    def is_pair(hand, card_type):
        """Checks whether the hand is a pair of a specific type

        Parameters:

        hand (list of ints): The hand that the player was given, represented as a list of integers

        card_type (int) : The face value to check whether it appears as pair (i.e. if type=3, then check if hand is pair 3)

        Returns:

        bool:Whether given hand is a pair of specific type
        """

        # If hand has more than two cards, automatically cannot be a pair
        if len(hand) > 2:
            return False

        # Go through each card and check whether all cards match to the specific type
        for card in hand:
            if card != card_type:
                return False

        # If none of aboce failed, means we have a pair of the specific type
        return True
        


    def hand_total(hand):
        """Determine the total of a given hand

        Parameters:

        hand (list of ints): The hand that the player was given, represented as a list of integers

        Returns:

        int:Total of current hand
        """
        
        if Player.is_soft(hand):
            total = [0, 0]

            for val in hand:
                # Case where we encountered an Ace
                if (val == 1):
                    total[0] += 11
                    total[1] += 1
                else:
                    total[0] += val
                    total[1] += val
            
            return total

        else:
            return list(sum(hand))
    

    def valid_total(totals):
        """Determine what total to return

        Parameters:

        total (list of ints): The different totals that can represent a hand

        Return:

        int:The proper total from the given totals
        """
        if len(totals) == 1:
            return totals[0]
        
        else:
            curr_max = max(totals)
            curr_min = min(totals)

            # error case
            if curr_max > 21 and curr_min > 21:
                return None
            
            if curr_max > 21:
                return curr_min
            else:
                return curr_max
    

    def print_decision(hand, decision):
        """Print out current hand and decision that is given

        Parameters:

        hand (list of ints): The hand that the player was given, represented as a list of integers

        decision (Actions enum): Decision that was made by the player

        Returns:

        void
        """

        # Reformatting hand structure such that Aces show up as A and not 1
        formatted_hand = []
        for val in hand:
            if val == 1:
                formatted_hand.append("A")
            else:
                formatted_hand.append(str(val))
        
        hand_str = "|".join(formatted_hand)

        print("Player's Cards: {}\nPlayer's Decision: {}".format(hand_str, decision))


    def compute_play(hand, dealer_upcard):
        """Computes the player's decision based on their given BlackJack hand (uses Basic Strategy)

        Parameters:

        hand (list of ints): The hand that the player was given, represented as a list of integers

        dealer_upcard (int): The value of the dealer's exposed card

        Returns:

        enum:Decision for player's current hand of cards

        """

        # Var to store the player's decision for the current hand of cards 
        decision = definitions.Actions.HIT

        # Var to store hand total
        total = Player.valid_total(Player.hand_total(hand))

        # Case for all Hard hands (i.e. no Ace in hand)
        if not Player.is_soft(hand):
            # if total less than 11, always hit
            if total <= 11:
                decision = definitions.Actions.HIT
            # if total 12, check dealer's upcard for specific cases
            if total == 12:
                if dealer_upcard in range(4, 7):
                    decision = definitions.Actions.STAND
                
                # Execption, Always hit on total 12 with dealer upcard of 2 or 3
                if dealer_upcard in range(2, 4):
                    decision = definitions.Actions.HIT

            # Case where total between 13-16 and dealer upcard is 2-6 (stand case)
            if total in range(13, 17) and dealer_upcard in range (2, 7):
                decision = definitions.Actions.STAND

            if total in range(13, 17) and dealer_upcard > 6:
                decision = definitions.Actions.HIT
            
            # ALways stand on total 17 or higher
            if total >= 17:
                decision = definitions.Actions.STAND

        # Case for all Soft hands (i.e. no Ace in hand)
        else:

            if total <= 17:
                decision = definitions.Actions.HIT
            
            if total == 18 and dealer_upcard <= 8:
                decision = definitions.Actions.STAND
            
            if total == 18 and dealer_upcard in range(9, 11):
                decision = definitions.Actions.HIT

            if total > 18:
                decision = definitions.Actions.STAND

        # DOUBLE DOWN, set of cases

        if total == 11:
            decision = definitions.Actions.DOUBLE

        elif total == 10 and dealer_upcard in range(2, 10):
            decision = definitions.Actions.DOUBLE
        
        elif total == 9 and dealer_upcard in range(2, 7):
            decision = definitions.Actions.DOUBLE

        elif total == 8 and dealer_upcard in range(5, 7):
            decision = definitions.Actions.DOUBLE

        # SPLIT, set of cases

        # If pair of Aces or pair of 8's, always split
        if Player.is_pair(hand, 1) or Player.is_pair(hand, 8):
            decision = definitions.Actions.SPLIT

        elif Player.is_pair(hand, 2) and dealer_upcard in range(3, 8):
            decision = definitions.Actions.SPLIT

        elif Player.is_pair(hand, 3) and dealer_upcard in range(3, 8):
            decision = definitions.Actions.SPLIT
        
        elif Player.is_pair(hand, 6) and dealer_upcard in range(2, 7):
            decision = definitions.Actions.SPLIT
        
        elif Player.is_pair(hand, 7) and dealer_upcard in range(2, 8):
            decision = definitions.Actions.SPLIT
        
        elif Player.is_pair(hand, 9) and dealer_upcard in range(2, 9):
            if dealer_upcard != 7:
                decision = definitions.Actions.SPLIT

        # If dev mode set, print out dealer's hand and resultant decision
        if Player.dev_mode:
            Player.print_decision(hand, decision)

        # return determined decision
        return decision




