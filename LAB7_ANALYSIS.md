# Lab #7 — From Code to Operation: Investigation Record

**Team:** Duo Minds  
**Student(s) / GitHub handle(s):** Basam Butt — `@201400160-wq`; Waleed Younis — `@Wali007-lab`  
**Fork / working branch:** https://github.com/Wali007-lab/Surprise/tree/lab7-Basam (baseline branch: https://github.com/Wali007-lab/Surprise/tree/lab7-waleed)  
**Upstream project and pinned version:** https://github.com/NicolasHug/Surprise (pinned commit `93e1c30f3b2d15bdd0f2c4c816fbfce59f000fad`, `surprise.__version__ == "1.1.5"`)

## 1. Stakeholder, goal and selected functionality

**Stakeholder concern:** Sam, the release engineer, needs confidence that the software can be installed and executed from our fork in a clean environment, and that delivery checks make an intentional behavior change visible while verifying existing behavior remains intact.

**GQM goal:** Analyze **the Surprise rating-prediction script and its GitHub Actions delivery workflow** for the purpose of **evaluating deployment reliability and behavioral-change verification**, with respect to **reproducible execution from the fork and observable regression detection**, from the viewpoint of **Sam (Release Engineer)**, in the context of **the `Wali007-lab/Surprise` fork and GitHub-hosted Ubuntu environment**.

| Question | Question in your own words | Evidence / measurement and why it helps |
|---|---|---|
| Q1 | Can the Surprise fork be built, installed, and executed for a real rating-prediction case in a fresh GitHub-hosted Ubuntu runner? | Passing Actions runs (`#8` and `#9`), checked-out commit SHA (`git rev-parse HEAD`), imported `surprise.__file__` location, and successful execution of `lab7/predict_rating.py`. Confirms the fork's code actually installs and runs outside the developer machine. |
| Q2 | Do automated checks detect the intentional change in displayed prediction precision while confirming that the underlying SVD estimate and core regression checks remain unchanged? | Formatting tests (`test_format_prediction_uses_one_decimal_place`, `test_predict_rating_cli_output`), numerical equality assertion against an independently trained `SVD(random_state=42)` model (`test_predict_rating_behavior_and_unchanged_estimate`), and existing SVD regression tests (`test_SVD_parameters`, `test_sanity_checks`). Separates the intended display change from any unintended algorithmic drift. |

