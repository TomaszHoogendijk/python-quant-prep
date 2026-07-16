import numpy as np
import time

def dice_simulation(num_trials: int, chunks: int) -> dict:
    if num_trials<1 or chunks<1 or num_trials<chunks or num_trials%chunks != 0:
      raise ValueError("Invalid input")
    total_sum = 0
    for i in range(chunks):
        dice_rolls = np.random.randint(1,7, size = (num_trials//chunks, 2))
        sum_per_trial = dice_rolls.sum(axis=1)
        total_sum += dice_rolls.sum()
        counts_per_integer_chunk = np.bincount(sum_per_trial, minlength=13)
        relevant_counts_chunk = counts_per_integer_chunk[2:13]
        if i == 0:
            relevant_counts = relevant_counts_chunk
        else:
            relevant_counts += relevant_counts_chunk
    probabilities = relevant_counts/relevant_counts.sum()
    counts_dict = {}
    probabilities_dict = {}
    for i in range (2,13):
        counts_dict[i] = int(relevant_counts[i-2])
        probabilities_dict[i] = float(probabilities[i-2])
    expected_sum = total_sum/num_trials
    result = {}
    result["counts"] = counts_dict
    result["probabilities"] = probabilities_dict
    result["expected sum"] = float(expected_sum)
    return result


if __name__ == "__main__":
    start_time = time.perf_counter()
    result = dice_simulation(100_000_000,10)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    print(result)
    print(run_time)