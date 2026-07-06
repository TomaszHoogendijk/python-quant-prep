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

### Completed

- Fixed the random-strategy averaging bug in the boarding simulator.
- Updated `average_boarding_time()` so it receives a strategy function instead of a pre-generated boarding order.
- Confirmed that deterministic strategies reuse the same logical order each trial, while the random strategy generates a fresh order each trial.
- Added basic sanity tests for the strategy helper functions and strategy-comparison output.
- Cleaned the `if __name__ == "__main__"` section so it only runs the sanity test output.
- Used `git diff`, committed the working update, and pushed the changes to GitHub.

### What works now

- `front_to_back_order(num_rows)` returns rows in ascending order.
- `back_to_front_order(num_rows)` returns rows in descending order.
- `random_boarding_order(num_rows)` returns a valid random permutation of all rows.
- `compare_strategies(num_rows, sit_time, num_trials)` returns a dictionary with average boarding times for:
  - front-to-back
  - back-to-front
  - random boarding
- Sanity tests confirm the basic output structure and expected helper-function behavior.

### Bugs / concepts debugged

- Understood the difference between passing a function object and calling a function:
  - `random_boarding_order` passes the function.
  - `random_boarding_order(num_rows)` creates one specific random order.
- Fixed the Monte Carlo issue where one random order was reused across trials.
- Learned how `assert` can be used for basic sanity tests.
- Learned that testing each condition separately makes failures easier to locate.
- Clarified dictionary key testing:
  - `result.keys()` gives the dictionary keys.
  - `set(result.keys()) == expected_keys` checks that the output has exactly the expected strategy names.
- Saw why lists are unhashable and why checking a whole list with `in result.keys()` is not the right logic.

### Tests added

Basic sanity tests now check:

- `front_to_back_order(5) == [1, 2, 3, 4, 5]`
- `back_to_front_order(5) == [5, 4, 3, 2, 1]`
- `random_boarding_order(5)` contains exactly the numbers 1 through 5
- `compare_strategies(5, 1, 10)` returns a dictionary
- the comparison dictionary contains exactly the expected strategy names
- the strategy averages are returned as floats

### Git / workflow

- Used `git diff` to inspect changes before committing.
- Cleaned the main demo output.
- Committed and pushed the completed Day 7 work.

### Next steps

- Add a basic bar chart for strategy comparison results.
- Keep the plotting simple: no pandas, no animation, no extra simulator realism yet.
- Later, add more structured tests for `simulate_boarding()` itself using small deterministic examples.
