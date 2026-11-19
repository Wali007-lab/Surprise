# Lab #6 - Investigation Record

**Team / student(s):** Basam (`201400160-wq`) & Independent Partner
**Mode:** Pair (reporting Basam's individual contribution)
**Approved upstream project:** [NicolasHug/Surprise](https://github.com/NicolasHug/Surprise)
**Fork / working branch:** [Wali007-lab/Surprise/tree/lab6-Basam](https://github.com/Wali007-lab/Surprise/tree/lab6-Basam)
**Original Lab #5 version:** `93e1c30f3b2d15bdd0f2c4c816fbfce59f000fad`
**Lab #6 pre-refactoring baseline:** [`93e1c30f3b2d15bdd0f2c4c816fbfce59f000fad`](https://github.com/Wali007-lab/Surprise/commit/93e1c30f3b2d15bdd0f2c4c816fbfce59f000fad)

---

## Task 1 - Stakeholder, GQM, and Code Smell Selection

**Selected stakeholder and exact fictional concern from handout:**
Scenario A - Alex, Software Maintainer:
> *"Our software keeps evolving. Future contributors need to understand and modify its components, but certain design choices might make that work unnecessarily difficult. Please investigate possible code smells, identify maintainability concerns worth addressing, and demonstrate a focused improvement without changing the software's intended behavior."*

**GQM goal:**
Analyze **the Surprise recommender system library** for the purpose of **identifying maintainability improvements**, with respect to **code quality and ease of modification**, from the viewpoint of **Alex (Software Maintainer)**, in the context of **the Surprise GitHub repository**.

| Initial question | Question wording | Relevant metric(s) / observation(s) | Why useful? |
|---|---|---|---|
| **Q1** | Which components of the Surprise library exhibit maintainability problems such as excessive complexity, large responsibilities, duplication, or poor structure? | Cognitive Complexity, Method Length (LOC), Class Responsibilities, Duplicated Lines Density, Source Call Coupling. | Identifies where software maintainability risks are concentrated before planning improvements. |
| **Q2** | Which identified maintainability issues can be improved through small behavior-preserving refactorings? | Cyclomatic/Cognitive Complexity delta, Method Length delta, Behavioral Regression Test Outcomes (Exact RMSE equality). | Distinguishes high-risk architectural redesigns from safe, verifiable, high-leverage refactorings. |

**Code-smell types chosen from the lecture:** (6 across the pair; 3 assigned to Basam, 3 assigned independently to partner)

| Smell type | Lecture slide(s) | Why relevant to our GQM? | How we plan to investigate it (tool/rule/metric/inspection) |
|---|---|---|---|
| **1. Long Method** *(Basam)* | Slides 34–45 | Obscures algorithm training flow, mixing allocation, hyperparameters, and math updates, making maintenance difficult. | Manual source inspection of `surprise/prediction_algorithms/matrix_factorization.pyx`, method line counts, and Ruff `C901` complexity. |
| **2. Large Class** *(Basam)* | Slides 53–65 | Monolithic estimator classes that accumulate configuration, validation, fitting, and prediction violate SRP. | SonarQube Cloud class LOC, field count inspection, and architectural analysis of `SVD` and `BaseSearchCV`. |
| **3. Feature Envy** *(Basam)* | Slides 83–92 | Methods that directly reach into the internal data structures of other classes (e.g. `Trainset` internals) increase coupling. | Manual call-graph inspection of `AlgoBase.compute_baselines` and metric extractors in `accuracy.py`. |
| **4. Long Parameter List** *(Partner)* | Slides 46–52 | Excessive parameters in estimator constructors increase coupling and call error rates. | Ruff `PLR0913`, SonarQube `python:S107`. |
| **5. Duplicated Code** *(Partner)* | Slides 20–33 | Cloned rating aggregation and normalization logic across algorithms increases maintenance overhead. | SonarQube Cloud duplication detection, `jscpd` token comparison. |
| **6. Dead Code** *(Partner)* | Slides 75–82 | Unused parameters and unreachable conditionals produce cognitive drag. | SonarQube Cloud rule issues (`python:S1144`, `python:S1172`). |

**Primary GitHub-integrated tool:** [SonarQube Cloud](https://sonarcloud.io/project/overview?id=Wali007-lab_Surprise)
**Complementary tool (only if needed):** Ruff (version `0.14.4`) & `jscpd` (version `5.3.2`) via GitHub Actions
**Why these tools match our questions and selected smells:**
SonarQube Cloud provides top-level maintainability ratings, project-wide cognitive complexity (349), and duplication detection (0.4%). However, because SonarQube's Python engine skips Cython `.pyx` syntax, manual source inspection and targeted GitHub Actions regression workflows are necessary to investigate performance-critical Cython modules like `matrix_factorization.pyx`.

---

## Task 2 - Detect and Investigate Code Smells

**Analysis configuration:**
- Fork branch and **baseline SHA**: `lab6-Basam` at commit `93e1c30f3b2d15bdd0f2c4c816fbfce59f000fad`
- Source directory/directories analyzed: `surprise/` (specifically handwritten Python and Cython modules)
- Exclusions: `doc/**`, `examples/**`, `tests/**` (test fixtures and datasets)
- Tool(s), versions and relevant enabled rules/settings:
  - SonarQube Cloud (Standard Python Quality Profile)
  - Ruff `0.14.4` (`C901`, `PLR0912`, `PLR0913`, `PLR0915`)
  - `jscpd` `5.3.2`
- **Baseline GitHub scan / Actions run link(s):**
  - SonarQube Cloud Project: `https://sonarcloud.io/project/overview?id=Wali007-lab_Surprise`
  - GitHub Actions Python Ruff Run: [Run 44544220815](https://github.com/Wali007-lab/Surprise/actions/runs/44544220815) (Artifact: `lab6-ruff-report`; workflow success confirms execution, not zero findings)
  - GitHub Actions Duplication Run: [Run 44544220480](https://github.com/Wali007-lab/Surprise/actions/runs/44544220480) (Artifact: `lab6-duplication-report`; workflow success confirms report generation, not zero duplication)

| Selected smell type | Found / not found / not assessable | Tool result or source link | Interpretation / limitations |
|---|---|---|---|
| **1. Long Method** *(Basam)* | Found | [matrix_factorization.pyx#L159](https://github.com/Wali007-lab/Surprise/blob/93e1c30f3b2d15bdd0f2c4c816fbfce59f000fad/surprise/prediction_algorithms/matrix_factorization.pyx#L159-L251) | 93-line `SVD.sgd()` method combining 4 responsibilities. Not assessed directly by SonarQube due to Cython syntax; confirmed via source inspection. |
| **2. Large Class** *(Basam)* | Found | [matrix_factorization.pyx#L18](https://github.com/Wali007-lab/Surprise/blob/93e1c30f3b2d15bdd0f2c4c816fbfce59f000fad/surprise/prediction_algorithms/matrix_factorization.pyx#L18-L278) | Class `SVD` has 15 constructor parameters, managing state, SGD optimization, biases, and prediction fallback logic. |
| **3. Feature Envy** *(Basam)* | Found | [algo_base.py#L145](https://github.com/Wali007-lab/Surprise/blob/93e1c30f3b2d15bdd0f2c4c816fbfce59f000fad/surprise/prediction_algorithms/algo_base.py#L145-L210) | `AlgoBase.compute_baselines()` repeatedly accesses internal rating dictionaries (`ur`, `ir`, `n_users`, `n_items`) of `Trainset`. |
| **4. Long Parameter List** *(Partner)* | [Independent partner contribution] | [To be documented independently on partner's branch] | [Independent partner contribution — to be documented independently on partner's branch] |
| **5. Duplicated Code** *(Partner)* | [Independent partner contribution] | [To be documented independently on partner's branch] | [Independent partner contribution — to be documented independently on partner's branch] |
| **6. Dead Code** *(Partner)* | [Independent partner contribution] | [To be documented independently on partner's branch] | [Independent partner contribution — to be documented independently on partner's branch] |

**Candidate issues inspected in source (at least two):**

| Candidate ID | File/entity permalink | What was actually observed? | Why it might matter / why uncertain |
|---|---|---|---|
| **C1** | [matrix_factorization.pyx:159](https://github.com/Wali007-lab/Surprise/blob/93e1c30f3b2d15bdd0f2c4c816fbfce59f000fad/surprise/prediction_algorithms/matrix_factorization.pyx#L159-L251) | `SVD.sgd()` spans 93 lines, combining memory allocation, RNG factor initialization, hyperparameter unpacking, epoch iteration, and rating updates. | Crucial for algorithm maintainers; high risk if inner loop is naively touched due to Cython performance overhead. |
| **C2** | [algo_base.py:145](https://github.com/Wali007-lab/Surprise/blob/93e1c30f3b2d15bdd0f2c4c816fbfce59f000fad/surprise/prediction_algorithms/algo_base.py#L145-L210) | `AlgoBase.compute_baselines()` iterates over `self.trainset.ur` and `self.trainset.ir` directly rather than querying statistical methods on `Trainset`. | Encapsulation violation, but refactoring it changes the shared interface across all 11 recommender algorithms. |

**One warning we challenged, or one potentially missed issue:**
SonarQube Cloud's default automated scan reported **0 code smells** in the maintainability category for the baseline commit. We challenged this tool outcome: SonarQube Cloud only parses standard `.py` ASTs and excludes Cython `.pyx` files from smell rules. This created a false sense of zero maintainability debt, whereas actual source inspection revealed the 93-line `SVD.sgd()` method with multiple mixed responsibilities.

---

## Task 3 - Prioritize Technical Debt and Plan Refactoring

| Candidate | Expected future impact / relevance | Estimated effort and behavior risk | Prioritize now or defer? Why? |
|---|---|---|---|
| **C1 (`SVD.sgd()` Long Method)** | High. SVD is the primary algorithm in Surprise. Decoupling initialization from training logic allows maintainers to adapt initialization or optimize parameters cleanly. | Low to Moderate effort. Low risk when extraction is performed at the initialization boundary and verified with the exact RMSE test. | **Prioritize now.** Clear maintainability gain with a rigorous behavioral regression safety net (`test_sanity_checks`). |
| **C2 (`compute_baselines` Feature Envy)** | Moderate. Affects data encapsulation between algorithms and the dataset model. | High effort and high risk. Modifying `Trainset` contracts impacts all 11 algorithms in the library. | **Defer.** High systemic regression risk across algorithms; not suitable for a focused, safe improvement. |

**Selected documented issue(s) and individual ownership:**

| Contributor / GitHub handle | Candidate ID | Planned refactoring | Expected benefit | GitHub regression check planned |
|---|---|---|---|---|
| **Basam (`201400160-wq`)** | **C1** | Extract Method: extract factor and bias initialization into `_init_factors_and_biases(self, trainset)` on `SVD`. | Deconstructs monolithic 93-line method; isolates RNG and memory allocation from training loops with zero runtime overhead. | `.github/workflows/lab6-verification.yml` executing `pytest -v tests/test_SVD.py tests/test_algorithms.py -k "test_SVD_parameters or test_sanity_checks"`. |
| **Independent Partner** | [Independent partner contribution] | [Independent partner refactoring — to be documented independently on partner's branch] | [To be documented on partner's branch] | Handled on partner's branch |

---

## Task 4 - Refactor, Verify, and Commit

**Baseline test/check run(s) on GitHub:** [Lab6 Baseline Run](https://github.com/Wali007-lab/Surprise/actions)
**After-refactoring SHA(s):** [`bd790bb3bf7bf1108c9692dd3eb8fdb506f19162`](https://github.com/Wali007-lab/Surprise/commit/bd790bb3bf7bf1108c9692dd3eb8fdb506f19162)
**After-refactoring scan / workflow run(s):**
- Python Ruff: [Run 44544220815](https://github.com/Wali007-lab/Surprise/actions/runs/44544220815) (Status: Success, uploaded `lab6-ruff-report`; workflow success confirms execution, not absence of scanner findings).
- Duplication (jscpd): [Run 44544220480](https://github.com/Wali007-lab/Surprise/actions/runs/44544220480) (Status: Success, uploaded `lab6-duplication-report`; workflow success confirms report generation, not zero duplication).
**After-refactoring test/check run(s):**
- Regression Verification: [Run 44544220711](https://github.com/Wali007-lab/Surprise/actions/runs/44544220711) (Status: Success, 15 passed, 4 deselected).

| Issue / contributor | Before (same scope and measurement) | After | Test / verification result | What does this actually establish? |
|---|---|---|---|---|
| **C1 / Basam (`201400160-wq`)** | `SVD.sgd()` spanned 93 lines (lines 159–251) containing mixed initialization, C-scalar unpacking, and training loops. | Initialization extracted into dedicated `_init_factors_and_biases()` (23 lines); `sgd()` invokes helper cleanly via tuple unpacking. | **Verified in CI ([Run 44544220711](https://github.com/Wali007-lab/Surprise/actions/runs/44544220711)):** `tests/test_algorithms.py::test_sanity_checks[SVD]` PASSED (`RMSE == 1.0077323320656948`); `tests/test_SVD.py::test_SVD_parameters` PASSED. | Confirms exact floating-point equality to the golden benchmark for the chosen execution path. This provides empirical regression evidence, but is not mathematical proof of complete behavioral equivalence across all arbitrary inputs. |
| **Partner Contribution** | [Independent contribution] | [Independent refactoring] | [To be documented independently on partner's branch] | [To be documented independently on partner's branch] |

**Answers to the original GQM questions:**

- **Q1:** Static analysis and manual source inspection revealed that while high-level Python code has low duplication (0.4%), core optimization routines in Cython (notably `SVD.sgd()`) suffer from the Long Method smell by mixing array allocation, memoryview binding, and gradient iteration in monolithic blocks.
- **Q2:** The initialization responsibility within `SVD.sgd()` was refactored through Extract Method (`_init_factors_and_biases`). By performing extraction at the initialization boundary, we respected Cython's performance requirements (avoiding Python dispatch overhead in inner loops) and verified empirical behavioral preservation through GitHub Actions CI ([Run 44544220711](https://github.com/Wali007-lab/Surprise/actions/runs/44544220711)), where all 15 tests passed and the golden regression assertion held (`RMSE == 1.0077323320656948`).

**Conclusion and limits:**
Extracting `_init_factors_and_biases` modularized the SVD training process, clarifying where latent factors are instantiated without touching the inner loop. Passing the regression suite demonstrates that parameter handling and numerical results on benchmark sets remain intact, though passing a chosen test suite provides evidence rather than exhaustive proof of complete behavioral invariance. Static linters designed strictly for Python have blind spots for Cython syntax, emphasizing that code quality in hybrid Python/C codebases requires combining manual inspection with rigorous numerical regression testing.

---

### Individual implementation commits - permanent GitHub links

| Contributor / GitHub account | Documented issue (C1, C2, ...) | What was refactored? | **Permanent commit link** | PR or GitHub Actions push-run link |
|---|---|---|---|---|
| **Basam (`201400160-wq`)** | **C1** | Extracted `_init_factors_and_biases` from `SVD.sgd()` in `matrix_factorization.pyx` | [`bd790bb3bf7bf1108c9692dd3eb8fdb506f19162`](https://github.com/Wali007-lab/Surprise/commit/bd790bb3bf7bf1108c9692dd3eb8fdb506f19162) | [CI Verification Run 44544220711](https://github.com/Wali007-lab/Surprise/actions/runs/44544220711) |
| **Independent Partner** | [Partner Issue] | [Independent refactoring] | [To be documented on partner's branch] | [To be documented on partner's branch] |

**Completed template location on `semester-investigation`:** `https://github.com/Wali007-lab/Surprise/blob/lab6-Basam/LAB6_ANALYSIS.md`
**Template/report commit link:** [`bd790bb3bf7bf1108c9692dd3eb8fdb506f19162`](https://github.com/Wali007-lab/Surprise/commit/bd790bb3bf7bf1108c9692dd3eb8fdb506f19162)

**Evidence preservation note:**
SonarQube Cloud project measurements: NCLOC 3,924; Cognitive Complexity 349; Duplication Density 0.4%; Maintainability Rating A (1.0); Golden Regression RMSE: `1.0077323320656948`.