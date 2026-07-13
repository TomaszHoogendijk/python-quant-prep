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

---

## Day 10 — 08/07/2026

### Completed

- Finished the boarding strategy trend interpretation layer.
- Added summary wording for fixed-row and fixed-sit-time slices.
- Cleaned the interpretation output so it describes:
  - best strategy
  - worst strategy
  - strategy gap
  - random gap from best
  - overall win count
  - largest and smallest strategy gaps
  - whether strategy gaps increase or decrease across selected slices
- Fixed misleading trend wording by changing it to:
  - "Within the rows = 20 slice..."
  - "Within the sit_time = 1 slice..."
- Ran final checks before pushing.
- Pushed the working version before starting the cleanup/refactor phase.

### What works now

- The simulator can compare front-to-back, back-to-front, and random boarding strategies.
- The experiment grid can test multiple row counts and sit times.
- Results are stored in dictionaries and reused for:
  - plotting
  - summary output
  - trend interpretation
- The strategy interpretation function can identify the best and worst strategy for each setting.
- The report can summarize whether strategy gaps appear to increase with:
  - larger planes
  - longer passenger blocking times

### Bugs / concepts debugged

- Fixed the wording problem around trend slices.
  - The code was not testing all possible fixed-row or fixed-sit-time values.
  - It was specifically checking the `rows = 20` slice and the `sit_time = 1` slice.
- Reviewed why `assert` works without needing to wrap the full expression in parentheses.
- Added/considered an invariant check that final `wait_time` should be empty after simulation ends.
- Reviewed why `wait_time` is returned and why it can be useful during debugging.
- Understood that `assert simulate_boarding(...)[2] == value` checks the indexed return value directly.
- Reviewed why the movement loop must go backwards so passengers cannot move multiple positions in one timestep.
- Understood why the condition `aisle[position] != position` is necessary:
  - it prevents passengers from moving past their target row.
- Reviewed why the simulator uses a copied boarding order:
  - the original input should not be mutated.
  - the copied list represents the remaining boarding queue.

### Main concepts

- Dictionaries are useful for storing structured experiment results.
- A result dictionary can be reused across plotting, interpretation, and summary logic.
- Simulation code often works by updating state across timesteps.
- Building a "next state" dictionary is safer than removing keys from a dictionary while iterating over it.
- Tests should check exact expected values, not just whether outputs are truthy.
- Naming should describe the model meaning, not only the technical implementation.
  - Example: `mutated_boarding_order` works technically, but `boarding_queue` or `remaining_boarding_order` is clearer.
- The current code works, but the next improvement phase should focus on readability and function structure.

### Git / workflow

- Performed final checks before pushing the working version.
- Pushed the trend interpretation version before beginning the cleanup/refactor phase.
- Decided to separate feature completion from cleanup work.

### Reflections

- The `interpret_strategy()` task was large and difficult, but useful.
- It forced the use of dictionaries, stored results, trend logic, and output generation together.
- The task made it clear that the next bottleneck is code hygiene, not core logic.
- Current pattern:
  - logic is ahead of coding cleanliness
  - the code works
  - the next phase is making the code easier to read and maintain

### Next steps

- Start Day 11 with cleanup/refactoring.
- Improve unclear variable names.
- Replace manual sequence-building logic where cleaner built-in patterns exist.
- Consider renaming:
  - `mutated_boarding_order`
  - `adjust_wait_time`
  - unclear temporary variables like `z`
- Later split long functions, especially `interpret_strategy()`, into smaller helper functions.

---

## Day 11 — 09/07/2026 — Cleanup, naming, and refactor preparation

### Commit / project

Boarding simulation cleanup/refactor phase.

### What works

- Boarding simulator still runs end-to-end.
- Strategy comparison works for front-to-back, back-to-front, and random boarding.
- Average boarding time still works over repeated trials.
- Experiment grid still works across row counts and sit times.
- Plotting functions still work for fixed row / fixed sit-time views.
- Interpretation/reporting layer still works, although it is too long and needs to be split.
- Tests for strategy generation and simulator edge cases still exist.

### What I changed