**Selected function/component:** Rating prediction workflow in [`lab7/predict_rating.py`](https://github.com/Wali007-lab/Surprise/blob/fab663309e80f644cda855f010e2c25a3569c3df/lab7/predict_rating.py) (`compute_prediction` and `format_prediction`, calling `Dataset.load_from_df`, `SVD(random_state=42).fit`, and `algo.predict`).  
**Why this represents the software's purpose:** Surprise is a recommender-system library whose core purpose is training collaborative-filtering models on user–item ratings and predicting unknown ratings. Fitting `SVD` on a ratings dataset and predicting a user–item pair exercises this end-to-end core workflow.  
**Representative input and baseline expectation:** Fixed 4-rating dataset `[("1", "1", 5), ("1", "2", 4), ("2", "1", 3), ("2", "2", 5)]` with `Reader(rating_scale=(1, 5))`, `SVD(random_state=42)`, and prediction query `("1", "3")`. Baseline expectation: prints the unrounded floating-point estimate via `print(f"Prediction: {prediction.est}")` (observed as `Prediction: 4.28800760736211`).  
**Planned small behavior change:** Extract `compute_prediction()` and add application-facing `format_prediction(prediction)` in `lab7/predict_rating.py` to format the displayed rating to one decimal place (`f"Prediction: {prediction.est:.1f}"`, producing `Prediction: 4.3`), while keeping the underlying `SVD` training and numerical estimate identical.  
**What must still work unchanged?** The underlying numerical estimate `prediction.est` (`4.28800760736211` for `("1", "3")` with `SVD(random_state=42)`), `prediction.details["was_impossible"] == False`, rating bounds `[1.0, 5.0]`, and Surprise's existing SVD parameter and sanity regression checks (`tests/test_SVD.py` and `tests/test_algorithms.py`).

## 2. Baseline: deploy and execute on GitHub

| Evidence | Baseline |
|---|---|
| Baseline commit SHA and link | `1b01da1991c3ef31ca15e61045fbae79b92e60ba` — https://github.com/Wali007-lab/Surprise/commit/1b01da1991c3ef31ca15e61045fbae79b92e60ba |
| Actions workflow file link | https://github.com/Wali007-lab/Surprise/blob/1b01da1991c3ef31ca15e61045fbae79b92e60ba/.github/workflows/lab7.yml |
| Ubuntu/runtime and relevant dependency versions | `ubuntu-latest`, CPython `3.12.16`; `scikit-surprise==1.1.5` (built from local fork), `pandas==3.1.1`, `numpy==2.5.5`, `scipy==1.18.1`, `joblib==1.6.0` |
| How the fork's code is installed/built and verified as the executed code | Installed from the checked-out fork via `python -m pip install .` (log: `Building wheel for scikit-surprise (pyproject.toml)` -> `Successfully built scikit-surprise`), then executed via `python lab7/predict_rating.py` (putting `lab7/` on `sys.path[0]` so `surprise` resolves to the installed package rather than an uncompiled checkout). Explicit `git rev-parse HEAD` and `surprise.__file__` logging were not yet in the baseline workflow (`1b01da1`) and were added in Task 3 (`fab6633`). |
| Functional case executed (command/script/test or local endpoint) | `python lab7/predict_rating.py` (loads 4 ratings, fits `SVD(random_state=42)`, calls `algo.predict("1", "3")`) |
| Expected vs observed behavior | Expected: trains `SVD(random_state=42)` and prints `Prediction: <prediction.est>` in full floating-point precision. Observed in Run `#8`: `Prediction: 4.28800760736211`. |
| Check result and meaningful measurement(s), if any | Baseline workflow exited 0 (`completed` / `success`, `2026-11-26T13:49:03Z` to `2026-11-26T13:50:02Z`), producing `Prediction: 4.28800760736211`. Note: the baseline commit did not include automated `pytest` assertions, commit SHA printing, or `surprise.__file__` logging. |
| Exact GitHub Actions run URL | https://github.com/Wali007-lab/Surprise/actions/runs/45832818528 |

**What does this establish, and what does it not establish?** Run `#8` establishes that the fork (`scikit-surprise==1.1.5`) builds and installs cleanly via `pip install .` on a fresh `ubuntu-latest` CPython `3.12.16` runner and that `lab7/predict_rating.py` executes `SVD` training and prediction, printing `Prediction: 4.28800760736211`. It does not establish automated assertion coverage on the output, explicit runtime logging of commit SHA/`surprise.__file__`, or accuracy across larger real-world datasets.

## 3. Controlled change and verification

**Source/function changed:** `format_prediction(prediction)` (with `compute_prediction()` and `main()` extracted) in [`lab7/predict_rating.py`](https://github.com/Wali007-lab/Surprise/blob/fab663309e80f644cda855f010e2c25a3569c3df/lab7/predict_rating.py)  
**Reason for change:** Standardize user-facing predicted rating display to one decimal place (`Prediction: 4.3` instead of `Prediction: 4.28800760736211`) for cleaner presentation without modifying the underlying collaborative-filtering computation.  
**Code-change commit(s):** https://github.com/Wali007-lab/Surprise/commit/fab663309e80f644cda855f010e2c25a3569c3df

| Item | Before change | After change |
|---|---|---|
| Same input/case | 4-row ratings dataset, `SVD(random_state=42)`, query `("1", "3")` | Same 4-row ratings dataset, `SVD(random_state=42)`, query `("1", "3")` |
| Expected behavior under each version's stated contract | Print `Prediction: {prediction.est}` (full float precision) | Print `Prediction: {prediction.est:.1f}` (rounded to 1 decimal place) |
| Observed behavior on GitHub runner | Run `#8` (`ubuntu-latest`, CPython `3.12.16`) printed `Prediction: 4.28800760736211` | Run `#9` (`ubuntu-latest`, CPython `3.12.16`) verified `git rev-parse HEAD` = `fab663309e80f644cda855f010e2c25a3569c3df`, `Surprise path: /home/runner/work/Surprise/Surprise/surprise/__init__.py`, and printed `Prediction: 4.3` |
| Automated case check/result | None in baseline (`1b01da1` only ran the script) | `python -m pytest -v tests/test_lab7_prediction.py` (`pytest-9.2.0`): **3 passed in 0.47s** (`test_format_prediction_uses_one_decimal_place`, `test_predict_rating_behavior_and_unchanged_estimate`, `test_predict_rating_cli_output`) |
| Unchanged regression/invariant check | Baseline `SVD(random_state=42)` estimate (`4.28800760736211`) and Surprise core SVD tests | `test_predict_rating_behavior_and_unchanged_estimate` verifies `was_impossible is False`, `1.0 <= est <= 5.0`, and exact equality with an independently trained `SVD(random_state=42)` model; CI also ran `python -m pytest -v tests/test_SVD.py tests/test_algorithms.py -k "test_SVD_parameters or test_sanity_checks"`: **15 passed, 4 deselected in 1.42s** (including `SVD(random_state=0)` RMSE `1.0077323320656948`) |
| Exact Actions run URL | https://github.com/Wali007-lab/Surprise/actions/runs/45832818528 | https://github.com/Wali007-lab/Surprise/actions/runs/45835966892 |
| Commit SHA | `1b01da1991c3ef31ca15e61045fbae79b92e60ba` | `fab663309e80f644cda855f010e2c25a3569c3df` |

**How do your checks distinguish the two versions?** Baseline Run `#8` printed `Prediction: 4.28800760736211` (14 decimal digits), whereas changed-version Run `#9` printed `Prediction: 4.3` (1 decimal digit, rounding `4.288...` to `4.3` via `:.1f`). In `tests/test_lab7_prediction.py`, `test_format_prediction_uses_one_decimal_place` verifies 1-decimal formatting (`"Prediction: 2.3"` != `"Prediction: 2.3456"`), while `test_predict_rating_behavior_and_unchanged_estimate` and `test_predict_rating_cli_output` verify both that the live `SVD(random_state=42)` output strictly matches `Prediction: {est:.1f}` (`r"Prediction: -?\d+\.\d"`) and that `prediction.est` equals an independently fit baseline `SVD(random_state=42)` model. The 15 passing core tests (`test_SVD_parameters` and `test_sanity_checks`) confirm no regression in Surprise's algorithms.

**Did anything fail unexpectedly? What did you learn or fix?** Earlier baseline iterations on `lab7-waleed` failed before reaching Run `#8` (Run `#2` failed because importing `surprise` from the repo root after non-editable `pip install .` shadowed `site-packages` with the uncompiled source directory; Run `#3` failed YAML indentation; Run `#5` failed because `lab7/predict_rating.py` had not been added yet; Run `#7` failed for missing `pandas`). Locally on Windows, running `pytest` failed collection with `ModuleNotFoundError: No module named 'numpy'` because compiled dependencies are not installed locally, while `python -m py_compile` succeeded. In Task 3 (`fab6633`), switching the workflow to `python -m pip install -e .` and installing `pytest` (`9.2.0`) allowed `python -m pytest` to run cleanly from the repository root, and Run `#9` passed on all steps.

## 4. Engineering judgment and submission

**Answer Q1:** Yes. Both Run `#8` (`1b01da1`) and Run `#9` (`fab6633`) succeeded on a fresh `ubuntu-latest` CPython `3.12.16` runner (`scikit-surprise==1.1.5`, `pandas==3.1.1`, `numpy==2.5.5`, `scipy==1.18.1`), and Run `#9` explicitly logged `git rev-parse HEAD` (`fab663309e80f644cda855f010e2c25a3569c3df`) and `Surprise path: /home/runner/work/Surprise/Surprise/surprise/__init__.py` after editable installation (`pip install -e .`), proving the fork's code built and executed.  
**Answer Q2:** Yes. Run `#9` verified both the intentional 1-decimal display change (`Prediction: 4.28800760736211` -> `Prediction: 4.3`, with `3` tests in `tests/test_lab7_prediction.py` passing) and the unchanged underlying numerical `SVD` behavior (exact equality with an independent `SVD(random_state=42)` model plus `15` passing core regression tests in `tests/test_SVD.py` and `tests/test_algorithms.py`).

**Release decision:** **Accept changed version (pending completion of Task 4 PR and merge into `semester-investigation`).** Both the baseline (`#8`) and changed (`#9`) GitHub Actions runs passed with verified logs, the intended formatting change (`4.28800760736211` -> `4.3`) was detected and verified, and the underlying `SVD` algorithm and regression invariants remain intact. Before final submission, open and merge the PR targeting `semester-investigation` using a merge commit.  
**One important limitation or missing check:** The Lab 7 verification exercises only a small 4-rating synthetic dataset and a single prediction query (`"1"`, `"3"`); it does not test recommendation quality on real datasets, latency under load, or cases where `prediction.est` already happens to end in `.0` (where old and new printed strings would look identical).

| GitHub evidence | Link |
|---|---|
| Lab #7 pull request (within your fork) | `TODO — open pull request from lab7-Basam targeting semester-investigation` |
| **Merged commit** on `semester-investigation` | `TODO — add merge commit URL after merging PR (use merge commit, not squash)` |
| Final `LAB7_ANALYSIS.md` on merged branch | `TODO — add final LAB7_ANALYSIS.md URL on semester-investigation after merge` |
| Student 1 meaningful commit(s) | Basam Butt (`@201400160-wq`): https://github.com/Wali007-lab/Surprise/commit/fab663309e80f644cda855f010e2c25a3569c3df |
| Student 2 meaningful commit(s), if a pair | Waleed Younis (`@Wali007-lab`): https://github.com/Wali007-lab/Surprise/commit/707d7ee1d5c80324a0cb23f41ffe14101dbc4e29, https://github.com/Wali007-lab/Surprise/commit/117599aa93707350b2601a15860bd8e0afd34898, https://github.com/Wali007-lab/Surprise/commit/1b01da1991c3ef31ca15e61045fbae79b92e60ba |

**LLM assistance (if used):** An LLM assisted with inspecting the fork's Git history and GitHub Actions logs, refactoring `lab7/predict_rating.py` into testable helpers, drafting `tests/test_lab7_prediction.py` and `.github/workflows/lab7.yml` updates, and updating `LAB7_ANALYSIS.md`. All file diffs, commit SHAs, dependency versions, prediction outputs (`4.28800760736211` and `4.3`), and test counts (`3 passed`, `15 passed`) were independently verified from Git and GitHub Actions Run `#8`/`#9` logs.

**Submission reminder:** Each student submits `Lab7_YOUR_GITHUB_HANDLE.txt` to the Lab #7 MS Teams submit folder, containing their full name, fork URL, merged-commit URL and final analysis URL.
