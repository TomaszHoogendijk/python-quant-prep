import random
import matplotlib.pyplot as plt

def coin_pair_v(num_trials:int) -> float:
    if num_trials<1:
        raise ValueError("Invalid input")
    total_actions = 0
    for trial in range(num_trials):
        actions = 4
        desired_outcome = ["heads"]*4
        coin_outcome = random.choices(population=["heads","tails"],k=4)
        while coin_outcome != desired_outcome:
            for index in range(len(coin_outcome)):
                if coin_outcome[index] == "tails":
                    coin_outcome[index] = "heads"
                    forbidden_index = index
                    break
            for index in range(len(coin_outcome)):
                if index == forbidden_index:
                    continue
                if "tails" not in coin_outcome:
                    coin_outcome[index] = random.choice(["heads", "tails"])
                    break
                elif "tails" in coin_outcome:
                    if coin_outcome[index] == "tails":
                        coin_outcome[index] = random.choice(["heads", "tails"])
                        break
            actions += 2
        total_actions += actions
    mean_actions = total_actions/num_trials
    return mean_actions
            
def plot_coin_pair_v(num_trials:int, num_trials_means: int) -> None:
    if num_trials_means<1:
        raise ValueError("Invalid input")
    mean_actions_list = []
    for trial in range(num_trials_means):
       mean_actions = coin_pair_v(num_trials)
       mean_actions_list.append(mean_actions)
    plt.hist(mean_actions_list, bins=25, edgecolor="black")
    plt.xlabel("mean number of actions")
    plt.ylabel("frequency")
    plt.show()

if __name__ == "__main__":
    plot_coin_pair_v(100,10000)

