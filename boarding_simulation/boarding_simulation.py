import random
import matplotlib.pyplot as plt
from collections.abc import Callable

def simulate_boarding(num_rows: int, boarding_order: list[int], sit_time: int) -> tuple:
    """
    Simulate passenger movement through a single-aisle plane.
    sit_time = number of future movement rounds a passenger blocks
    after reaching their target row.
    """
    time_stamps = {}
    time = 0
    aisle = [""]*(num_rows+1)
    time_stamps[time] = aisle.copy()
    wait_time = {}
    remaining_boarding_order = boarding_order.copy()
    while True:
        updated_wait_time = {}
        for i in wait_time: # Update wait times before movement, so seated passengers block this round.
                wait_time[i] -= 1
                if wait_time[i] == -1:
                    aisle[i] = ""
                else:
                    updated_wait_time[i] = wait_time[i]
        wait_time = updated_wait_time
        for position in range(num_rows-1,-1,-1): # Move backwards so passengers can not move more than 1 position in a round
            if aisle[position+1] == "" and aisle[position] != "" and aisle[position] != position:
                aisle[position+1] = aisle[position]
                aisle[position] = ""
                if aisle[position+1] == position+1:
                    wait_time[position+1] = sit_time
        time += 1
        if aisle[0] == "" and remaining_boarding_order!=[]:
            aisle[0] = remaining_boarding_order[0]
            remaining_boarding_order.pop(0)
        time_stamps[time] = aisle.copy()
        if all(x == "" for x in aisle) and remaining_boarding_order == []:
            break
    total_time = max(time_stamps)
    return time_stamps, wait_time, total_time


def front_to_back_order(num_rows: int) -> list:
    order = list(range(1, num_rows+1))
    return order
    
def back_to_front_order(num_rows: int) -> list:
    order = list(range(num_rows, 0, -1))
    return order

def random_boarding_order(num_rows: int) -> list:
    order = random.sample(range(1, num_rows+1), num_rows)
    return order


def average_boarding_time(num_rows: int, sit_time: int, num_trials: int, order_function: Callable[[int], list[int]]) -> float:
    total_time_sum = 0
    for trial in range(num_trials):
        boarding_order = order_function(num_rows)
        _, _, trial_total_time = simulate_boarding(num_rows, boarding_order, sit_time)
        total_time_sum += trial_total_time
    average_trial_time = total_time_sum/num_trials
    return average_trial_time

        

def compare_strategies(num_rows: int, sit_time: int, num_trials: int) -> dict[str, float]:
    average_time_per_strategy = {}
    forward = average_boarding_time(num_rows, sit_time, num_trials, front_to_back_order)
    backwards = average_boarding_time(num_rows, sit_time, num_trials, back_to_front_order)
    random_order = average_boarding_time(num_rows, sit_time, num_trials, random_boarding_order)
    average_time_per_strategy["front_to_back_order"] = forward
    average_time_per_strategy["back_to_front_order"] = backwards
    average_time_per_strategy["random_boarding_order"] = random_order
    return average_time_per_strategy

def greater_compare_strategies(num_rows: list, sit_time: list, num_trials: int) -> tuple:
    storage = {}
    for row_count in num_rows: 
        for sit_time_value in sit_time:
            average_time_per_strategy = compare_strategies(row_count,sit_time_value,num_trials)
            result_for_setting = average_time_per_strategy
            result_for_setting["rows"] = row_count
            result_for_setting["sit_time"] = sit_time_value
            storage[row_count,sit_time_value] = result_for_setting
    overview = []
    for value in storage.values():
        overview.append(f"Rows: {value['rows']}| sit_time: {value['sit_time']}| front: {value['front_to_back_order']}| back: {value['back_to_front_order']}| random: {value['random_boarding_order']}")
    return storage, overview

def plot_strategy_rows(results, fixed_sit_time):
    x = []
    yf = []
    yb = []
    yr = []
    for value in results.values():
        if value["sit_time"] == fixed_sit_time:
            x.append(value["rows"])
            yf.append(value["front_to_back_order"])
            yb.append(value["back_to_front_order"])
            yr.append(value["random_boarding_order"])
    plt.plot(x, yf, label="front", color="blue", linestyle="-", marker="o")
    plt.plot(x, yb, label="back", color="green", linestyle="--", marker="o")
    plt.plot(x, yr, label="random", color="orange", linestyle=":", marker="o")
    plt.xlabel("Number of rows")
    plt.ylabel("Average time per strategy")
    plt.legend()
    plt.show()

