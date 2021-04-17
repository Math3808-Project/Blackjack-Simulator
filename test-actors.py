# MATH 3808 W21 - Final Project
# Author: Nabeel Warsalee
# Date: 14/04/2021
# 
# Testing Player and Dealer classes

import pydealer

import player
import dealer
import definitions


def main():
    # construct deck of 52 cards
    deck = pydealer.Deck()

    pl = player.Player(dev_mode=True)
    dlr = dealer.Dealer(dev_mode=True)

    # testing value_to_int function
    #for card in deck:
    #    print("{} | {}".format(card, pl.value_to_int(card))) 

    # shuffle the cards
    deck.shuffle()

    # testing hand_total & valid_total function
    hand = deck.deal(2)

    return_total = pl.valid_total(pl.hand_total(hand))

    print("{} | Total: {}".format(hand, return_total))

    # testing valid_total function

    hand2 = deck.deal(3)

    return_total2 = pl.valid_total(pl.hand_total(hand2))

    print("{} | Total: {}".format(hand2, return_total2))

    print()
    print()

    # testing compute_hand function

    pl.compute_play(hand, hand2[0])

if __name__ == "__main__":
    main()