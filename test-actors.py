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

def main():
    # construct deck of 52 cards
    deck = pydealer.Deck()

    pl = player.Player()
    dlr = dealer.Dealer()

    # testing value_to_int function
    #for card in deck:
    #    print("{} | {}".format(card, pl.value_to_int(card))) 

    # shuffle the cards
    deck.shuffle()

    # testing hand_total & valid_total function
    hand = deck.deal(2)

    return_total = pl.valid_total(pl.hand_total(hand))

    #print("{} | Total: {}".format(hand, return_total))

    # testing valid_total function

    hand2 = deck.deal(3)

    return_total2 = pl.valid_total(pl.hand_total(hand2))

    #print("{} | Total: {}".format(hand2, return_total2))

    #print()
    #print()

    # testing compute_hand function

    #pl.compute_play(hand, hand2[0])

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
    print("done testing...")

    

if __name__ == "__main__":
    main()