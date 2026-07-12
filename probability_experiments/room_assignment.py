import random
import math
from collections import Counter


def room_assignment_empirical(number_of_rooms: int, number_of_people: int, assignment: list[int], num_trials: int) -> float:
    if len(assignment) != number_of_rooms or sum(assignment) != number_of_people:
        raise ValueError("Invalid input")
    successful_trials_count = 0
    for trial in range(num_trials):
        room_occupancy = []
        people_occupancy = random.choices(population=range(1, number_of_rooms+1), k=number_of_people)
        for room in range(1, number_of_rooms+1):
            people_in_room = people_occupancy.count(room)
            room_occupancy.append(people_in_room)
        if sorted(room_occupancy) == sorted(assignment):
            successful_trials_count += 1
    return successful_trials_count/num_trials

def room_assignment_theoretical(number_of_rooms: int, number_of_people: int, assignment: list[int]) -> float:
    if len(assignment) != number_of_rooms or sum(assignment) != number_of_people:
        raise ValueError("Invalid input")
    favorable_outcomes = 1 
    remaining_people = number_of_people
    remaining_assignment = assignment.copy()
    total_outcomes = number_of_rooms**number_of_people
    while True: #Assign all people with one fixed order
        favorable_outcomes *= math.comb(remaining_people, remaining_assignment[0])
        remaining_people -= remaining_assignment[0]
        remaining_assignment.pop(0)
        if remaining_assignment == []:
            break
    room_count_by_occupancy = dict(Counter(assignment))
    remaining_rooms = number_of_rooms
    for room_count in room_count_by_occupancy.values():
        favorable_outcomes *= math.comb(remaining_rooms, room_count)
        remaining_rooms -= room_count
    return favorable_outcomes/total_outcomes
    
        
if __name__ == "__main__":
    print(room_assignment_empirical(4,8,[3,3,1,1],10000))
    print(room_assignment_theoretical(4,8,[3,3,1,1]))
