# MATH 3808 W21 - Final Project
# Author: Nabeel Warsalee
# Date: 14/04/2021
# 
# Class - Dealer
# Represents the dealer of the Blackjack game which uses the dealer's default strategy

import definitions
import pydealer

class Dealer:
    """Class that represents the Dealer of a BlackJack game
    Dealer will make a decision on their Blackjack hand according to the Dealer's default strategy (stand on 17 above; hit on 16 below)
    
    Parameters:

    dev_mode (bool): Flag that indicates developer mode. In developer mode all debug and print statements will display.

    """

    def __init__(self, dev_mode=False):
        self.dev_mode = dev_mode
    
    def has_ace(self, hand):
        """Checks whether an Ace is contained within the given hand, meaning the current hand is a soft hand

        Parameters:

        hand (list of Card objects): The hand that the dealer was given, represented as a list of Card objects

        Returns:

        bool:Whether given hand is soft or not
        """

        for card in hand:
            if card.value == "Ace":
                return True

        return False
        

    def value_to_int(self, card):
        """Function to translate a card's value to a numeric value (i.e., value: "2" --> 2, value: "King" --> 10)

        Parameters:

        card (Card object): Card to translate its value into a number

        Return:

        int:Numeric value of given card
        """

        # If K, J or Q, return value 10
        if card.value in ["King", "Queen", "Jack"]:
            return 10
        # If Ace, return value 1 (value 11 checked in hand_total function)
        elif card.value == "Ace":
            return 1
        # Otherwise, cast value into an int and return that (ex. card.value="2" --> return 2)
        else:
            return int(card.value)


    def hand_total(self, hand):
        """Determine the total of a given hand

        Parameters:

        hand (list of Card objects): The hand that the Dealer was given, represented as a list of Card objects

        Returns:

        list of ints:Totals of current hand
        """
        
        # If the hand has an ace, account for two different totals
        if self.has_ace(hand):
            total = [0, 0]

            # var to store number of aces that are to be considered as 11 in the final total
            num_of_full_aces = 1

            for card in hand:
                # Convert card's string value into a numeric value
                val = self.value_to_int(card)

                # Case where we encountered an Ace
                if (val == 1):
                    # If current Ace is the first ace we have seen, consider it with value 11 in calculations
                    if num_of_full_aces > 0:
                        total[0] += 11
                        num_of_full_aces -= 1
                    # Otherwise, this is not the first Ace we've seen meaning we should consider its value 1 so as not to bust the total
                    else:
                        total[0] += 1

                    # Increase the smaller total with value 1
                    total[1] += 1
                else:
                    total[0] += val
                    total[1] += val
            
            return total

        # Hand has no ace, return the sum of all card's values
        else:
            total = 0

            for card in hand:
                # Convert card's string value into a numeric value
                val = self.value_to_int(card)

                total += val

            return [total]
    
    def valid_total(self, totals):
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

            if curr_max > 21 and curr_min > 21:
                return curr_min
            
            if curr_max > 21:
                return curr_min
            else:
                return curr_max

    def hand_sum(self, hand):
        """
        Generates the numerical sum of a playing hand

        Parmeters
        ---------
        hand : Card list
            The hand to calculate

        Returns
        -------
        int : An integer representing the numerical sum of a blackjack hand
        """

        return self.valid_total(self.hand_total(hand))
            
    def print_decision(self, hand, decision):
        """Print out current hand and decision that is given

        Parameters:

        hand (list of ints): The hand that the player was given, represented as a list of integers

        decision (Actions enum): Decision that was made by the player

        Returns:

        void
        """

        print("\n___Dealer's Cards___\n{}\nDealer's Decision: {}".format(hand, decision))
    
    def compute_play(self, hand):
        """Computes the dealer's decision based on their given BlackJack hand

        Parameters:

        hand (list of ints): The hand that the player was given, represented as a list of integers

        Returns:

        enum:Decision for dealer's current hand of cards

        """

        # Var to store the player's decision for the current hand of cards 
        decision = definitions.Actions.STAND

        # Var to store hand total
        total = self.hand_sum(hand)

        # any total less than 17 dealer hits
        if total < 17:
            decision = definitions.Actions.HIT
        
        # check for blackjack
        if total == 21 and len(hand) == 2:
            decision = definitions.Actions.BLACKJACK

        # If dev mode set, print out dealer's hand and resultant decision
        if self.dev_mode:
            self.print_decision(hand, decision)

        return decision
        