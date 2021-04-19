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

        # initialize the dictionary storing game result data
        game_info = self.init_dict()

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

        # draw dealer hand 
        if dealer_hand is None:
            dealer_hand = deck.deal(2)

        # for testing
        if self.dev_mode:
            self.print_info(player_hand, dealer_hand, deck.size)

        # the initial action for the player and dealer
        player_action = self.player.compute_play(player_hand, dealer_hand[0], split_aces)
        dealer_action = self.dealer.compute_play(dealer_hand)
            
        # check for player Blackjack with initial hand
        if player_action == definitions.Actions.BLACKJACK:
            # check if dealer also has Blackjack -> tie
            game_info["player_sum"] = [21]
            game_info["dealer_sum"] = self.dealer.hand_sum(dealer_hand)

            if dealer_action == definitions.Actions.BLACKJACK:
                game_info["result"] = 0
                return game_info

            # player gets 1.5 to 1 payout for Blackjack
            game_info["result"] = 1.5 * bet
            return game_info

        # checks for dealer blackjack with initial hand
        elif dealer_action == definitions.Actions.BLACKJACK:
            game_info["player_sum"] = self.player.hand_sum(player_hand)
            game_info["dealer_sum"] = 21
            game_info["result"] = -1 * bet

            return game_info

        else:
            # handle player decisions

            # hit
            while player_action == definitions.Actions.HIT and not split_aces:
                # add card to player hand
                player_hand.add(deck.deal())

                player_sum = self.player.hand_sum(player_hand)

                # player busts on this draw and loses betting amount
                if player_sum > 21:
                    game_info["player_sum"] = [player_sum]
                    game_info["result"] = -1 * bet

                    # for testing
                    if self.dev_mode:
                        print("\n___Player's Cards After Bust___\n{}".format(player_hand))

                    return game_info

                player_action = self.player.compute_play(player_hand, dealer_hand[0], split_aces)

            # double
            if player_action == definitions.Actions.DOUBLE:
                game_info["double_down"] = True

                # add single card to player hand
                player_hand.add(deck.deal())
                bet *= 2

                # for testing
                if self.dev_mode:
                    print("\n___Player's Cards After Bust___\n{}".format(player_hand))

                player_sum = self.player.hand_sum(player_hand)

                # player busts on this draw and loses betting amount
                if player_sum > 21:
                    game_info["player_sum"] = [player_sum]
                    game_info["result"] = -1 * bet
                    return game_info

            # split
            if player_action == definitions.Actions.SPLIT:
                # make recursive calls and add the results of each hand
                result1 = self.game_result(bet, pydealer.Stack(cards = [player_hand[0]]), dealer_hand, deck)
                result2 = self.game_result(bet, pydealer.Stack(cards = [player_hand[1]]), dealer_hand, deck)

                # combine the two into a single dict
                game_info["result"]     = result1["result"] + result2["result"]
                game_info["player_sum"] = result1["player_sum"] + result2["player_sum"]
                game_info["dealer_sum"] = result1["dealer_sum"] if result1["dealer_sum"] > result2["dealer_sum"] else result2["dealer_sum"]
                game_info["split"]      = True

                return game_info

        while True:
            # handle dealer decisions and final game outcome per draw 
            # precondition: player's hand is not busted

            # hit, add card to dealer hand
            if dealer_action == definitions.Actions.HIT:
                dealer_hand.add(deck.deal())

                # compute next dealer action
                dealer_action = self.dealer.compute_play(dealer_hand)

            # blackjack for dealer and not player, player loses betting amount
            elif dealer_action == definitions.Actions.BLACKJACK:
                game_info["result"] = -1 * bet
                game_info["player_sum"] = [self.player.hand_sum(player_hand)]
                game_info["dealer_sum"] = 21
                return game_info

            # stand
            elif dealer_action == definitions.Actions.STAND:
                dealer_sum = self.dealer.hand_sum(dealer_hand)
                player_sum = self.player.hand_sum(player_hand)
                
                # for testing
                if self.dev_mode:
                    print("\nPlayer sum: {}\nDealer sum: {}".format(player_sum, dealer_sum))

                # dealer busts, player wins bet amount 
                if dealer_sum > 21:
                    game_info["result"] = bet

                # player has higher hand, player wins bet amount 
                elif player_sum > dealer_sum:
                    game_info["result"] = bet

                # tie, player neither gains nor loses bet amount
                elif player_sum == dealer_sum:
                    game_info["result"] = 0

                # dealer has higher hand, player loses their bet
                else:
                    game_info["result"] = -1 * bet

                game_info["player_sum"] = [player_sum]
                game_info["dealer_sum"] = dealer_sum
                
                return game_info

    def init_dict(self):
        """
        Returns an initialized dictionary to store game information 

        Returns
        -------
        A dictionary with the following keys: "result", "player_sum", "dealer_sum", "doubledown", "split"
        
        Where the player_sum is a list of sums for each hand the player has in the round 
        """
        game_info = {
            "result": 0,
            "player_sum": [0],
            "dealer_sum": 0,
            "double_down": False,
            "split": False
        }

        return game_info
    
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

        print("\n~~~Starting Player Hand~~~")
        print(player_hand)
        print("\n~~~Starting Dealer Hand~~~")
        print(dealer_hand)     
        print("\n~~~Starting Deck Size~~~\n{}".format(num_cards))