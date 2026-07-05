# Learning Log

This log tracks my Python simulation progress while preparing for quant/trading-style problems.

## Day 1 — 29/06/2026

Started basic Python practice.

Covered:
- Lists
- Dictionaries
- Basic functions
- User input
- Simple data storage

Built:
- A list practice function
- A dictionary/person information function
- A dice generator that simulates rolls and calculates total, mean, z-score, and percentile

Main concept:
- Python functions can take inputs, store intermediate values, and return structured results.

---

## Day 2 — 30/06/2026

Built a rolling average function.

Covered:
- `deque(maxlen=50)`
- Keeping a rolling history
- Updating state across function calls
- Calculating an average from stored past values

Main concept:
- Some functions depend not only on current input, but also on remembered previous values.

---

## Day 4–5 — 02/07/2026 to 03/07/2026

Built the dice simulation project.

Covered:
- Simulating two dice with `random.randint(1, 6)`
- Counting outcomes in a dictionary
- Converting counts into probabilities
- Computing the expected sum
- Returning structured results from a function
- Plotting counts and probabilities with matplotlib

Built:
- `simulate_dice(n)`
- `plot_dice(result)`

Main concepts:
- Dictionaries for frequency counts
- `.keys()` and `.values()`
- `plt.subplot(...)`
- `plt.bar(...)`
- `plt.tight_layout()`
- Type hints like `dict` and `None`
- Why `.copy()` matters for mutable objects

---

## Day 5–6 — 03/07/2026 to 04/07/2026

Built and cleaned up the airplane boarding simulator.

Covered:
- State-based simulation
- Timesteps
- List mutation
- Backwards loops
- Blocking behavior
- Wait timers
- Entering and exiting passengers
- Stop conditions
- Saving history with `.copy()`

Built:
- `simulate_boarding(num_rows, boarding_order, sit_time)`

Main concepts:
- The aisle is the state.
- The aisle index represents the passenger's current position.
- The aisle value represents the passenger's target row.
- Looping from back to front prevents one passenger from moving multiple times in one timestep.
- Temporary dictionaries can be used to avoid changing dictionary size while iterating.

Important insight:
- Do not think “loop over passengers.”
- Think “loop over positions and update the state stored at each position.”

Mental model:

```text
aisle index = where someone currently is
aisle value = where that person wants to go
```

---

## Current status after Day 6

Projects built so far:
- Dice generator
- Dice simulation
- Dice probability plotting
- Airplane boarding state-machine simulation
- Basic GitHub repo structure

Next steps:
- Manually test tiny boarding cases
- Add a total boarding time metric
- Add random boarding orders
- Compare boarding strategies
- Plot average boarding times
- Later: animate the boarding process

Also started organizing the codebase for GitHub:
- Moved clean projects into separate files/folders
- Kept `replicate.py` as scratch/backup
- Added `README.md`
- Added `.gitignore`
- Prepared repo structure for GitHub

---

## Day 6 — 04/07/2026

Extended the boarding simulator from a single simulation into a strategy comparison tool.

Covered:
- Building helper functions around an existing simulator
- Creating fixed boarding orders
- Creating random boarding orders
- Computing average boarding time over multiple trials
- Comparing strategies with a returned dictionary
- Debugging deterministic versus random behavior

Built:
- `front_to_back_order(num_rows)`
- `back_to_front_order(num_rows)`
- `random_boarding_order(num_rows)`
- First version of `average_boarding_time(num_rows, sit_time, num_trials, strategy)`
- First version of `compare_strategies(num_rows, sit_time, num_trials)`

Main concepts:
- A fixed strategy can reuse the same order.
- A random strategy must generate a new order for each trial.
- Repeating one random list many times is not the same as averaging over random boarding orders.
- Simulation output becomes more useful when it can be summarized and compared.

Important issue found:
- `random_boarding_order(num_rows)` was generated once before averaging.
- This meant the same random order was reused every trial.
- Since `simulate_boarding()` is deterministic for a given order, this was not a real Monte Carlo average.

Next step:
- Refactor `average_boarding_time()` so it receives a strategy function and calls it inside each trial.

---

## Day 7 — 05/07/2026

Fixed the random strategy averaging issue and cleaned the strategy comparison layer.

Covered:
- Passing functions as arguments
- Calling a strategy function inside a trial loop
- Distinguishing a function from the result of calling a function
- Returning total boarding time from the simulator
- Using `git diff` to review changes before committing
- Understanding Git’s `No newline at end of file` warning

Built / updated:
- `simulate_boarding(...)` now returns `total_time`
- `average_boarding_time(...)` now calls `strategy(num_rows)` inside each trial
- `compare_strategies(...)` returns average boarding times for:
  - front-to-back boarding
  - back-to-front boarding
  - random boarding

Main concept:
- `strategy = random_boarding_order` stores the function.
- `strategy(num_rows)` calls the function and creates an order.
- For random boarding, calling the function inside the loop creates a fresh random order each trial.

Why this matters:
- Front-to-back and back-to-front are deterministic, so their average times stay fixed.
- Random boarding changes each trial, so its average converges as the number of trials increases.
- The sample mean of many random boarding times should stabilize around the expected boarding time.

Example output:
```text
{
    "front_to_back_order": 16.0,
    "back_to_front_order": 8.0,
    "random_boarding_order": approximately 12.4
}
```
