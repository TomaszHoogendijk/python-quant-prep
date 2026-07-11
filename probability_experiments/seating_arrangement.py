import random

def seating_adjacent_probability(total_people: int, adjacent_people: int, num_trials: int) -> float:
    if num_trials<1 or adjacent_people>total_people or adjacent_people<1:
        raise ValueError("Invalid input")
    successful_pattern = ["success"] * adjacent_people
    successful_trials = 0
    remaining_people = total_people-adjacent_people
    for trial in range(num_trials):
        order = random.sample(["success", "failure"], k=total_people, counts=[adjacent_people, remaining_people])
        for i in range(total_people-adjacent_people+1):
            if order[i:i+adjacent_people] == successful_pattern:  
                successful_trials += 1
                break
    return successful_trials/num_trials

if __name__ == "__main__":
    print(seating_adjacent_probability(14,3,100000))
    