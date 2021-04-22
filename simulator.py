# Class - Simulator
# Runs multiple simulations of the game and saves the results

import game
import concurrent.futures
import csv

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
        results = []

        for x in range(self.sim_count):
            results.append(self.run_single_game())
                
        self.write_results(results)
        
        print(f'Result for this simulation batch: {sum(results)/self.sim_count}')
        self.get_overall_average(results)


    def run_single_game(self):
        """ Runs a single Black Jack game.

        Returns:
        
        int: the result of the game
        """

        bj = game.Game()
        result_dict = bj.game_result(bet=self.bet_amount)
        return result_dict["result"] 

    def write_results(self, results):
        """ Writes the results of all simulations to results.csv.

        Parameters:
        
        arr[int]: an array of game results
        """

        res = open("results.csv", "a")
        res.write(f'{self.sim_count},{self.bet_amount},{sum(results)}\n')
        res.close()
    
    def get_overall_average(self, results):
        """ Calulates the overall average of results from most recent and historical simulations and
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

if __name__ == "__main__":
    Simulator().start()
