from random import randint
import sys
import pydealer
import definitions
import game

card_values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

def main():
    bj = game.Game(dev_mode=True)

    # output file
    sys.stdout = open("game_test.txt", "w")

    # initial betting amount 
    bet_amount = 1

    # traverse card values for making the player's first card
    for i in card_values:

        # traverse card values for making the player's second card
        for j in card_values:

            # deck used during gameplay
            deck = pydealer.Deck()
            deck.shuffle()

            # assemble player hand
            hand = pydealer.Stack(cards = [
                deck.get(i+" of Hearts")[0],
                deck.get(j+" of Spades")[0]])

            print("\n\n-----------[ New Game ]-----------\n\n")

            # play game with the hand
            game_str = bj.game_result(bet=bet_amount, player_hand=hand, deck=deck)

            print("\nPlayer Net Result After ${} Initial Bet: ${}\n".format(bet_amount, game_str["result"]))
        
    sys.stdout.close()

if __name__ == "__main__":
    main()