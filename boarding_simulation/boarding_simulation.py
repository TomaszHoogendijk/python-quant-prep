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

def greater_compare_strategies(num_rows: list[int], sit_time: list[int], num_trials: int) -> tuple:
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

def plot_strategy_rows(results: dict, fixed_sit_time: int) -> None:
    x = []
    y_front = []
    y_back = []
    y_random = []
    for value in results.values():
        if value["sit_time"] == fixed_sit_time:
            x.append(value["rows"])
            y_front.append(value["front_to_back_order"])
            y_back.append(value["back_to_front_order"])
            y_random.append(value["random_boarding_order"])
    plt.plot(x, y_front, label="front", color="blue", linestyle="-", marker="o")
    plt.plot(x, y_back, label="back", color="green", linestyle="--", marker="o")
    plt.plot(x, y_random, label="random", color="orange", linestyle=":", marker="o")
    plt.xlabel("Number of rows")
    plt.ylabel("Average time per strategy")
    plt.legend()
    plt.show()

def plot_strategy_sit_time(results: dict, fixed_rows: int) -> None:
    x = []
    y_front = []
    y_back = []
    y_random = []
    for value in results.values():
        if value["rows"] == fixed_rows:
            x.append(value["sit_time"])
            y_front.append(value["front_to_back_order"])
            y_back.append(value["back_to_front_order"])
            y_random.append(value["random_boarding_order"])
    plt.plot(x, y_front, label="front", color="blue", linestyle="-", marker="o")
    plt.plot(x, y_back, label="back", color="green", linestyle="--", marker="o")
    plt.plot(x, y_random, label="random", color="orange", linestyle=":", marker="o")
    plt.xlabel("Sit time")
    plt.ylabel("Average time per strategy")
    plt.legend()
    plt.show()

def collect_strategy_interpretation_data(results):
    max_worst_best_gap = float('-inf')
    min_worst_best_gap = float('inf')
    fixed_rows_gaps = {}
    fixed_sit_time_gaps = {}
    wins_count = {"front": 0, "back": 0, "random": 0}
    for result in results.values():
        front = result["front_to_back_order"]
        back = result["back_to_front_order"]
        random = result["random_boarding_order"]
        average_time_per_strategy = {"front": front,
                                     "back": back,
                                     "random": random}
        worst_strategy = max(average_time_per_strategy, key=average_time_per_strategy.get)
        best_strategy = min(average_time_per_strategy, key=average_time_per_strategy.get)
        worst_best_gap = average_time_per_strategy[worst_strategy]-average_time_per_strategy[best_strategy]
        if result['rows'] == 20:
            fixed_rows_gaps[result['sit_time']] = worst_best_gap
        if result['sit_time'] == 1:
            fixed_sit_time_gaps[result['rows']] = worst_best_gap
        if worst_best_gap>max_worst_best_gap:
            max_worst_best_gap = worst_best_gap
            largest_gap = f"Largest gap happened at rows = {result['rows']}, sit_time = {result['sit_time']}"
        if min_worst_best_gap>worst_best_gap:
            min_worst_best_gap = worst_best_gap
            smallest_gap = f"Smallest gap happened at rows = {result['rows']}, sit_time = {result['sit_time']}"
        wins_count[best_strategy]+=1
    interpretation_data = {}
    interpretation_data["wins_count"] = wins_count
    interpretation_data["fixed_rows_gaps"] = fixed_rows_gaps
    interpretation_data["fixed_sit_time_gaps"] = fixed_sit_time_gaps
    interpretation_data["largest_gap"] = largest_gap
    interpretation_data["smallest_gap"] = smallest_gap
    return interpretation_data

def print_strategy_per_setting_report(results):
    for result in results.values():
        print(f"\nRows: {result['rows']}, sit_time: {result['sit_time']}")
        front = result["front_to_back_order"]
        back = result["back_to_front_order"]
        random = result["random_boarding_order"]
        average_time_per_strategy = {"front": front,
                                     "back": back,
                                     "random": random}
        worst_strategy = max(average_time_per_strategy, key=average_time_per_strategy.get)
        best_strategy = min(average_time_per_strategy, key=average_time_per_strategy.get)
        worst_best_gap = average_time_per_strategy[worst_strategy]-average_time_per_strategy[best_strategy]
        best_script = {"front": f"Best strategy: front_to_back_order, {front}", 
                       "back": f"Best strategy: back_to_front_order, {back}", 
                       "random": f"Best strategy: random_boarding_order, {random}"}
        worst_script = {"front": f"Worst strategy: front_to_back_order, {front}", 
                       "back": f"Worst strategy: back_to_front_order, {back}", 
                       "random": f"Worst strategy: random_boarding_order, {random}"}
        print(best_script[best_strategy])
        print(worst_script[worst_strategy])
        print(f"Gap: {worst_best_gap}")
        print(f"Random gap from best: {round(random-average_time_per_strategy[best_strategy],2)}")
    
def print_strategy_overall_report(interpretation_data: dict):
    wins_count = interpretation_data["wins_count"] 
    fixed_rows_gaps = interpretation_data["fixed_rows_gaps"] 
    fixed_sit_time_gaps = interpretation_data["fixed_sit_time_gaps"]
    largest_gap = interpretation_data["largest_gap"] 
    smallest_gap = interpretation_data["smallest_gap"]   
    worst_best_gap_prev_sit_time = None
    gap_fixed_sit_time = []
    total_gap_sit_time = 0
    score_fixed_sit_time = 0
    for worst_best_gap in fixed_sit_time_gaps.values():
        if worst_best_gap_prev_sit_time is not None:
            gap_difference_sit_time = worst_best_gap - worst_best_gap_prev_sit_time
            gap_fixed_sit_time.append(gap_difference_sit_time)
            total_gap_sit_time += gap_difference_sit_time
            if worst_best_gap>worst_best_gap_prev_sit_time:
                score_fixed_sit_time += 1
            elif worst_best_gap_prev_sit_time>worst_best_gap:
                score_fixed_sit_time -= 1
        worst_best_gap_prev_sit_time = worst_best_gap
    worst_best_gap_prev_rows = None
    gap_fixed_rows = []
    total_gap_rows = 0  
    score_fixed_rows = 0    
    for worst_best_gap in fixed_rows_gaps.values():
        if worst_best_gap_prev_rows is not None:
            gap_difference_rows = worst_best_gap - worst_best_gap_prev_rows
            gap_fixed_rows.append(gap_difference_rows)
            total_gap_rows += gap_difference_rows
            if worst_best_gap>worst_best_gap_prev_rows:
                score_fixed_rows += 1
            elif worst_best_gap_prev_rows>worst_best_gap:
                score_fixed_rows -= 1
        worst_best_gap_prev_rows = worst_best_gap

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

    winner = max(wins_count, key=wins_count.get)
    won_script  = {"front": f"Front_to_back_order won {wins_count[winner]}/{sum(wins_count.values())} settings", 
                       "back": f"Back_to_front_order won {wins_count[winner]}/{sum(wins_count.values())} settings", 
                       "random": f"Random_boarding_order won {wins_count[winner]}/{sum(wins_count.values())} settings"}
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
    print_strategy_per_setting_report(results)
    data = collect_strategy_interpretation_data(results)
    print_strategy_overall_report(data)

    
    

    
