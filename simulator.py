# Class - Simulator
# Runs multiple simulations of the game and saves the results

import game
import concurrent.futures
import csv
from yaspin import yaspin

class Simulator:
    """Class that manages simulations of a BlackJack game
    
    Parameters:

    sim_count (int): Indicates the number of simulations to compute
    
    bet (int): Represents the starting bet for the Black Jack game
    """

    def __init__(self, sim_count=1000000, bet_amount=1):
        self.sim_count = sim_count
        self.bet_amount = bet_amount

    def start(self):
        """ Runs the Simulation with the initialized attributes.

        Outputs:
        
        The result of the current simulation as well as the overall result of all simulations run previously.

        Appends the most recent result to results.csv
        
        Updates overall_avg.csv with the updated totals for total_sims and result_sum
        """
        print(f'Starting Blackjack Simulator with {self.sim_count} simulations - will take approximately 4 minutes.')
        bj = game.Game()
        results = []
        non_final_hands=0
        dealer_dist = {
            "17":0,
            "18":0,
            "19":0,
            "20":0,
            "21":0,
            "BJ":0,
            "Bust":0
        }

        with yaspin(text="Elapsed Time", timer=True) as spinner:
            for x in range(self.sim_count):
                result_dict = self.run_single_game(bj)
                results.append(result_dict["result"])
                non_final_hands = self.store_dealer_dist(dealer_dist, non_final_hands, result_dict)
            
            spinner.ok()
                
        self.write_results(results)

        self.adjust_dealer_dist(dealer_dist, non_final_hands)
        
        print(f'\nResult for this simulation batch: {sum(results)/self.sim_count}')
        print("Dealer Final Hand Distribution: {}\n".format(dealer_dist))
        self.get_overall_average(results)


    def run_single_game(self, bj):
        """ Runs a single Black Jack game.

        Returns:
        
        result_dict: the result of the game
        """
        return bj.game_result(bet=self.bet_amount)

    def write_results(self, results):
        """ Writes the results of all simulations to results.csv.

        Parameters:
        
        arr[int]: an array of game results
        """

        res = open("results.csv", "a")
        res.write(f'{self.sim_count},{self.bet_amount},{sum(results)}\n')
        res.close()
    
    def get_overall_average(self, results):
        """ Calculates the overall average of results from most recent and historical simulations and
            updates the values in overall_avg.csv
     
        Parameters:
        
        arr: an array of game results

        Returns:
        
        float: the average of all results
        """

        total_sims = self.sim_count
        result_sum = sum(results)
        with open('overall_avg.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                total_sims += float(row["total_sims"])
                result_sum += float(row["result_sum"])
        prev_totals = open("overall_avg.csv", "w")
        prev_totals.write(f'total_sims,result_sum\n{total_sims},{result_sum}')
        
        print(f'Adjusted overall result for {total_sims} simulations: {result_sum/total_sims}')

    def store_dealer_dist(self, dealer_dist, non_final_hands, result_dict):
        """ Adjusts the dealer_dist dictionary with the sum from the round
     
        Parameters:
        
        dealer_dist: the dictionary of the dealer distribution 

        non_final_hands: the number of dealer hands that did not have an impact on the game result

        result_dict: the result dictionary after a game

        Returns:

        non_final_hands: the adjusted number of dealer hands that did not have an impact on the game result
        """
        dealer_sum = result_dict["dealer_sum"]
        blackjack = result_dict["blackjack"]

        if dealer_sum == 17:
            dealer_dist["17"] += 1
        elif dealer_sum == 18:
            dealer_dist["18"] += 1
        elif dealer_sum == 19:
            dealer_dist["19"] += 1
        elif dealer_sum == 20:
            dealer_dist["20"] += 1
        elif dealer_sum == 21 and not blackjack:
            dealer_dist["21"] += 1
        elif dealer_sum == 21 and blackjack:
            dealer_dist["BJ"] += 1
        elif dealer_sum > 21:
            dealer_dist["Bust"] += 1
        else: 
            non_final_hands += 1

        return non_final_hands

    def adjust_dealer_dist(self, dealer_dist, non_final_hands):
        """ Adjusts the dealer_dist dictionary by dividing its values by the number of final hands
     
        Parameters:
        
        dealer_dist: the dictionary of the dealer distribution 

        non_final_hands: the number of dealer hands that did not have an impact on the game result

        Returns:

        void
        """

        for key in dealer_dist.keys():
            dealer_dist[key] = round((dealer_dist[key] / (self.sim_count-non_final_hands)), 4)

if __name__ == "__main__":
    Simulator().start()
