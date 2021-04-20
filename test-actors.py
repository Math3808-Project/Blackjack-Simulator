# MATH 3808 W21 - Final Project
# Author: Nabeel Warsalee
# Date: 14/04/2021
# 
# Testing Player and Dealer classes

from random import randint
import pydealer

import player
import dealer
import definitions

card_values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

card_suits = ["Clubs", "Hearts", "Spades", "Diamonds"]

def test_all_2card_hands(pl, dlr):
    """Function to test all 2 card hands for the compute_play function
       Goes through all possible combinations and outputs the results to a file.

    Parameters:

    pl (Player Object) : Instance of player class to use compute_play function

    dlr (Dealer Object) : Instance of dealer class to use compute_play function

    Returns:

    None
    """
    # open file for dumping test information
    f = open("test_player_basic_strat.txt", "w")
    f2 = open("test_dealer_strat.txt", "w")

    # traverse card values for making the player's first card
    for i in card_values:

        # traverse card values for making the player's second card
        for j in card_values:
            # crafting player's hand
            pl_hand = [pydealer.Card(i, card_suits[randint(0, 3)]), pydealer.Card(j, card_suits[randint(0, 3)])]

            # player card string
            plr_card_str = "Player's Hand: "

            for card in pl_hand:
                plr_card_str += str(card) + " | "
                
            plr_card_str = plr_card_str[:-3]

            # If pair currently, make note of that
            if pl_hand[0].value == pl_hand[1].value:
                plr_card_str += "  (Pairs)"

            plr_card_str += "\n"

            f.write("-----------[ {} ]-----------\n\n".format(plr_card_str.strip("\n")))

            # compute dealer's decision and print to it's own file
            dlr_decision = dlr.compute_play(pl_hand)
            f2.write("-----------[ {} ]-----------\n".format(plr_card_str.strip("\n").replace("Player", "Dealer")))
            f2.write("   Decision: {}\n\n".format(dlr_decision))

            # traverse card values for making the dealer's upcard
            for k in card_values:
                # craft dealer's upcard
                dlr_upcard = pydealer.Card(k, card_suits[randint(0, 3)])

                # check compute play result
                decision = pl.compute_play(pl_hand, dlr_upcard)

                dlr_upcard_str = "Dealer's Upcard: {}\n".format(dlr_upcard)

                # Write results to file
                f.write(plr_card_str)
                f.write(dlr_upcard_str)
                f.write("Decision: {}\n".format(decision))
                f.write("\n")
            
        
        f.write("&==================================================================================================\n\n")
        
    f.close()
    f2.close()
    print("done 2 card hand testing...")

def test_ace_counting(plr):
    """Function to test ace counting in a blackjack hand
    
    Parameters:

    plr (Player Object) : Instance of player class to use compute_play function

    Returns:

    None
    """

    # Create a 3 card hand of cards
    hand = pydealer.Stack(cards = [
                pydealer.Card("Ace", card_suits[randint(0, 3)]),
                pydealer.Card("5", card_suits[randint(0, 3)]),
                pydealer.Card("3", card_suits[randint(0, 3)])
           ])
    
    print("Player's Cards:")
    print(hand)
    print("Hand total: {}".format(plr.hand_sum(hand)))
    print("Soft? {}\n".format(plr.is_soft(hand)))
    

    hand2 = pydealer.Stack(cards = [
                pydealer.Card("Ace", card_suits[randint(0, 3)]),
                pydealer.Card("5", card_suits[randint(0, 3)]),
                pydealer.Card("Ace", card_suits[randint(0, 3)])
            ])

    print("Player's Cards:")
    print(hand2)
    print("Hand total: {}".format(plr.hand_sum(hand2)))
    print("Soft? {}\n".format(plr.is_soft(hand2)))

    hand3 = pydealer.Stack(cards = [
                pydealer.Card("Ace", card_suits[randint(0, 3)]),
                pydealer.Card("5", card_suits[randint(0, 3)]),
                pydealer.Card("Ace", card_suits[randint(0, 3)]),
                pydealer.Card("8", card_suits[randint(0, 3)])
            ])

    print("Player's Cards:")
    print(hand3)
    print("Hand total: {}".format(plr.hand_sum(hand3)))
    print("Soft? {}\n".format(plr.is_soft(hand3)))

    hand4 = pydealer.Stack(cards = [
                pydealer.Card("4", card_suits[randint(0, 3)]),
                pydealer.Card("6", card_suits[randint(0, 3)]),
                pydealer.Card("Ace", card_suits[randint(0, 3)])
            ])

    print("Player's Cards:")
    print(hand4)
    print("Hand total: {}".format(plr.hand_sum(hand4)))
    print("Soft? {}\n".format(plr.is_soft(hand4)))

    hand4 = pydealer.Stack(cards = [
                pydealer.Card("4", card_suits[randint(0, 3)]),
                pydealer.Card("6", card_suits[randint(0, 3)]),
                pydealer.Card("Ace", card_suits[randint(0, 3)]),
                pydealer.Card("Ace", card_suits[randint(0, 3)])
            ])

    print("Player's Cards:")
    print(hand4)
    print("Hand total: {}".format(plr.hand_sum(hand4)))
    print("Soft? {}\n".format(plr.is_soft(hand4)))

    print("done testing ace counting...")

def main():
    # construct deck of 52 cards
    deck = pydealer.Deck()

    # init dealer and player classes
    pl = player.Player()
    dlr = dealer.Dealer()

    # randomize deck aka shuffle
    deck.shuffle()

    # call function to test all 2 card hands
    test_all_2card_hands(pl, dlr)
    
    # call function to test ace counting
    #test_ace_counting(pl)

    print("done testing...")


if __name__ == "__main__":
    main()