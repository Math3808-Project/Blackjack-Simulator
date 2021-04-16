# MATH 3808 W21 - Final Project
# Author: Nabeel Warsalee
# Date: 14/04/2021
# 
# Class - Player
# Represents the player of the Blackjack game which uses the basic strategy


import definitions
import pydealer

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

        hand (list of Card objects): The hand that the player was given, represented as a list of Card objects

        Returns:

        bool:Whether given hand is soft or not
        """

        for card in hand:
            if card.value == "Ace":
                return True

        return False

    def is_pair(hand, card_type):
        """Checks whether the hand is a pair of a specific type

        Parameters:

        hand (list of Card objects): The hand that the player was given, represented as a list of Card objects

        card_type (string) : The face value to check whether it appears as pair

        Returns:

        bool:Whether given hand is a pair of specific type
        """

        # If hand has more than two cards, automatically cannot be a pair
        if len(hand) > 2:
            return False

        # Go through each card and check whether all cards match to the specific type
        for card in hand:
            if card.value != card_type:
                return False

        # If none of above failed, means we have a pair of the specific type
        return True
        

    def value_to_int(card):
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


    def hand_total(hand):
        """Determine the total of a given hand

        Parameters:

        hand (list of Card objects): The hand that the player was given, represented as a list of Card objects

        Returns:

        list of ints:Totals of current hand
        """
        
        # If the hand is soft, account for two different totals
        if Player.is_soft(hand):
            total = [0, 0]

            for card in hand:
                # Convert card's string value into a numeric value
                val = Player.value_to_int(card.value)

                # Case where we encountered an Ace
                if (val == 1):
                    total[0] += 11
                    total[1] += 1
                else:
                    total[0] += val
                    total[1] += val
            
            return total

        # Hand is hard, return the sum of all card's values
        else:
            total = 0

            for card in hand:
                # Convert card's string value into a numeric value
                val = Player.value_to_int(card.value)

                total += val

            return list(total)
    

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

        # Join all cards together in a string
        hand_str = "|".join(hand)

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

        # Var to store numeric value of dealer's upcard 
        dealer_up_val = Player.value_to_int(dealer_upcard)

        # TODO: Rework basic strategy logic.

        # Case for Hard Hands
        if not Player.is_soft(hand):
            if total in range(5, 8):
                decision = definitions.Actions.HIT
            
            if total == 8:
                if dealer_up_val in range(5, 7):
                    decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.HIT
            
            if total == 9:
                if dealer_up_val in range(2, 7):
                    decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.HIT
            
            if total == 10:
                if dealer_up_val in range(2, 10):
                    decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.HIT
            
            if total == 11:
                decision = definitions.Actions.DOUBLE

            if total == 12:
                if dealer_up_val in range(4, 7):
                    decision = definitions.Actions.STAND
                else:
                    decision = definitions.Actions.HIT
            
            if total in range(13, 17):
                if dealer_up_val in range(2, 7):
                    decision = definitions.Actions.STAND
                else:
                    decision = definitions.Actions.HIT
            
            if total >= 17:
                decision = definitions.Actions.STAND

        # Case for Soft Hands
        else:
            if total in range(13, 17):
                if dealer_up_val in range(4, 7):
                    decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.HIT
            
            if total == 17:
                if dealer_up_val in range(2, 7):
                    decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.HIT

            if total == 18:
                if dealer_up_val in range(3, 7):
                    decision = definitions.Actions.DOUBLE
                elif dealer_up_val in range(9, 11):
                    decision = definitions.Actions.HIT
                else:
                    decision = definitions.Actions.STAND
            
            if total == 19:
                if dealer_up_val == 6:
                    decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.STAND
            
            if total >= 20:
                if total == 21 and len(hand) == 2:
                    decision = definitions.Actions.BLACKJACK
                else:
                    decision = definitions.Actions.STAND
        

        # Case for Splits

        if Player.is_pair(hand, "2"):
            if dealer_up_val in range(2, 8):
                decision = definitions.Actions.SPLIT
            else:
                decision = definitions.Actions.HIT
        
        if Player.is_pair(hand, "3"):
            if dealer_up_val in range(2, 9):
                decision = definitions.Actions.SPLIT
            else:
                decision = definitions.Actions.HIT
        
        if Player.is_pair(hand, "4"):
            if dealer_up_val in range(4, 7):
                decision = definitions.Actions.SPLIT
            else:
                decision = definitions.Actions.HIT
        
        if Player.is_pair(hand, "6"):
            if dealer_up_val in range(2, 8):
                decision = definitions.Actions.SPLIT
            else:
                decision = definitions.Actions.HIT
        
        if Player.is_pair(hand, "7"):
            if dealer_up_val == 9 or dealer_upcard.value == "Ace":
                decision = definitions.Actions.HIT
            elif dealer_up_val == 10:
                decision = definitions.Actions.STAND
            else:
                decision = definitions.Actions.SPLIT
        
        if Player.is_pair(hand, "8"):
            decision = definitions.Actions.SPLIT
        
        if Player.is_pair(hand, "9"):
            if dealer_up_val == 7 or dealer_up_val == 10 or dealer_upcard.value == "Ace":
                decision = definitions.Actions.STAND
            else:
                decision = definitions.Actions.SPLIT

        if Player.is_pair(hand, "Ace"):
            decision = definitions.Actions.SPLIT

        # return determined decision
        return decision




