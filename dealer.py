# MATH 3808 W21 - Final Project
# Author: Nabeel Warsalee
# Date: 14/04/2021
# 
# Class - Dealer
# Represents the dealer of the Blackjack game which uses the dealer's default strategy

import definitions

class Dealer:
    def __init__():
        # don't know what to put here...
        return
    
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
        
        if Dealer.is_soft(hand):
            total = [0, 0]

            for val in hand:
                # Case where we encountered an Ace
                if (val == 1):
                    total[0] += 10
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
            
    
    def compute_play(hand):
        """Computes the dealer's decision based on their given BlackJack hand

        Parameters:

        hand (list of ints): The hand that the player was given, represented as a list of integers

        Returns:

        enum:Decision for dealer's current hand of cards

        """

        # Var to store the player's decision for the current hand of cards 
        decision = definitions.Actions.STAND

        # Var to store hand total
        total = Dealer.valid_total(Dealer.hand_total(hand))

        # any total less than 17 dealer hits
        if total < 17:
            decision = definitions.Actions.HIT
        
        return decision
        