import definitions
import pydealer
import numpy as np

class Game:
    """
    A class used to compute the result of a blackjack game
    """

    def __init__(self, dev_mode=False):
        self.dev_mode = dev_mode

    def blackjack_game_result(self, bet=1, player_hand=0, dealer_upcard=0):
        """
        Simulates a game of Blackjack and returns the betting result 

        Parmeters
        ---------
        bet : int, optional
            The initial betting amount
            Default betting value is 1 unit

        player_hand : Card list, optional
            The preset player hand, used for splits
            
        dealer_upcard : Card, optional
            The preset dealer upcard         

        Returns
        -------
        An integer value representing the player net amount, initial bet included
        """

        # create deck
        deck = pydealer.Deck()
        deck.shuffle()

        # init dealer hand 
        dealer_hand = pydealer.Stack()

        # condition for split aces 
        split_aces = False;

        # draw player hand if hand not inputted
        if player_hand == 0:
            player_hand = deck.deal(2)
        
        # split aces 
        if player_hand.size == 1 and player_hand[0].value == "Ace":
            split_aces = True

        # add second card to player hand following split condition
        if player_hand.size < 2:
            player_hand.add(deck.deal())

        # add dealer upcard 
        if dealer_upcard == 0:
            dealer_upcard = deck.deal()[0]

        dealer_hand.add(dealer_upcard)        

        if split_aces == False:
            
            # check for player Blackjack with initial hand
            pass

bj = Game()
bj.blackjack_game_result(1)