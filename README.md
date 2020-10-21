
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![LinkedIn][linkedin-shield]][linkedin-url]

<p>
  <h1 align="center">Sliding Puzzle Solver</h1>
  <p align="center">
  <h3 align = "center"> Solves a random sliding puzzle using A* </h3>
</p>

<p align="center">

<img wdith = "400" height = "400" src="https://github.com/vincentwang60/sliding-puzzle-solver/blob/master/images/1.gif">

</p>

## Description
The solver creates random 3x3 puzzles until it finds one that is solvable. [geeksforgeeks.org/check-instance-15-puzzle-solvable](https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/)
The solver then uses the [A* Search Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) on a graph with nodes consisting of different board states. The heuristic used is [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry).
When the solution is found, the solver saves the path taken, and moves the pieces accordingly.
UI is implemented using [PyGame](https://www.pygame.org/docs/)


## Future Development
- Enhance UI with progress bar to reasonably estimate time to solve.
- Make algorithm distributable to solve bigger puzzles in reasonable time.
- Port to web platform and utilize cloud computing for algorithm computations.

## References
- https://towardsdatascience.com/sliding-puzzle-solving-search-problem-with-iterative-deepening-a-d7e8c14eba04




[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=flat-square
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/vkwang
