# LEC 13 / Drill 11: 30 local commits

The first 15 commits implement IDLE, SLEEP and RUN. The next 15 add AutoRun, tests and the diagram image.

The Git log contains the exact hashes for all 30 commits.

1. `b77a3b4` build: declare pico2d and transitions dependencies
2. `f1052f4` feat: add reusable Grass game object
3. `65853fe` feat: add Boy object with repeating idle animation
4. `6ddcf51` feat: assemble grass and boy in the game loop
5. `9e59a34` feat: model IDLE with transitions Machine
6. `702c2bf` feat: track IDLE duration with a monotonic timer
7. `dbc9c45` feat: enter SLEEP after five idle seconds and draw a sleeping pose
8. `a52dcac` feat: route keyboard events and wake SLEEP with Space
9. `294e074` fix: animate at ten frames per second using elapsed time
10. `6bd8453` feat: add one RUN state with arrow input and directional running sprites
11. `4d0b2b0` fix: keep the running sprite inside the screen bounds
12. `53138b8` fix: keep running while either direction key remains held
13. `5aee6f2` fix: ignore key repeat when choosing the latest direction
14. `031f7cc` feat: allow arrow input to transition directly from SLEEP to RUN
15. `d2ca5d6` docs: describe IDLE SLEEP RUN behavior and the target state diagram
16. feat: introduce a dedicated AutoRun state class
17. feat: track AutoRun entry time and reset state lifecycle data
18. feat: activate the AUTO_RUN state with A from IDLE
19. feat: move automatically at twice normal running speed
20. feat: draw AutoRun at 150 pixels while keeping its feet grounded
21. fix: fit the enlarged sprite inside the screen on state entry
22. feat: reverse AutoRun at the right screen edge
23. feat: reverse AutoRun at the left screen edge
24. fix: preserve travel distance through slow-frame and multiple edge bounces
25. feat: return AutoRun to IDLE after five seconds
26. feat: cancel AutoRun into normal RUN with either direction key
27. fix: ignore held-A repeat events when starting AutoRun
28. docs: explain Drill 11 controls speed size and execution
29. test: cover AutoRun timers movement rendering input and state regressions
30. docs: include the AutoRun state diagram and PRD
