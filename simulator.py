# Class - Simulator
# Runs multiple simulations of the game and saves the results

import game
import concurrent.futures
import csv

class Simulator:
    """Class that manages simulations of a BlackJack game
    
    Parameters:

    sim_count (int): Indicates the number of simulations to compute - will be rounded up to the
    
    nearest multiple of 10000 
    
    bet (int): Represents the starting bet for the Black Jack game
    """

    def __init__(self, sim_count=1000000, bet_amount=1):
        if sim_count % 10000 != 0: 
            self.sim_count = sim_count + 10000 - (sim_count % 10000)
        else:
            self.sim_count = sim_count

        self.bet_amount = bet_amount
        self.completed_sims = 0

    def start(self):
        """ Runs the Simulation with the initialized attributes.

        Outputs:
        
        The result of the current simulation as well as the overall result of all simulations run previously.

        Appends the most recent result to results.csv
        
        Updates overall_avg.csv with the updated totals for total_sims and result_sum
        """
        print(f'Starting Blackjack Simulator with {self.sim_count} simulations')
        results = []

        with concurrent.futures.ProcessPoolExecutor() as executor:
            p_list = []
            for i in range(int(self.sim_count/10000)):
                p_list.append(executor.submit(self.run_multiple_games, 10000))
                
                for res in concurrent.futures.as_completed(p_list):
                    results.append(res.result())
                
        
        self.write_results(results)
        
        print(f'Result for this simulation batch: {sum(results)/self.sim_count}')
        print(f'Adjusted overall result: {self.get_overall_average(results)}')


    def run_single_game(self):
        """ Runs a single Black Jack game.

        Returns:
        
        int: the result of the game
        """

        bj = game.Game()
        result_dict = bj.game_result(bet=self.bet_amount)
        return result_dict["result"]
    
    def run_multiple_games(self, num_games):
        """ Runs a given number of Black Jack games.

        Returns:
        
        int: the result sum of the games
        """
        results = []
        for x in range(num_games):
            results.append(self.run_single_game())
        self.completed_sims += num_games
        print(f'Simulations completed so far: {self.completed_sims}')
        return sum(results)

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
        
        return result_sum/total_sims

if __name__ == "__main__":
    Simulator().start()
