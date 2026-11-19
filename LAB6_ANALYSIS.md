\## Lab #6 - Investigation Record



\*\*Team / student(s):\*\* Waleed Younis (Wali007-lab)



\*\*Mode:\*\* Individual



\*\*Approved upstream project:\*\* https://github.com/NicolasHug/Surprise



\*\*Fork / working branch:\*\* https://github.com/Wali007-lab/Surprise/tree/semester-investigation



\*\*Original Lab #5 version:\*\* N/A



\*\*Lab #6 pre-refactoring baseline:\*\* 93e1c30



\---



\### Task 1 - Stakeholder, GQM, and Code Smell Selection



\*\*Selected stakeholder and exact fictional concern from handout:\*\*



Alex (Software Maintainer) wants to improve maintainability and reduce future maintenance effort.



\*\*GQM goal:\*\*



Analyze Surprise for the purpose of identifying maintainability improvements, with respect to code quality and maintainability, from the viewpoint of a software maintainer, in the context of the Surprise GitHub repository.



| Initial Question | Question wording | Relevant metric(s) / observation(s) | Why useful? |

|-----------|-----------|-----------|-----------|

| Q1 | Which components exhibit maintainability issues? | Complexity, method size, smell occurrence | Identifies problematic components |

| Q2 | Which issues can be improved through refactoring? | Before/after code inspection | Supports maintainability improvement decisions |



\*\*Code-smell types chosen from the lecture:\*\*



| Smell type | Lecture slide(s) | Why relevant to our GQM? | Investigation method |

|------------|------------|------------|------------|

| Long Method | Slide 34 | Large methods reduce maintainability | Manual inspection + SonarQube |

| Large Class | Slide 38 | Classes with many responsibilities are harder to maintain | Manual inspection |

| Feature Envy | Slide 89 | May indicate misplaced functionality | Manual inspection |



\*\*Primary GitHub-integrated tool:\*\* SonarQube Cloud



\*\*Complementary tool:\*\* Manual inspection



\*\*Why these tools match our questions and selected smells:\*\*



SonarQube provides repository-level quality analysis, while manual inspection is required because many maintainability smells are not automatically detected.



\---



\### Task 2 - Detect and Investigate Code Smells



\*\*Analysis configuration:\*\*



\- Fork branch and baseline SHA: 93e1c30

\- Source directories analyzed: surprise/prediction\_algorithms

\- Exclusions: none

\- Tools: SonarQube Cloud

\- Baseline GitHub scan / Actions run links: SonarQube Cloud project dashboard



| Selected smell type | Found / not found / not assessable | Tool result or source link | Interpretation / limitations |

|------------|------------|------------|------------|

| Long Method | Found | Manual inspection | Detected in SVD.sgd() |

| Large Class | Found | Manual inspection | matrix\_factorization.pyx contains several large algorithm implementations |

| Feature Envy | Not assessable | Manual inspection | No strong evidence identified |



\*\*Candidate issues inspected in source:\*\*



| Candidate ID | File/entity permalink | What was actually observed? | Why it might matter / why uncertain |

|------------|------------|------------|------------|

| C1 | surprise/prediction\_algorithms/matrix\_factorization.pyx | SVD.sgd() contains initialization, error calculation, updates and training logic in a single method | Reduces readability and maintainability |

| C2 | surprise/prediction\_algorithms/matrix\_factorization.pyx | SVDpp.sgd() is also a large method with multiple responsibilities | Similar maintainability concern but not selected for refactoring |



\*\*One warning we challenged, or one potentially missed issue:\*\*



SonarQube reported primarily security-related issues but did not automatically identify maintainability smells; therefore manual inspection was necessary.



\---



\### Task 3 - Prioritize Technical Debt and Plan Refactoring



| Candidate | Expected future impact / relevance | Estimated effort and behavior risk | Prioritize now or defer? Why? |

|------------|------------|------------|------------|

| C1 | High | Low effort, low risk | Prioritize now |

| C2 | Medium | Higher effort | Defer |



\*\*Selected documented issue(s) and individual ownership:\*\*



| Contributor / GitHub handle | Candidate ID | Planned refactoring | Expected benefit | GitHub regression check planned |

|------------|------------|------------|------------|------------|

| Wali007-lab | C1 | Extract Method | Improved readability and maintainability | Git commit inspection |



\---



\### Task 4 - Refactor, Verify, and Commit



\*\*Baseline test/check run(s) on GitHub:\*\* SonarQube analysis before refactoring



\*\*After-refactoring SHA(s):\*\* b2c2cb3



\*\*After-refactoring scan / workflow run(s):\*\* Not executed



\*\*After-refactoring test/check run(s):\*\* Local pytest execution attempted but project build/import dependencies prevented execution



| Issue / contributor | Before | After | Test / verification result | What does this actually establish? |

|------------|------------|------------|------------|------------|

| C1 / Wali007-lab | Error computation embedded directly in SVD.sgd() | Error computation extracted into \_compute\_error() | Manual verification | Responsibility reduced within SVD.sgd() |



\*\*Answers to the original GQM questions:\*\*



\- \*\*Q1:\*\* The file matrix\_factorization.pyx contains maintainability concerns, particularly large methods such as SVD.sgd() and SVDpp.sgd().

\- \*\*Q2:\*\* The identified Long Method smell in SVD.sgd() was improved through an Extract Method refactoring.



\*\*Conclusion and limits:\*\*



The refactoring improved readability and separation of concerns. The code structure became easier to understand. No claim can be made about runtime performance improvement because no performance testing was conducted. Automated regression testing could not be completed due to project build/import issues.



\---



\### Individual implementation commits - permanent GitHub links



| Contributor / GitHub account | Documented issue | What was refactored? | Permanent commit link | PR or GitHub Actions push-run link |

|------------|------------|------------|------------|------------|

| Wali007-lab | C1 | Extracted error computation from SVD.sgd() into \_compute\_error() | https://github.com/Wali007-lab/Surprise/commit/b2c2cb3 | N/A |



\*\*Completed template location on semester-investigation:\*\* To be committed as LAB6\_ANALYSIS.md



\*\*Template/report commit link:\*\* To be created after committing the report file.



\*\*Evidence preservation note:\*\* Refactoring evidence is preserved in Git commit b2c2cb3 and branch lab6-waleed.

