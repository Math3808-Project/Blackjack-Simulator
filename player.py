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
    def __init__(self, dev_mode=False):
        self.dev_mode = dev_mode

    
    def has_ace(self, hand):
        """Checks whether an Ace is contained within the given hand

        Parameters:

        hand (list of Card objects): The hand that the player was given, represented as a list of Card objects

        Returns:

        bool:Whether given hand contains an Ace
        """

        for card in hand:
            if card.value == "Ace":
                return True

        return False

    def is_soft(self, hand):
        """Checks whether the given hand is soft (has an Ace counted as 11)

        Parameters:

        hand (list of Card objects): The hand that the player was given, represented as a list of Card objects

        Returns:

        bool:Whether given hand is soft
        """
        if not self.has_ace(hand) or self.hand_total(hand)[0] != self.hand_sum(hand):
            return False

        return True


    def is_pair(self, hand, card_type):
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

        hand (list of Card objects): The hand that the player was given, represented as a list of Card objects

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
            hand_sum = 0

            for card in hand:
                # Convert card's string value into a numeric value
                val = self.value_to_int(card)

                hand_sum += val

            return [hand_sum]
    

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
    
    def print_decision(self, hand, dealers, decision):
        """Print out current hand and decision that is given

        Parameters:

        hand (list of Card objects): The hand that the player was given, represented as a list of Card objects

        dealers (Card object): The Dealer's upcard

        decision (Actions enum): Decision that was made by the player

        Returns:

        void
        """

        print("\n___Player's Cards___\n{}\nDealer's Up Card: {} \nPlayer's Decision: {}".format(hand, dealers, decision))


    def compute_play(self, hand, dealer_upcard, split_aces=False):
        """Computes the player's decision based on their given BlackJack hand (uses Basic Strategy)

        Parameters:

        hand (list of Card Objects): The hand that the player was given, represented as a list of Card objects

        dealer_upcard (Card Object): The value of the dealer's exposed card, as a Card object

        Returns:

        enum:Decision for player's current hand of cards

        """

        # Var to store the player's decision for the current hand of cards 
        decision = definitions.Actions.NONE

        # Var to store hand total
        total = self.hand_sum(hand)

        # Var to store numeric value of dealer's upcard 
        dealer_up_val = self.value_to_int(dealer_upcard)

        # Case for Hard Hands
        if not self.is_soft(hand):
            if total in range(5, 8):
                decision = definitions.Actions.HIT
            
            if total == 8:
                if dealer_up_val in range(5, 7):
                    if split_aces or not len(hand) == 2:
                        decision = definitions.Actions.HIT
                    else:
                        decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.HIT
            
            if total == 9:
                if dealer_up_val in range(2, 7):
                    if split_aces or not len(hand) == 2:
                        decision = definitions.Actions.HIT
                    else:
                        decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.HIT
            
            if total == 10:
                if dealer_up_val in range(2, 10):
                    if split_aces or not len(hand) == 2:
                        decision = definitions.Actions.HIT
                    else:
                        decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.HIT
            
            if total == 11:
                if split_aces or not len(hand) == 2:
                    decision = definitions.Actions.HIT
                else:
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
                    if split_aces or not len(hand) == 2:
                        decision = definitions.Actions.HIT
                    else:
                        decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.HIT
            
            if total == 17:
                if dealer_up_val in range(2, 7):
                    if split_aces or not len(hand) == 2:
                        decision = definitions.Actions.HIT
                    else:
                        decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.HIT

            if total == 18:
                if dealer_up_val in range(3, 7):
                    if split_aces or not len(hand) == 2:
                        decision = definitions.Actions.STAND
                    else:
                        decision = definitions.Actions.DOUBLE
                elif dealer_up_val in range(9, 11):
                    decision = definitions.Actions.HIT
                else:
                    decision = definitions.Actions.STAND
            
            if total == 19:
                if dealer_up_val == 6:
                    if split_aces or not len(hand) == 2:
                        decision = definitions.Actions.STAND
                    else:
                        decision = definitions.Actions.DOUBLE
                else:
                    decision = definitions.Actions.STAND
            
            if total >= 20:
                if total == 21 and len(hand) == 2 and not split_aces:
                    decision = definitions.Actions.BLACKJACK
                else:
                    decision = definitions.Actions.STAND
        

        # Case for Splits

        if self.is_pair(hand, "2"):
            if dealer_up_val in range(2, 8):
                decision = definitions.Actions.SPLIT
            else:
                decision = definitions.Actions.HIT
        
        if self.is_pair(hand, "3"):
            if dealer_up_val in range(2, 9):
                decision = definitions.Actions.SPLIT
            else:
                decision = definitions.Actions.HIT
        
        if self.is_pair(hand, "4"):
            if dealer_up_val in range(4, 7):
                decision = definitions.Actions.SPLIT
            else:
                decision = definitions.Actions.HIT
        
        if self.is_pair(hand, "6"):
            if dealer_up_val in range(2, 8):
                decision = definitions.Actions.SPLIT
            else:
                decision = definitions.Actions.HIT
        
        if self.is_pair(hand, "7"):
            if dealer_up_val == 9 or dealer_upcard.value == "Ace":
                decision = definitions.Actions.HIT
            elif dealer_up_val == 10:
                decision = definitions.Actions.STAND
            else:
                decision = definitions.Actions.SPLIT
        
        if self.is_pair(hand, "8"):
            decision = definitions.Actions.SPLIT
        
        if self.is_pair(hand, "9"):
            if dealer_up_val == 7 or dealer_up_val == 10 or dealer_upcard.value == "Ace":
                decision = definitions.Actions.STAND
            else:
                decision = definitions.Actions.SPLIT

        if self.is_pair(hand, "Ace"):
            decision = definitions.Actions.SPLIT

        # If dev mode set, print out dealer's hand and resultant decision
        if self.dev_mode:
            self.print_decision(hand, dealer_upcard, decision)

        if decision == definitions.Actions.NONE:
            raise Exception("Actions value is NONE...")

        # return determined decision
        return decision