def plot_strategy_sit_time(results, fixed_rows):
    x = []
    yf = []
    yb = []
    yr = []
    for value in results.values():
        if value["rows"] == fixed_rows:
            x.append(value["sit_time"])
            yf.append(value["front_to_back_order"])
            yb.append(value["back_to_front_order"])
            yr.append(value["random_boarding_order"])
    plt.plot(x, yf, label="front", color="blue", linestyle="-", marker="o")
    plt.plot(x, yb, label="back", color="green", linestyle="--", marker="o")
    plt.plot(x, yr, label="random", color="orange", linestyle=":", marker="o")
    plt.xlabel("Sit time")
    plt.ylabel("Average time per strategy")
    plt.legend()
    plt.show()

def interpret_strategy(results):
    max_difference = 0
    min_difference = 10000
    fixed_rows = {}
    fixed_sit_time = {}
    wins = {"front": 0, "back": 0, "random": 0}
    for test in results.values():
        print(f"\nRows: {test['rows']}, sit_time: {test['sit_time']}")
        front = test["front_to_back_order"]
        back = test["back_to_front_order"]
        random = test["random_boarding_order"]
        scores = {"front": front,
                  "back": back,
                  "random": random}
        worst_strategy = max(scores, key=scores.get)
        best_strategy = min(scores, key=scores.get)
        difference = scores[worst_strategy]-scores[best_strategy]
        best_script = {"front": f"Best strategy: front_to_back_order, {front}", 
                       "back": f"Best strategy: back_to_front_order, {back}", 
                       "random": f"Best strategy: random_boarding_order, {random}"}
        worst_script = {"front": f"Worst strategy: front_to_back_order, {front}", 
                       "back": f"Worst strategy: back_to_front_order, {back}", 
                       "random": f"Worst strategy: random_boarding_order, {random}"}
        if test['rows'] == 20:
            fixed_rows[test['sit_time']] = difference
        if test['sit_time'] == 1:
            fixed_sit_time[test['rows']] = difference
        if difference>max_difference:
            max_difference = difference
            largest_gap = f"Largest gap happened at rows = {test['rows']}, sit_time = {test['sit_time']}"
        if min_difference>difference:
            min_difference = difference
            smallest_gap = f"Smallest gap happened at rows = {test['rows']}, sit_time = {test['sit_time']}"
        print(best_script[best_strategy])
        wins[best_strategy]+=1
        print(worst_script[worst_strategy])
        print(f"Gap: {difference}")
        print(f"Random gap from best: {round(random-scores[best_strategy],2)}")
    difference_prev_sit_time = None
    gap_fixed_sit_time = []
    total_gap_sit_time = 0
    score_fixed_sit_time = 0
    for difference in fixed_sit_time.values():
        if difference_prev_sit_time is not None:
            gap_difference_sit_time = difference - difference_prev_sit_time
            gap_fixed_sit_time.append(gap_difference_sit_time)
            total_gap_sit_time += gap_difference_sit_time
            if difference>difference_prev_sit_time:
                score_fixed_sit_time += 1
            elif difference_prev_sit_time>difference:
                score_fixed_sit_time -= 1
        difference_prev_sit_time = difference
    difference_prev_rows = None
    gap_fixed_rows = []
    total_gap_rows = 0  
    score_fixed_rows = 0    
    for difference in fixed_rows.values():
        if difference_prev_rows is not None:
            gap_difference_rows = difference - difference_prev_rows
            gap_fixed_rows.append(gap_difference_rows)
            total_gap_rows += gap_difference_rows
            if difference>difference_prev_rows:
                score_fixed_rows += 1
            elif difference_prev_rows>difference:
                score_fixed_rows -= 1
        difference_prev_rows = difference

    gap_fixed_rows_script = {
    "increasing": "Within the rows = 20 slice, the strategy gap consistently increases as sit_time increases.\nThis suggests boarding strategy matters more when passengers block the aisle longer.",
    "mostly increasing": "Within the rows = 20 slice, the strategy gap mostly increases as sit_time increases.\nThis suggests boarding strategy matters more when passengers block the aisle longer.",
    "neutral": "Within the rows = 20 slice, the strategy gap does not structurally increase or decrease as sit_time increases.\nThis suggests boarding strategy is not strongly affected by longer sitting delays in this model.",
    "mostly decreasing": "Within the rows = 20 slice, the strategy gap mostly decreases as sit_time increases.\nThis suggests boarding strategy matters less when passengers block the aisle longer.",
    "decreasing": "Within the rows = 20 slice, the strategy gap consistently decreases as sit_time increases.\nThis suggests boarding strategy matters less when passengers block the aisle longer."
    }

    gap_fixed_sit_time_script = {
    "increasing": "Within the sit_time = 1 slice, the strategy gap consistently increases as rows increase.\nThis suggests boarding strategy matters more for larger planes.",
    "mostly increasing": "Within the sit_time = 1 slice, the strategy gap mostly increases as rows increase.\nThis suggests boarding strategy matters more for larger planes.",
    "neutral": "Within the sit_time = 1 slice, the strategy gap does not structurally increase or decrease as rows increase.\nThis suggests boarding strategy is not strongly affected by larger planes in this model.",
    "mostly decreasing": "Within the sit_time = 1 slice, the strategy gap mostly decreases as rows increase.\nThis suggests boarding strategy matters less for larger planes.",
    "decreasing": "Within the sit_time = 1 slice, the strategy gap consistently decreases as rows increase.\nThis suggests boarding strategy matters less for larger planes."
    }

    
    if score_fixed_rows>0:
        if score_fixed_rows == len(gap_fixed_rows):
            gap_fixed_rows_result = "increasing"
        else:
            gap_fixed_rows_result = "mostly increasing"
    elif score_fixed_rows == 0:
        gap_fixed_rows_result = "neutral" 
    else:
        if abs(score_fixed_rows) == len(gap_fixed_rows):
            gap_fixed_rows_result = "decreasing"
        else:
            gap_fixed_rows_result = "mostly decreasing"

    if score_fixed_sit_time>0:
        if score_fixed_sit_time== len(gap_fixed_sit_time):
            gap_fixed_sit_time_result = "increasing"
        else:
            gap_fixed_sit_time_result = "mostly increasing"
    elif score_fixed_sit_time == 0:
        gap_fixed_sit_time_result = "neutral" 
    else:
        if abs(score_fixed_sit_time) == len(gap_fixed_sit_time):
            gap_fixed_sit_time_result = "decreasing"
        else:
            gap_fixed_sit_time_result = "mostly decreasing"

    winner = max(wins, key=wins.get)
    won_script  = {"front": f"Front_to_back_order won {wins[winner]}/{sum(wins.values())} settings", 
                       "back": f"Back_to_front_order won {wins[winner]}/{sum(wins.values())} settings", 
                       "random": f"Random_boarding_order won {wins[winner]}/{sum(wins.values())} settings"}
    print("\n----------------------------------------------------------------")
    print(f"\nOverall summary \n\n{won_script[winner]} \n\n{largest_gap} \n{smallest_gap}")
    print(f"\n{gap_fixed_sit_time_script[gap_fixed_sit_time_result]} \n\n{gap_fixed_rows_script[gap_fixed_rows_result]}")