- Cleaned variable names in strategy comparison functions.
- Added clearer type hints in several functions.
- Replaced unclear plotting variables like `yf`, `yb`, `yr` with `y_front`, `y_back`, and `y_random`.
- Removed leftover debug print output from plotting.
- Improved names inside `interpret_strategy()`:
  - `scores` became average-time-based naming.
  - `difference` became `worst_best_gap`.
  - `wins` became `wins_count`.
  - `test` became `result`.
  - max/min gap variables became more explicit.
- Noticed that `interpret_strategy()` is doing too many jobs and should be split later.

### What I debugged / understood independently

- `git diff` is not a timeline of all historic edits. It compares the last committed version against the current uncommitted working file.
- Diff output is grouped by file location, not by the order in which edits were made.
- Unsaved editor changes may not be included in a commit.
- A function returning many values is possible, but too many returned values may signal that related state should eventually be grouped more cleanly.
- Good variable names should preserve the model meaning, not just sound nicer.

### Concepts learned

- Semantic naming matters: `scores` was misleading because lower average time is better.
- `max(average_time_per_strategy, key=average_time_per_strategy.get)` is clearer when the dictionary name matches the business logic.
- `worst_best_gap` is more precise than a generic `difference`.
- Refactoring should be incremental: first naming, then helper extraction.
- Long functions should be split by responsibility, not by line count.
- `interpret_strategy()` likely contains at least two major responsibilities:
  - per-setting analysis/reporting
  - overall summary/trend reporting

### Remaining cleanup targets

- Split the interpretation logic into smaller helper functions.
- Separate calculation from printing/reporting.
- Clean the repeated trend-classification logic.
- Keep the simulator behavior unchanged while refactoring.
- Add stronger tests around interpretation data later.
- Improve exact type hints for result dictionaries later.

### Next step

Continue refactoring the strategy interpretation code by separating data collection from printed reports.

---

## Day 12 — 10/07/2026 — Interpretation refactor and trend cleanup

### Commit / project

Boarding simulation interpretation refactor.

### What works

- Boarding simulator still runs end-to-end.
- Strategy comparison still works across front-to-back, back-to-front, and random boarding.
- Experiment grid still works across row counts and sit times.
- Plotting functions still work.
- Strategy interpretation still prints per-setting results and overall summaries.
- Existing simulator and strategy sanity tests still pass.

### What I changed

- Split the old interpretation logic into clearer responsibilities:
  - one function collects interpretation data
  - one function prints the per-setting report
  - one function prints the overall report
- Renamed interpretation functions to use clearer action-based names:
  - `collect_strategy_interpretation_data`
  - `print_strategy_per_setting_report`
  - `print_strategy_overall_report`
- Removed printing from the data-collection function.
- Kept per-setting reporting focused on local setting information:
  - best strategy
  - worst strategy
  - strategy gap
  - random gap from best
- Kept overall reporting focused on cross-setting information:
  - win counts
  - largest and smallest gaps
  - fixed-row trend
  - fixed-sit-time trend
- Removed unused total-gap variables.
- Removed unnecessary lists that only existed to count comparisons.
- Replaced those lists with direct comparison counts for each trend slice.

### What I debugged / understood independently

- A function that both prints and returns data is harder to reason about.
- Data collection and reporting are separate responsibilities.
- Per-setting output should not contain overall experiment logic.
- Largest and smallest gap tracking belongs to the overall summary, not to one setting.
- Fixed-row and fixed-sit-time trend logic need separate comparison counts.
- Storing intermediate values is unnecessary when they are only used to calculate a count.
- Simpler state makes refactored code easier to understand.

### Concepts learned

- Refactoring means preserving behavior while improving structure.
- Function names should describe the action:
  - `collect...` means return data
  - `print...` means produce console output
- A long function should be split by responsibility, not only by length.
- Local analysis and overall analysis should be kept separate.
- Removing unused variables removes false meaning from the code.
- Trend classification only needs:
  - a direction score
  - a comparison count
- Different experiment slices can have different numbers of comparisons.

### Git / workflow

