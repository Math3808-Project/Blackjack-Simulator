# MATH 3808 W21 - Final Project
# Author: Nabeel Warsalee
# Date: 14/04/2021
# 
# Class - Player
# Represents the player of the Blackjack game which uses the basic strategy


# import definitions # TODO: Uncomment once definitions.py is included in project files 

class Player:
    def __init__():
        # foo, idk what to do here atm
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
        
        return sum(hand)

    def compute_play(hand, dealer_upcard):
        """Computes the player's decision based on their given BlackJack hand

        Parameters:

        hand (list of ints): The hand that the player was given, represented as a list of integers

        Returns:

        enum:Decision for player's current hand of cards

        """

        # Var to store the player's decision for the current hand of cards 
        decision = "hit"


        # TODO: Rework conditional logic

        if Player.hand_total(hand) in range(12, 17) and dealer_upcard in range(2, 7):
            # Exception case: HIT on 12 vs 2 or 3
            if Player.hand_total(hand) == 12 and dealer_upcard in range(2, 4):
                decision = "hit"
            else:
                decision = "stand"
        else:
            decision = "hit"

        if Player.is_soft(hand) and Player.hand_total(hand) == 17:
            decision = "hit"

        elif Player.is_soft(hand) and Player.hand_total(hand) == 17 and dealer_upcard in range(9, 11):
            decision = "hit"

        # DOUBLE DOWN, set of cases

        if Player.hand_total(hand) == 11:
            decision = "double-down"

        elif Player.hand_total(hand) == 10 and dealer_upcard in range(2, 10):
            decision = "double-down"
        
        elif Player.hand_total(hand) == 9 and dealer_upcard in range(2, 7):
            decision = "double-down"

        elif Player.hand_total(hand) == 8 and dealer_upcard in range(5, 7):
            decision = "double-down"

        # SPLIT, set of cases

        # If pair of Aces or pair of 8's, always split
        if Player.is_pair(hand, 1) or Player.is_pair(hand, 8):
            decision = "split"

        elif Player.is_pair(hand, 2) and dealer_upcard in range(3, 8):
            decision = "split"

        elif Player.is_pair(hand, 3) and dealer_upcard in range(3, 8):
            decision = "split"
        
        elif Player.is_pair(hand, 6) and dealer_upcard in range(2, 7):
            decision = "split"
        
        elif Player.is_pair(hand, 7) and dealer_upcard in range(2, 8):
            decision = "split"
        
        elif Player.is_pair(hand, 9) and dealer_upcard in range(2, 9):
            if dealer_upcard != 7:
                decision = "split"
        
        #elif Player.is_pair(hand, 4) or Player.is_pair(hand, 5) or Player.is_pair(hand, 10):
        #    decision = "stand"




