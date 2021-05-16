# OAST
Project for the subject OAST - A program which solves DAP and DDAP problems.

## Note

Would be a fork of https://github.com/pantalejmon/oast2 but we rewrote it from scratch to correct factual errors, correct the naming of some elements to align with the subject's naming convention, provide better documentation and add important output data collection functionalities. As a result, only the program structure and used data structures are similar.

## Results

The program in this repo is written to follow the correct naming conventions and solves the DAP and DDAP problems as best we could make it to, however:
* We do not guarantee 100% correctness of the variable names in the source code and of the algorithm implementation
* The program doesn't always reach satisfying results. Especially, DAP is bigger than zero for big networks in which the best solutions can reach DAP of non-positive numbers.

## Usage
Install dependencies:
```
pip install -r requirements.txt
```
Run the program:
```
python main.py
```
Follow the instructions provided by the program. You can use the `[s]` option to skip manual input and use the default parameters which you can alter by changing the variables at the start of the `main.py` script.

## Contributing

As it is currently, a function (`calculate_fitness()`) gets called which takes the chromosome population, and the link and demand data. The function calculates the fitness for each chromosome and then updates those values in the chromosomes. Instead, to follow OOP paradigms the fitness calculations should be done by each chromosome when its genes are changed and upon initialization. To do that, a reference to the demand and link data sets should be stored in each chromosome.

Any other improvements which make the algorithm results better are welcome.

Optimal DAP solutions for reference:
* net4: -138
* net12_1: -29
* net12_2: 0

We do not have the optimal DDAP solutions, but we believe the ones in `final_results` to be quite close to optimal.