- Ran the boarding simulation before committing.
- Used `git status` and `git diff` before pushing.
- Committed the interpretation refactor in small cleanup commits.
- Fixed save and staging issues by using Save All and checking Git status carefully.

### Next steps

- Clean the duplicated trend-classification logic.
- Consider extracting a helper for classifying increasing, decreasing, or neutral trends.
- Sort fixed-row and fixed-sit-time gap dictionaries before comparing trend direction.
- Fix the `for line in results` loop so it prints readable overview lines instead of dictionary keys.
- Add a small test for `collect_strategy_interpretation_data`.

---

## Day 13 — 11/07/2026 — Probability experiments

### Commit / project

Card-hand probability and consecutive-seating Monte Carlo experiments.

### What works

- A card probability experiment compares an empirical Monte Carlo estimate with an exact theoretical probability.
- A consecutive-seating simulation estimates the probability that one fixed group of people sits together in a random seating arrangement.
- Both probability experiments run independently from the boarding simulator.

### What I changed

- Added `probability_experiments/card_probabilities.py`.
- Built an empirical card-hand probability function using `random.sample(..., counts=...)`.
- Built a theoretical card-hand probability function using `math.comb(...)`.
- Added a main guard so the card probability script can be run directly.
- Renamed the card probability file to better describe its purpose.
- Added a Monte Carlo simulation for consecutive seating.
- Reduced the seating representation to:
  - `"success"` for members of the designated group
  - `"failure"` for everyone else
- Checked consecutive windows using list slicing.
- Added `break` so each successful seating arrangement is counted only once.
- Added input validation using `raise ValueError`.
- Renamed the success counter to `successful_trials`.
- Fixed the spelling of `"success"`.
- Ran the consecutive-seating simulation with `(14, 3, 100_000)` and checked that the result was close to the theoretical probability `3/91`.
- Committed and pushed the probability experiments.

### What I debugged / understood independently

- The card-hand probability can be approached both empirically and theoretically.
- Sampling card suits without replacement can be modelled with `random.sample(..., counts=...)`.
- The theoretical card-hand probability is calculated using combinations for the requested number of cards from each suit.
- The identities and internal order of the designated people do not affect the consecutive-seating event.
- Only the seat positions occupied by the designated group matter.
- Replacing distinct people with `"success"` and `"failure"` labels preserves the relevant probability.
- Direct list membership does not check whether one list appears as a consecutive sublist.
- A sliding-window loop can inspect every possible consecutive block.
- `break` prevents one trial from being counted more than once.

### Concepts learned

- Monte Carlo simulation can approximate probabilities.
- Combinatorics can calculate exact probabilities.
- Comparing empirical and theoretical results helps verify probability reasoning.
- A probability model can often be simplified by removing information that does not affect the event.
- `math.comb(...)` calculates combinations.
- `random.sample(..., counts=...)` can sample from repeated categories without replacement.
- List slicing can be used to inspect fixed-length consecutive windows.
- `raise ValueError` is appropriate for invalid function inputs.
- Probability experiments can be separated into domain-specific files inside one folder.

### Git / workflow

- Clarified that `git diff` shows unstaged tracked-file changes.
- Used `git diff --cached` or `git diff --staged` to inspect staged changes.
- Used `git diff --cached --stat` for a compact staged-change summary.
- Used `git add -A` to stage new, modified, and deleted files across the repository.
- Learned that a renamed file can initially appear as one deleted file and one untracked file until both sides are staged.
- Ran both probability scripts before committing.
- Committed and pushed the completed Day 13 work.

### Next steps

- Consider adding the general theoretical probability for consecutive seating.
- Add small automated checks for the probability experiments.
- Continue the remaining boarding-simulator interpretation cleanup.
- Add another probability experiment only when it introduces a genuinely new modelling idea.

---

## Day 14 — 12/07/2026 — Room-assignment probability experiment

### Commit / project

General empirical and theoretical room-assignment probability experiment.

### What works

- An empirical Monte Carlo simulation estimates the probability of a specified room-occupancy pattern.
- A generalized theoretical function calculates the exact probability of the same occupancy pattern.
- Occupancy patterns with the same values in different room orders are treated as equivalent.
- A plot compares independent empirical estimates at increasing trial counts with the exact theoretical probability.

