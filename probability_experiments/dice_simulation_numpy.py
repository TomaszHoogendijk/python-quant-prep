import numpy as np
import time

def dice_simulation(num_trials: int) -> dict:
    if num_trials<1:
      raise ValueError("Invalid input")
    dice_rolls = np.random.randint(1,7, size = (num_trials, 2))
    sum_per_trial = dice_rolls.sum(axis=1)
    expected_sum = dice_rolls.sum()/num_trials
    counts_per_integer = np.bincount(sum_per_trial, minlength=13)
    relevant_counts = counts_per_integer[2:13]
    probabilities = relevant_counts/relevant_counts.sum()
    counts_dict = {}
    probabilities_dict = {}
    for i in range (2,13):
        counts_dict[i] = int(relevant_counts[i-2])
        probabilities_dict[i] = float(probabilities[i-2])
    result = {}
    result["counts"] = counts_dict
    result["probabilities"] = probabilities_dict
    result["expected sum"] = float(expected_sum)
    return result


if __name__ == "__main__":
    start_time = time.perf_counter()
    result = dice_simulation(100_000_000)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    print(result)
    print(run_time)