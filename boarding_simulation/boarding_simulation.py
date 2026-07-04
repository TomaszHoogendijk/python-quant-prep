def simulate_boarding(num_rows: int, boarding_order: list, sit_time: float):
    time_stamps = {}
    time = 0
    aisle = [""]*(num_rows+1)
    time_stamps[time] = aisle.copy()
    wait_time = {}
    state = True
    while state==True:
        adjust_wait_time = {}
        for i in wait_time:
                wait_time[i] -=1
                if wait_time[i] == 0:
                    aisle[i] = ""
                else:
                    adjust_wait_time[i] = wait_time[i]
        wait_time = adjust_wait_time
        for position in range(num_rows-1,-1,-1):
            if aisle[position+1] == "" and aisle[position] != "" and aisle[position] != position:
                aisle[position+1] = aisle[position]
                aisle[position] = ""
                if aisle[position+1] == position+1:
                    wait_time[position+1] = sit_time
        time += 1
        if aisle[0] == "" and boarding_order!=[]:
            aisle[0] = boarding_order[0]
            boarding_order.pop(0)
        time_stamps[time] = aisle.copy()
        if all(x == "" for x in aisle) and boarding_order == []:
            state = False
    return time_stamps, wait_time


if __name__ == "__main__":
    print(simulate_boarding(10,[10, 3, 7, 1, 9],2))