def test_strategies() -> str:
    result = compare_strategies(5,1,10)
    comparison_set = {"front_to_back_order", "back_to_front_order", "random_boarding_order"}
    assert(front_to_back_order(5)) ==[1,2,3,4,5]
    assert(back_to_front_order(5)) == [5,4,3,2,1] 
    assert(sorted(random_boarding_order(5))) == [1,2,3,4,5] 
    assert(type(result)) == dict
    assert(type(result["front_to_back_order"])) == float
    assert(type(result["back_to_front_order"])) == float
    assert(type(result["random_boarding_order"])) == float
    assert(set(result.keys())) == comparison_set
    return "All sanity tests passed."


def test_simulation() -> str:
    boarding_order_front = [1,2]
    front_test = boarding_order_front.copy()
    assert simulate_boarding(1,[1],0)[1] == {}
    assert simulate_boarding(1,[1],0)[2] == 3 
    assert simulate_boarding(1,[1],1)[2] == 4
    assert simulate_boarding(2,[1,2],0)[2] == 5
    assert simulate_boarding(2,[2,1],0)[2] == 4
    assert simulate_boarding(2,boarding_order_front,1)[2] == 7
    assert(boarding_order_front) == front_test
    return "Simulation tests passed"
    

if __name__ == "__main__":
    results, _ = greater_compare_strategies([5, 10, 20, 40],[0, 1, 2, 3],10)
    for line in results:
        print(line)
    print(test_strategies())
    print(test_simulation())
    plot_strategy_rows(results, fixed_sit_time=1)
    plot_strategy_sit_time(results, fixed_rows=10)
    interpret_strategy(results)
    
