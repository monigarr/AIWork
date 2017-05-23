# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: My class notes: 
Grid of 81 squares.
Rows 1 to 9
Columns A to I
Unit is a Collection of 9 Squares

If a square has only one solution (digit) available, remove that solution from all peers of the square.
If unit has only one place for a value, put the value in that place.
This is a good solution for simple puzzles.
If two different squares can have the same value :
	Banch out & consider options by creating tree with possible answers.
		One branch might provide 3 or more options. 
			Branch out and consider those options.
				Traverse the tree to find A solution.
I also added my notes as a comment in my code: solution.py



# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Same as constraint propogation above plus we iterate for the center diagonal peer squares.
I defined unitlist in solution.py to consider all of a square's peers (next to, above, below and diagnal)

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  
You will be prompted for a username and password.  If you login using google or facebook, visit 
[this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip. 
 This is the file that you should submit to the Udacity reviews system.

