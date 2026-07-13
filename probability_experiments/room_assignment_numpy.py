import numpy as np
import time

def room_assignment(num_rooms: int, num_people: int, assignment: list[int], num_trials: int) -> float:
    if (len(assignment) != num_rooms or sum(assignment) != num_people or num_people<1 or num_rooms<1 
        or num_trials<1 or any(value<0 for value in assignment)):
        raise ValueError("Invalid input")
    assignment_shape = (num_trials, num_people)
    outcomes = np.random.randint(1, num_rooms+1, size=assignment_shape)
    room_counts = []
    for room in range(1, num_rooms+1):
        room_counts.append((outcomes==room).sum(axis=1))
    occupancy_matrix = np.array(room_counts).T
    sorted_occupancy = np.sort(occupancy_matrix, axis=1)
    sorted_assignment = np.sort(assignment)
    matches = (sorted_occupancy == sorted_assignment).all(axis=1)
    successful_trials = matches.sum()   
    return successful_trials/num_trials


if __name__ == "__main__":
    start_time = time.perf_counter()
    result = room_assignment(4,8,[3,3,1,1],10000000)
    end_time = time.perf_counter()
    run_time = end_time-start_time
    print(result)
    print(run_time)
    
