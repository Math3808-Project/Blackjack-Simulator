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

        # gameplay conditions
        double_down = False
        split_aces  = False

        # draw player hand if hand not inputted
        if player_hand is None:
            player_hand = pydealer.Stack(cards = [deck.random_card(True), deck.random_card(True)])
       
        # add second card to player hand for a split
        if player_hand.size < 2:
            # check for split aces 
            if player_hand[0].value == "Ace":
                split_aces = True

            player_hand.add(deck.random_card(True))

        # draw dealer hand 
        if dealer_hand is None:
            dealer_hand = pydealer.Stack(cards = [deck.random_card(True), deck.random_card(True)])

        # for testing
        if self.dev_mode:
            self.print_info(player_hand, dealer_hand, deck.size)

        # the initial action for the player and dealer
        player_action = self.player.compute_play(player_hand, dealer_hand[0], split_aces)
        dealer_action = self.dealer.compute_play(dealer_hand)
            
        # check for player Blackjack with initial hand
        if player_action == definitions.Actions.BLACKJACK and not split_aces:
            # check if dealer also has Blackjack -> tie
            if dealer_action == definitions.Actions.BLACKJACK:
                return self.make_result_dict(
                    result      = 0, 
                    player_sum  = [21],
                    dealer_sum  = 21,
                    blackjack   = True)

            # player gets 1.5 to 1 payout for Blackjack
            return self.make_result_dict(
                result      = 1.5 * bet, 
                player_sum  = [21],
                blackjack   = True)

        else:
            # handle player decisions

            # hit
            while player_action == definitions.Actions.HIT and not split_aces:
                # add card to player hand
                player_hand.add(deck.random_card(True))

                player_sum = self.player.hand_sum(player_hand)

                # player busts on this draw and loses betting amount
                if player_sum > 21:
                
                    # for testing
                    if self.dev_mode:
                        print("\n___Player's Cards After Bust___\n{}".format(player_hand))

                    return self.make_result_dict(
                        result      = -1 * bet, 
                        player_sum  = [player_sum])

                player_action = self.player.compute_play(player_hand, dealer_hand[0], split_aces)

            # double
            if player_action == definitions.Actions.DOUBLE:
                double_down = True

                # add single card to player hand
                player_hand.add(deck.random_card(True))
                bet *= 2

                # for testing
                if self.dev_mode:
                    print("\n___Player's Cards After Double___\n{}".format(player_hand))

                player_sum = self.player.hand_sum(player_hand)

                # player busts on this draw and loses betting amount
                if player_sum > 21:
                    return self.make_result_dict(
                        result      = -1 * bet, 
                        player_sum  = [player_sum],
                        double_down = double_down)

            # split
            if player_action == definitions.Actions.SPLIT:
                # make recursive calls and add the results of each hand
                result1 = self.game_result(bet, pydealer.Stack(cards = [player_hand[0]]), dealer_hand, deck)
                result2 = self.game_result(bet, pydealer.Stack(cards = [player_hand[1]]), dealer_hand, deck)

                # combine the two into a single dict
                return self.make_result_dict(
                    result      = result1["result"] + result2["result"], 
                    player_sum  = result1["player_sum"] + result2["player_sum"],
                    dealer_sum  = result1["dealer_sum"] if result1["dealer_sum"] > result2["dealer_sum"] else result2["dealer_sum"],
                    split       = True)

        # checks for dealer blackjack with initial hand
        if dealer_action == definitions.Actions.BLACKJACK:
            return self.make_result_dict(
                result      = -1 * bet,
                dealer_sum  = 21,
                blackjack   = True)

        while True:
            # handle dealer decisions and final game outcome per draw 
            # precondition: player's hand is not busted

            # hit, add card to dealer hand
            if dealer_action == definitions.Actions.HIT:
                dealer_hand.add(deck.random_card(True))

                # compute next dealer action
                dealer_action = self.dealer.compute_play(dealer_hand)

            # stand
            elif dealer_action == definitions.Actions.STAND:
                player_sum = self.player.hand_sum(player_hand)
                dealer_sum = self.dealer.hand_sum(dealer_hand)
                res = 0
                
                # for testing
                if self.dev_mode:
                    print("\nPlayer sum: {}\nDealer sum: {}".format(player_sum, dealer_sum))

                # dealer busts, player wins bet amount 
                if dealer_sum > 21:
                    res = bet

                # player has higher hand, player wins bet amount 
                elif player_sum > dealer_sum:
                    res = bet

                # tie, player neither gains nor loses bet amount
                elif player_sum == dealer_sum:
                    res = 0

                # dealer has higher hand, player loses their bet
                else:
                    res = -1 * bet

                return self.make_result_dict(
                    result      = res, 
                    player_sum  = [player_sum],
                    dealer_sum  = dealer_sum,
                    double_down = double_down)
                
    def make_result_dict(self, result=0, player_sum=[0], dealer_sum=0, blackjack=False, double_down=False, split=False):
        """
        Returns an dictionary that stores game information 

        Default values are as follows:

        result_dict = {
            "result": 0,
            "player_sum": [0],
            "dealer_sum": 0,
            "blackjack": False,
            "double_down": False,
            "split": False
        }

        Where the player_sum is a list of sums for each hand the player has in the round 

        Both player_sum and dealer_sum represent the final card values. If they are zero, it means their sum was unused during the game.

        Returns
        -------
        A dictionary with various game details
        
        """
        result_dict = {
            "result": result,
            "player_sum": player_sum,
            "dealer_sum": dealer_sum,
            "blackjack": blackjack,
            "double_down": double_down,
            "split": split
        }

        return result_dict
    
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