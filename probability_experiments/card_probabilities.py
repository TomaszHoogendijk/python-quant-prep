import random
import math

def card_game_empirical(spades: int, clubs: int, hearts: int, diamonds: int, num_trials: int) -> float:
    total_cards_drawn = spades + clubs + hearts + diamonds
    total_trials = 0
    favorable_trials = 0
    for trial in range(num_trials):
        trial_outcome = random.sample(["spades", "clubs", "hearts", "diamonds"], counts=[13, 13, 13, 13], k=total_cards_drawn)
        total_trials += 1
        spades_outcome = trial_outcome.count("spades")
        hearts_outcome = trial_outcome.count("hearts")
        clubs_outcome = trial_outcome.count("clubs")
        diamonds_outcome = trial_outcome.count("diamonds")
        if spades_outcome == spades and hearts_outcome == hearts and clubs_outcome == clubs and diamonds_outcome == diamonds:
            favorable_trials += 1
    probability_favorable_outcome = favorable_trials/total_trials
    return probability_favorable_outcome

def card_game_theoretical(spades: int, clubs: int, hearts: int, diamonds: int) -> float:
    total_cards_drawn = spades + clubs + hearts + diamonds
    favorable_outcomes = math.comb(13, spades) * math.comb(13, clubs) * math.comb(13, hearts) * math.comb(13, diamonds)
    total_outcomes = math.comb(52, total_cards_drawn)
    probability_favorable_outcome = favorable_outcomes/total_outcomes
    return probability_favorable_outcome

if __name__ == "__main__":
    print(card_game_empirical(6,2,3,2, 1000))
    print(card_game_theoretical(6,2,3,2))

