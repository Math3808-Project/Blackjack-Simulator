# MATH 3808 W21 - Final Project
# Author: Nabeel Warsalee
# Date: 14/04/2021
# 
# Class - Dealer
# Represents the dealer of the Blackjack game which uses the dealer's default strategy

import definitions

class Dealer:
    """Class that represents the Dealer of a BlackJack game
    Dealer will make a decision on their Blackjack hand according to the Dealer's default strategy (stand on 17 above; hit on 16 below)
    
    Parameters:

    dev_mode (bool): Flag that indicates developer mode. In developer mode all debug and print statements will display.

    """

    def __init__(dev_mode=False):
        Dealer.dev_mode = dev_mode
    
    def is_soft(hand):
        """Checks whether an Ace is contained within the given hand, meaning the current hand is a soft hand

        Parameters:

        hand (list of ints): The hand that the player was given, represented as a list of integers

        Returns:

        bool:Whether given hand is soft or not
        """

        return 1 in hand
        

    def hand_total(hand):
        """Determine the total of a given hand

        Parameters:

        hand (list of ints): The hand that the player was given, represented as a list of integers

        Returns:

        list of ints:Totals of current hand
        """
        
        if Dealer.is_soft(hand):
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

        print("Dealer's Cards: {}\nDealer's Decision: {}".format(hand_str, decision))
    
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
        
        # If dev mode set, print out dealer's hand and resultant decision
        if Dealer.dev_mode:
            Dealer.print_decision(hand, decision)

        return decision
        