import random
import statistics
import math
import matplotlib.pyplot as plt
import time


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

if __name__ == "__main__":
    start_time = time.perf_counter()
    result = simulate_dice(100_000_000)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    print(result)
    print(run_time)