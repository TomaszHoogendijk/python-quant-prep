import random

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
    

if __name__ == "__main__":
    print(test_strategies())
    