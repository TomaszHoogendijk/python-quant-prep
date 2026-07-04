import random
import statistics
import math
from collections import deque
import matplotlib.pyplot as plt

# Day 1 29/6/2026

# List practice
def list_function():
    my_list = []
    my_list.append("Amsterdam")
    print(my_list)


# Dictionary practice
def person_information():
    name  = input("What is your name? ")
    age = int(input("What is your age? "))
    height = int(input("What is your height? "))
    my_dictionary = {"name":name,"age":age,"height":height}
    return my_dictionary

# Dice generator + percentile of outcome using Z score
def dice_generator(n):
    my_dictionary = {}
    for i in range(n):
        z = random.randint(1,6)
        my_dictionary[i] = z
    total = sum(my_dictionary.values())
    mean = total/n
    sigma = math.sqrt(35/12)
    z_score = (mean-3.5)/(sigma/math.sqrt(n))
    percentile = 100*(1 - statistics.NormalDist().cdf(z_score))
    return {"n": n, "total": total, "mean": mean, "percentile": percentile, "z_score": z_score}

#Day 2 30/6/2026

# Rolling average function, limit of 50
history = deque(maxlen=50)
def rolling_average(f_mid: float, s_mid: float):
    basis = f_mid-s_mid
    history.append(basis)
    return sum(history)/len(history)

# Day 4 2/7/2026 + day 5 3/7/2026 (cleaned up)

def simulate_dice(n):
    rolls_dictionary = {}
    for i in range(n):
        roll_one = random.randint(1, 6)
        roll_two = random.randint(1, 6)
        dice_sum = roll_one+roll_two
        if dice_sum in rolls_dictionary:
            rolls_dictionary[dice_sum] += 1
        else:
            rolls_dictionary[dice_sum] = 1 
    counts = {}
    probabilities = {}
    total = 0
    # Sorting (I am cooked bro)
    for i in range(2,13):
        if i in rolls_dictionary:
            total += rolls_dictionary[i]*i
            counts[i] = rolls_dictionary[i]
            probabilities[i] = rolls_dictionary[i]/n
        else:
            continue 
    expected_sum = total/n
    result = {}
    result["counts"] = counts
    result["probabilities"] = probabilities
    result["expected sum"] = expected_sum
    return result

result = simulate_dice(2000)

def plot_dice(result: dict) -> None:
    plt.figure()
    plt.subplot(1,2,1)
    x = list(result["counts"].keys())
    y = list(result["counts"].values())
    plt.bar(x,y)
    plt.xlabel("Sum of 2 dice")
    plt.ylabel("Count")
    plt.title("Occurrence of a 2 dice sum")
    plt.subplot(1,2,2)
    x_prob = list(result["probabilities"].keys())
    y_prob = list(result["probabilities"].values())
    plt.bar(x_prob,y_prob)
    plt.xlabel("Sum of 2 dice")
    plt.ylabel("Probability")
    plt.title("Probability of a 2 dice sum")
    plt.tight_layout()
    plt.show()

# Day 5 3/7/2026 + day 6 4/7/2026 (cleaned up)

def simulate_boarding(num_rows: int, boarding_order: list, sit_time: float):
    time_stamps = {} # Empty dictionary to store state at different timestamps
    time = 0 # Time start = 0
    aisle = [""]*(num_rows+1) # Initialize an empty aisle with 10 rows, 0 being entry and 1 being row 1
    time_stamps[time] = aisle.copy() # Important to use copy to not keep referring to the variable
    wait_time = {} # Empty dictionary to store wait time state per person
    state = True # Set a variable to True for the loop
    while state==True:
        # Wait time diminishes at the start of the loop, so after a new t has happened.
        # Wait time -1 for every wait time, if it reaches 0 then the aisle slot becomes empty.
        adjust_wait_time = {}
        for i in wait_time:
                wait_time[i] -=1
                if wait_time[i] == 0:
                    aisle[i] = ""
                else: 
                    adjust_wait_time[i] = wait_time[i]
        wait_time = adjust_wait_time
        # Loop, for every position
        for position in range(num_rows-1,-1,-1):
            # If spot ahead is empty and they are not at the right spot, move them a spot up
            if aisle[position+1] == "" and aisle[position] != "" and aisle[position] != position:
                aisle[position+1] = aisle[position]
                aisle[position] = ""
                # If that moving cause them to be at the right spot
                if aisle[position+1] == position+1:
                    wait_time[position+1] = sit_time
        # Increase time    
        time += 1
        # Move the boarding order to the aisle
        if aisle[0] == "" and boarding_order!=[]:
            aisle[0] = boarding_order[0]
            boarding_order.pop(0)
        time_stamps[time] = aisle.copy()
        if all(x == "" for x in aisle) and boarding_order == []:
            state = False
    return time_stamps, wait_time
    

   
print(simulate_boarding(10,[10, 3, 7, 1, 9],2))


