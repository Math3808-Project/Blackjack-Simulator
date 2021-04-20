# Class - Simulator
# Runs multiple simulations of the game and saves the results

import game
import multiprocessing as mp
import csv

class Simulator:
    """Class that manages simulations of a BlackJack game
    
    Parameters:

    sim_count (int): Indicated the number of simulations to compute

    """

    def __init__(self, sim_count=1000000, bet_amount=1):
        self.sim_count = sim_count
        self.bet_amount = bet_amount

    def main(self):
        print(f'Starting Blackjack Simulator with {self.sim_count} simulations')
        results = []
        
        #TODO: Implement concurrency
        for x in range(self.sim_count):
            results.append(self.run_game())
        
        self.write_results(results)
        
        print(f'Result for this simulation: {sum(results)/self.sim_count}')
        print(f'Adjusted overall result: {self.get_overall_average(results)}')

        # for x in range(10):
        #     p = Process(target=run_game)
        #     p.start()
        #     p.join()


    def run_game(self):
        bj = game.Game()
        result_dict = bj.game_result(bet=self.bet_amount)
        return result_dict["result"]

    def write_results(self, results):
        res = open("results.csv", "a")
        res.write(f'{self.sim_count},{self.bet_amount},{sum(results)}\n')
        res.close()
    
    def get_overall_average(self, results):
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
    Simulator().main()
