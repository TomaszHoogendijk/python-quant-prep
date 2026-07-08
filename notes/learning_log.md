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

---

## Day 8 — 06/07/2026

### Completed

- Added an experiment layer for the boarding simulator.
- Ran strategy comparisons over multiple combinations of:
  - number of rows
  - `sit_time`
- Stored experiment results in a dictionary using tuple keys like `(rows, sit_time)`.
- Added readable experiment summary output.
- Added plots showing strategy performance:
  - by number of rows for a fixed `sit_time`
  - by `sit_time` for a fixed number of rows
- Added an interpretation layer that identifies the best and worst strategy for each setting.
- Calculated the gap between the fastest and slowest strategy.
- Calculated the random strategy's gap from the best strategy.
- Summarized which strategy won most often and where the largest gap occurred.

### What works now

- The simulator can compare front-to-back, back-to-front, and random boarding across an experiment grid.
- Results are stored instead of only printed.
- Stored results can be reused for summaries, plots, and interpretation.
- The interpretation output gives a readable explanation of the experiment results.

### Bugs / concepts debugged

- Learned that a full grid means every combination of rows and `sit_time`, not just matching pairs.
- Understood that for 4 row settings, 4 `sit_time` settings, 3 strategies, and 100 trials, the simulator runs `4 × 4 × 3 × 100` times.
- Learned why tuple keys like `(rows, sit_time)` work in dictionaries.
- Learned that dictionaries cannot be used as dictionary keys because they are mutable and unhashable.
- Debugged a “not subscriptable” issue while filtering stored experiment results.
- Fixed the random-gap calculation:
  - since lower boarding time is better, random's gap from best is `random - minimum`, not `maximum - random`.
- Used `\n` to make printed output easier to read.

### Main concepts

- Experiment results become more useful when stored in a reusable structure.
- Tuple keys are useful for storing results by multiple dimensions.
- A simulation project should not only generate numbers, but also summarize what the numbers mean.
- Plotting and printed interpretation should tell the same story.
- The results matched the model intuition: back-to-front boarding is fastest because rear passengers move through the aisle before front passengers block it, while front-to-back creates early bottlenecks.

### Git / workflow

- Used `git status`, `git diff`, and ran the boarding simulation before committing.
- Committed and pushed the Day 8 experiment and interpretation updates.

### Next steps

- Add more deterministic tests for `simulate_boarding()` using tiny examples.
- Improve the interpretation code for readability and tie handling.
- Consider reducing repeated strategy-name logic with a small local dictionary.

---

## Day 9 — 07/07/2026

### Completed

- Added deterministic tests for `simulate_boarding()`.
- Tested small hand-checkable boarding scenarios.
- Added a mutation test to confirm that the original `boarding_order` list is not changed by the simulator.
- Improved the interpretation logic by using a `scores` dictionary for strategy times.
- Replaced repeated best/worst strategy logic with `min(..., key=...)` and `max(..., key=...)`.
- Counted how often each strategy wins across the experiment grid.
- Added smallest-gap tracking alongside largest-gap tracking.
- Cleaned the experiment interpretation output.

### What works now

- `simulate_boarding()` is tested directly on small deterministic cases.
- The tests check both timing behavior and input-list mutation behavior.
- The interpretation layer can identify:
  - best strategy
  - worst strategy
  - strategy gap
  - random gap from best
  - win count by strategy
  - largest and smallest strategy gaps

### Bugs / concepts debugged

- Understood that wrapper tests like `average_boarding_time()` are less direct than testing `simulate_boarding()` itself.
- Used timestamp output from `simulate_boarding()` to verify why small examples produce their `total_time`.
- Learned that mutable lists can be changed inside a function even if they are not returned.
- Added a test to confirm that the original boarding order remains unchanged.
- Learned the pattern `min(scores, key=scores.get)`:
  - the function returns the key with the lowest associated value.
  - this is useful when strategy names are keys and boarding times are values.
- Improved win counting by using a dictionary instead of separate manual counters.

### Main concepts

- Core simulation logic should be tested directly with tiny examples.
- Tests protect the simulator before later cleanup or refactoring.
- A dictionary can map strategy names to scores, making best/worst logic cleaner.
- Cleaner data structures reduce repeated conditional logic.
- Public project notes should record progress and concepts learned, not private ratings or career calibration.

### Git / workflow

- Ran the simulator tests before committing.
- Used `git status` and `git diff` before committing.
- Committed and pushed the deterministic simulator tests and interpretation cleanup.

### Next steps

- Finish trend interpretation for the experiment report.
- Summarize whether strategy gaps increase with:
  - more rows
  - higher `sit_time`
- Split the long interpretation function into smaller helper functions after the full report works.
