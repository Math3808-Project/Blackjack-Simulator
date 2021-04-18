import pydealer
import definitions
import player
import dealer

class Game:
    """
    A class used to compute the result of a blackjack game
    """

    def __init__(self, dev_mode=False):
        self.dev_mode = dev_mode
        self.player = player.Player(dev_mode)
        self.dealer = dealer.Dealer(dev_mode)

    def game_result(self, bet=1, player_hand=None, dealer_hand=None, deck=None):
        """
        Simulates a game of Blackjack and returns the betting result 

        Parmeters
        ---------
        bet : int, optional
            The initial betting amount
            Default betting value is 1 unit

        player_hand : Card list, optional
            The preset player hand
            
        dealer_hand : Card list, optional
            The preset dealer hand      

        deck : Deck of cards, optional
            The current deck of cards in play   

        Returns
        -------
        A float value representing the player net amount, initial bet included
        """

        # create deck if not inputted 
        if deck is None:
            deck = pydealer.Deck()
            deck.shuffle()

        # condition for split aces 
        split_aces = False

        # draw player hand if hand not inputted
        if player_hand is None:
            player_hand = deck.deal(2)
       
        # add second card to player hand for a split
        if player_hand.size < 2:
            # check for split aces 
            if player_hand[0].value == "Ace":
                split_aces = True

            player_hand.add(deck.deal())

        # add dealer upcard 
        if dealer_hand is None:
            dealer_hand = deck.deal()

        # for testing
        if self.dev_mode:
            self.print_info(player_hand, dealer_hand, deck.size)

        player_action = self.player.compute_play(player_hand, dealer_hand[0], split_aces)
            
        # check for player Blackjack with initial hand
        if player_action == definitions.Actions.BLACKJACK:
            
            # check if dealer also has Blackjack -> tie
            if dealer_hand.size == 1:
                dealer_hand.add(deck.deal())

            if self.dealer.compute_play(dealer_hand) == definitions.Actions.BLACKJACK:
                return 0

            # player gets 1.5 to 1 payout for Blackjack
            return 1.5 * bet

        else:
            # handle player decisions

            # hit
            while player_action == definitions.Actions.HIT:
                # add card to player hand
                player_hand.add(deck.deal())

                # player busts on this draw and loses betting amount
                if self.player.hand_sum(player_hand) > 21:
                    return -1 * bet

                player_action = self.player.compute_play(player_hand, dealer_hand[0], split_aces)

            # double
            if player_action == definitions.Actions.DOUBLE:
                # add single card to player hand
                player_hand.add(deck.deal())
                bet *= 2

                # player busts on this draw and loses betting amount
                if self.player.hand_sum(player_hand) > 21:
                    return -1 * bet

            # split
            if player_action == definitions.Actions.SPLIT:
                # make recursive calls and add the results of each hand
                result  = self.game_result(bet, pydealer.Stack(cards = [player_hand[0]]), dealer_hand, deck)
                result += self.game_result(bet, pydealer.Stack(cards = [player_hand[1]]), dealer_hand, deck)
                return result

        while True:
            # handle dealer decisions and final game outcome per draw 
            # precondition: player's hand is not busted

            dealer_action = self.dealer.compute_play(dealer_hand)

            # hit, add card to dealer hand
            if dealer_action == definitions.Actions.HIT:
                dealer_hand.add(deck.deal())

            # blackjack for dealer and not player, player loses betting amount
            elif dealer_action == definitions.Actions.BLACKJACK:
                return -1 * bet

            # stand
            elif dealer_action == definitions.Actions.STAND:
                dealer_sum = self.dealer.hand_sum(dealer_hand)
                player_sum = self.player.hand_sum(player_hand)

                # dealer busts, player wins bet amount 3 to 2
                if dealer_sum > 21:
                    return 1.5 * bet

                # player has higher hand, player wins bet amount 3 to 2
                elif player_sum > dealer_sum:
                    return 1.5 * bet

                # tie, player neither gains nor loses bet amount
                elif player_sum == dealer_sum:
                    return 0

                # dealer has higher hand, player loses their bet
                else:
                    return -1 * bet

    def print_info(self, player_hand, dealer_hand, num_cards):
        """
        Prints the information for the start of a blackjack round

        Parmeters
        ---------
        player_hand : Card list
            The  player hand
            
        dealer_hand : Card list
            The  dealer hand      

        num_cards : int
            The number of cards remaining in the deck

        Returns
        -------
        void
        """

        print("~~~Starting Player Hand~~~")
        print(player_hand)
        print("\n~~~Starting Dealer Hand~~~")
        print(dealer_hand)     
        print("\n~~~Starting Deck Size~~~\n{}".format(num_cards))