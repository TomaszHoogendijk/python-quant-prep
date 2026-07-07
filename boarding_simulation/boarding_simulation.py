import random
import matplotlib.pyplot as plt

def simulate_boarding(num_rows: int, boarding_order: list, sit_time: int):
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
    state = True
    mutated_boarding_order = boarding_order.copy()
    while state==True:
        adjust_wait_time = {}
        for i in wait_time: # Update wait times before movement, so seated passengers block this round.
                wait_time[i] -=1
                if wait_time[i] == -1:
                    aisle[i] = ""
                else:
                    adjust_wait_time[i] = wait_time[i]
        wait_time = adjust_wait_time
        for position in range(num_rows-1,-1,-1): # Move backwards so passengers can not move more than 1 position in a round
            if aisle[position+1] == "" and aisle[position] != "" and aisle[position] != position:
                aisle[position+1] = aisle[position]
                aisle[position] = ""
                if aisle[position+1] == position+1:
                    wait_time[position+1] = sit_time
        time += 1
        if aisle[0] == "" and mutated_boarding_order!=[]:
            aisle[0] = mutated_boarding_order[0]
            mutated_boarding_order.pop(0)
        time_stamps[time] = aisle.copy()
        if all(x == "" for x in aisle) and mutated_boarding_order == []:
            state = False
    total_time = max(time_stamps)
    return time_stamps, wait_time, total_time

def front_to_back_order(num_rows: int) -> list:
    order = []
    for i in range(1, num_rows+1):
        order.append(i)
    return order
    
def back_to_front_order(num_rows: int) -> list:
    order = []
    for i in range(num_rows, 0,-1):
        order.append(i)
    return order

def random_boarding_order(num_rows: int):
    order = []
    while len(order)<num_rows:
        x = random.randint(1,num_rows)
        if x not in order:
            order.append(x)
    return order

def average_boarding_time(num_rows: int, sit_time: int, num_trials: int, strategy):
    total_time = 0
    for i in range(num_trials):
        time = simulate_boarding(num_rows, strategy(num_rows), sit_time)[2]
        total_time += time
    return total_time/num_trials
        

def compare_strategies(num_rows, sit_time, num_trials):
    time_dictionary = {}
    forward = average_boarding_time(num_rows, sit_time, num_trials, front_to_back_order)
    backwards = average_boarding_time(num_rows, sit_time, num_trials, back_to_front_order)
    random_order = average_boarding_time(num_rows, sit_time, num_trials, random_boarding_order)
    time_dictionary["front_to_back_order"] = forward
    time_dictionary["back_to_front_order"] = backwards
    time_dictionary["random_boarding_order"] = random_order
    return time_dictionary


def greater_compare_strategies(num_rows: list, sit_time: list, num_trials: int) -> tuple:
    storage = {}
    for i in num_rows: 
        for j in sit_time:
            z = compare_strategies(i,j,num_trials)
            z["rows"] = i
            z["sit_time"] = j
            storage[i,j] = z
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
    f_b = 0
    b_b = 0
    r_b = 0
    max_difference = 0
    for test in results.values():
        print(f"\nRows: {test['rows']}, sit_time: {test['sit_time']}")
        front = test["front_to_back_order"]
        back = test["back_to_front_order"]
        random = test["random_boarding_order"]
        maximum = max(front,back,random)
        minimum = min(front,back,random)
        difference = maximum-minimum
        if difference>max_difference:
            max_difference = difference
            largest_gap = f"Largest gap happened at rows = {test['rows']}, sit_time = {test['sit_time']}"
        if minimum == front:
            print(f"Best strategy: front_to_back_order, {front}")
            f_b += 1
        elif minimum == back:
            print(f"Best strategy: back_to_front_order, {back}") 
            b_b += 1
        else:
            print(f"Best strategy: random_boarding_order, {random}")
            r_b += 1
        if maximum == front:
            print(f"Worst strategy: front_to_back_order, {front}")
        elif maximum == back:
            print(f"Worst strategy: back_to_front_order {back}") 
        else:
            print(f"Worst strategy: random_boarding_order {random}")
        print(f"Gap: {difference}")
        print(f"Random gap from best: {random-minimum}")
    winner = max(f_b,b_b,r_b)
    total = f_b + b_b + r_b
    if winner == f_b:
        won = f"Front_to_back won {f_b}/{total} settings"
    elif winner == b_b:
        won = f"Back_to_front won {b_b}/{total} settings"
    else:
        won = f"Random_boarding_order won {r_b}/{total} settings"
    print(f"\nOverall summary \n{won} \n{largest_gap}")


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

print(simulate_boarding(2,[1,2],1))

def test_simulation() -> str:
    boarding_order_front = [1,2]
    front_test = boarding_order_front.copy()
    assert(simulate_boarding(1,[1],0))[2] == 3 
    assert(simulate_boarding(1,[1],1))[2] == 4
    assert(simulate_boarding(2,[1,2],0))[2] == 5
    assert(simulate_boarding(2,[2,1],0))[2] == 4
    assert(simulate_boarding(2,boarding_order_front,1))[2] == 7
    assert(boarding_order_front) == front_test



    return "Simulation tests passed"
    

if __name__ == "__main__":
    results = greater_compare_strategies([5, 10, 20, 40],[0, 1, 2, 3],10)[0]
    for line in results:
        print(line)
    print(test_strategies())
    print(test_simulation())
    plot_strategy_rows(results, fixed_sit_time=1)
    plot_strategy_sit_time(results, fixed_rows=10)
    interpret_strategy(results)
    
