import definitions
import pydealer

class Game:
    """
    A class used to compute the result of a blackjack game
    """

    def __init__(self, dev_mode=False):
        self.dev_mode = dev_mode

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

        print("Player hand")
        print(player_hand)
        print("\nDealer hand")
        print(dealer_hand)     
        print("\nDeck")
        print(deck.size)
            
        # check for player Blackjack with initial hand
        if "PLAYER_ACTION" == definitions.Actions.BLACKJACK:
            
            # check if dealer also has Blackjack -> tie
            if dealer_hand.size == 1:
                dealer_hand.add(deck.deal())

            if "DEALER_ACTION" == definitions.Actions.BLACKJACK:
                return 0

            # player gets 1.5 to 1 payout for Blackjack
            return 1.5 * bet

        else:
            # handle player decisions

            # hit
            while "PLAYER_ACTION" == definitions.Actions.HIT:
                # add card to player hand
                player_hand.add(deck.deal())

                # player busts on this draw and loses betting amount
                if self.hand_sum(player_hand) > 21:
                    return -1 * bet

            # double
            if "PLAYER_ACTION" == definitions.Actions.DOUBLE:
                # add single card to player hand
                player_hand.add(deck.deal())
                bet *= 2

                # player busts on this draw and loses betting amount
                if self.hand_sum(player_hand) > 21:
                    return -1 * bet

            # split
            if "PLAYER_ACTION" == definitions.Actions.SPLIT:
                # make recursive calls and add the results of each hand
                result  = self.game_result(bet, pydealer.Stack(cards = [player_hand[0]]), dealer_hand, deck)
                result += self.game_result(bet, pydealer.Stack(cards = [player_hand[1]]), dealer_hand, deck)
                return result

        while True:
            # handle dealer decisions and final game outcome per draw 
            # precondition: player's hand is not busted

            # hit, add card to dealer hand
            if "DEALER_ACTION" == definitions.Actions.HIT:
                dealer_hand.add(deck.deal())

            # blackjack for dealer and not player, player loses betting amount
            if "DEALER_ACTION" == definitions.Actions.BLACKJACK:
                return -1 * bet

            # stand
            if "DEALER_ACTION" == definitions.Actions.STAND:
                dealer_sum = self.hand_sum(dealer_hand)
                player_sum = self.hand_sum(player_hand)

                # dealer busts, player wins bet amount
                if dealer_sum > 21:
                    return bet

                # dealer has higher hand
                elif dealer_sum > player_sum:
                    return -1 * bet

                # player has higher hand
                elif player_sum> dealer_sum:
                    return bet

                # tie
                else:
                    return 0
                       
    def hand_sum(self, hand):
        """
        Generates the numerical sum of a playing hand

        Parmeters
        ---------
        hand : Card list
            The hand to calculate

        Returns
        -------
        An integer representing the numerical sum of a blackjack hand
        """
        sum = 0

        for card in hand:
            if card.value in ["King", "Queen", "Jack"]:
                sum += 10
            elif card.value == "Ace":
                sum += 1
            else:
                sum += int(card.value)

        return sum

bj = Game()
print(bj.game_result(1))

 # check if dealer also has Blackjack -> tie
# dealer_hand.add(deck.deal())

# for card in dealer_hand:
#     if card.value == "Ace":
#         if self.hand_sum(dealer_hand) == 11:
#             return 0
#         break

print("\n-----absolute lunacy-----\n")

# deck = pydealer.Deck()
# deck.shuffle()

# hand = deck.deal(2)
# print(hand)

# print(hand[0])
# print(type([hand[0]])==list)

# h = pydealer.Stack(cards = [hand[0]])
# print(h)
# a = pydealer.Stack()
# if a is None:
#     print("a")

# b = None
# if b is None:
#     print("b")
# bj.game_result(1, pydealer.Stack(cards = [hand[0]]), hand[1])