### What I changed

- Added `probability_experiments/room_assignment.py`.
- Built `room_assignment_empirical(...)`.
- Modelled each person as independently selecting one of the labeled rooms using `random.choices(...)`.
- Counted the number of people assigned to each room using `list.count(...)`.
- Stored each trial as a room-occupancy list.
- Used sorted occupancy lists so patterns such as `[3, 3, 1, 1]` and `[3, 1, 3, 1]` are treated as equivalent.
- Added validation that:
  - the occupancy-list length equals the number of rooms
  - the occupancy values sum to the number of people
- Built `room_assignment_theoretical(...)`.
- Counted assignments for one fixed room order using successive `math.comb(...)` calculations.
- Used `Counter` to count repeated occupancy sizes.
- Calculated the number of distinct ways occupancy sizes can be assigned to labeled rooms.
- Divided favorable assignments by `number_of_rooms ** number_of_people`.
- Added `plot_theoretical_empirical(...)`.
- Plotted independent empirical estimates against a constant theoretical reference line.
- Used unconnected markers for the independent empirical estimates.
- Evaluated every fifth trial count to reduce runtime and visual clutter.

### What I debugged / understood independently

- For eight distinct people and four labeled rooms, the total number of possible assignments is `4 ** 8`.
- A fixed room order and an occupancy pattern in any room order are different events.
- Repeated occupancy values require counting distinct room arrangements without overcounting identical values.
- For `[3, 3, 1, 1]`, the distinct room-order factor is:
  - `math.comb(4, 2) * math.comb(2, 2)`
- Assigning `remaining_assignment = assignment` creates two references to the same list.
- Mutating one reference therefore also mutates the original list.
- Using `assignment.copy()` prevents this aliasing bug.
- Printing intermediate results helped isolate which section of the theoretical function worked and why the later loop did not run.
- Calculating fresh empirical estimates for every trial count creates rapidly increasing runtime.
- Independent estimates should not be connected as though they form one cumulative simulation path.

### Concepts learned

- `random.choices(...)` samples with replacement.
- `list.count(...)` counts occurrences of a value.
- `Counter` can represent occupancy multiplicities.
- Sequential combinations can count assignments of distinct people into labeled groups.
- Repeated group sizes require a separate count for their distinct arrangements.
- A shallow copy is sufficient for a list containing immutable integers.
- Comparing empirical and theoretical probabilities helps validate both simulation code and combinatorial reasoning.
- Plot design should reflect whether observations are independent or cumulative.

### Git / workflow

- Ran the room-assignment script before committing.
- Used intermediate print statements during debugging and removed them after identifying the mutation problem.
- Committed and pushed the working room-assignment experiment and comparison plot.

### Next steps

- Improve remaining abbreviated variable names.
- Test additional occupancy patterns.
- Add automated probability checks.
- Consider a genuinely cumulative convergence plot later.

---

## Day 15 — 13/07/2026 — Room-assignment naming cleanup

### Completed

- Improved names in the empirical-versus-theoretical plotting function.
- Replaced abbreviated plotting variables with:
  - `trial_counts`
  - `theoretical_probabilities`
  - `empirical_probabilities`
- Renamed the occupancy-multiplicity dictionary to `room_count_by_occupancy`.
- Renamed its loop value to `room_count`.
- Kept empirical estimates as unconnected markers.
- Kept the theoretical probability as a constant reference line.
- Ran the script after the naming cleanup.
- Reviewed the working-tree changes before committing.

### Concepts reinforced

- Variable names should describe mathematical meaning rather than only their technical type or axis.
- Dictionary names should make the meaning of both keys and values understandable.
- Independent simulation estimates should not automatically be connected by a line.
- Small cleanup commits are useful after a working feature has already been pushed.

### Next steps

- Add automated checks for several valid occupancy patterns.
- Test patterns that include empty rooms.
- Consider simplifying the fixed-order theoretical calculation after tests are in place.
- Continue the remaining boarding-simulator interpretation cleanup.
