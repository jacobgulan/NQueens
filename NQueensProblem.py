# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 15:05:23 2021

@author: JacobG
"""

import numpy as np
from collections import Counter

class Queens:

    def __init__(self, n, queens=None):
        self.n = n
        if queens is None:
            self.queens = self.generateQueens()
        else:
            self.queens = queens
         
    def generateQueens(self):
        # Generate queens in random locations
        queenLocs = []
        for i in range(self.n):
            queenLocs.append(np.random.randint(0, self.n))

        return queenLocs

    # Get all possible moves
    def getNeighbors(self):
        neighbors =  []
        queens = self.queens
        
        # Iterate through each queen's possible moves
        for y in range(self.n):
            for x in range(self.n):
                if x != queens[y]:
                    # Create new state
                    temp = queens.copy()
                    temp[y] = x
                    temp = Queens(self.n, temp)
                    neighbors.append(temp)

        return neighbors

    
    def calcHeuristic(self):
        h = 0

        # Initialize counters
        a, b, c = [Counter() for i in range(3)]

        # Count the matches
        for row, col in enumerate(self.queens):
            a[col] += 1
            b[row-col] += 1
            c[row+col] += 1

        # Count the conflicts for each queen and add to the heuristic
        for count in [a, b, c]:
            for key in count:
                h += count[key] * (count[key] - 1)/2

        return h

    # Made a 2D array to display the chess board
    def makeBoard(self):
        # Make empty chess board
        board = np.zeros((self.n,self.n), np.int8)

        # Assign queens to their correct location
        for i in range (self.n):
            for j in range (self.n):
                if j == self.queens[i]:
                    board[i][j] = 1

        return board


class HillClimber:
    def __init__(self, n):
        self.queens = Queens(n)
        self.initialBoard = self.queens
        self.steps = 0
        self.restarts = 0
        self.success = False

    def minRandomNeighbor(self, neighbors):
        # Find the neighbor with the smallest heuristic
        neighborsCost = []
        for n in neighbors:
            neighborsCost.append(n.calcHeuristic())
        minCost = min(neighborsCost)

        # Get all neighbors with same minimum cost
        minNeighbors = []
        for i in neighbors:
            if i.calcHeuristic() == minCost:
                minNeighbors.append(i)
        
        # Randomly select smallest neighbor
        return np.random.choice(minNeighbors)
        

    def hillClimbing(self, sideways = False):
        curr = self.queens
        currH = curr.calcHeuristic()
        sidemoves = 0

        # Begin hill climbing
        while True:
            neighbors = curr.getNeighbors()

            # Break if solution is found
            if currH == 0:
                self.success = True
                break

            # Find neighbor with minimum heuristic value to take next step
            neighbor = self.minRandomNeighbor(neighbors)
            newH = neighbor.calcHeuristic()

            # Check to see whether next step is better than previous
            if newH > currH:
                break
            elif newH == currH:
                # Sideways move if enabled
                if (sideways and (sidemoves < 100)):
                    sidemoves += 1
                else:
                    break
            else:
                sidemoves = 0
            
            # Take the next step
            curr = neighbor
            currH = newH
            self.steps += 1

        return curr.queens


    def randomRestart(self, sideways=False):
        curr = self.queens
        sidemoves = 0
        currH = 10
        newH = 10
        
        while True:
            while True:
                currH = curr.calcHeuristic()
                neighbors = curr.getNeighbors()
                
                # Break if solution is found
                if currH == 0:
                    self.success = True
                    break

                # Find neighbor with minimum heuristic value to take next step 
                neighbor = self.minRandomNeighbor(neighbors)
                newH = neighbor.calcHeuristic() 

                # Check to see whether next step is better than previous
                if newH > currH:
                    break
                elif newH == currH:
                    # Sideways move if enabled
                    if not sideways or sidemoves == 100:
                        break
                    else:
                        sidemoves += 1
                else:
                    sidemoves = 0

                # Take the next step
                curr = neighbor
                self.steps += 1
                newH = curr.calcHeuristic()

            # If solution not found then restart with new board
            if newH > 0:
                curr = Queens(curr.n)
                self.queens = curr
                self.restarts += 1
            else:
                return curr.queens

def main():
    n = int(input('Enter the number of queens:\n'));

    # Track information
    successSteps = []
    failedSteps = []
    boards = []

    # Hill Climbing Without Sideways
    for i in range(100):
        # Create hill climber
        climber = HillClimber(n)
        boards.append(climber.initialBoard)
        climber.hillClimbing(sideways=False)

        # Track the number of steps needed for failures and successes
        if climber.success:
            successSteps.append(climber.steps)
        else:
            failedSteps.append(climber.steps)

    # Randomly take four initial states
    np.random.shuffle(boards)
    boards = boards[:4]

    # Print Info
    print("\nHill Climbing Without Sideways")
    print("Successes: ", len(successSteps))
    print("Failures: ", len(failedSteps))
    print("Successes Average Steps: ", np.average(successSteps))
    print("Failures Average Steps: ", np.average(failedSteps))
    print("Four Random Initial Configurations: ")
    for b in boards:
        print(b.makeBoard(), "\n")

    # Reset Arrays
    successSteps = []
    failedSteps = []
    boards = []

    # Hill Climbing With Sideways
    for i in range(100):
        # Create hill climber
        climber = HillClimber(n)
        boards.append(climber.initialBoard)
        climber.hillClimbing(sideways=True)

        # Track the number of steps needed for failures and successes
        if climber.success:
            successSteps.append(climber.steps)
        else:
            failedSteps.append(climber.steps)

    # Randomly take four initial states
    np.random.shuffle(boards)
    boards = boards[:4]

    # Print Info
    print("\nHill Climbing With Sideways")
    print("Successes: ", len(successSteps))
    print("Failures: ", len(failedSteps))
    print("Successes Average Steps: ", np.average(successSteps))
    print("Failures Average Steps: ", np.average(failedSteps))
    print("Four Random Initial Configurations: ")
    for b in boards:
        print(b.makeBoard(), "\n")

    # Reset Array
    successSteps = []
    failedSteps = []
    restarts = []

    # Random Restart Hill Climbing Without Sideways
    for i in range(100):
        # Create hill climber
        climber = HillClimber(n)
        climber.randomRestart(sideways=False)

        # Track the number of steps needed for failures and successes
        if climber.success:
            successSteps.append(climber.steps)
            restarts.append(climber.restarts)

    # Print Info
    print("\nRandom Restart Without Sideways")
    print("Average Steps: ", np.average(successSteps))
    print("Average Restarts: ", np.average(restarts))

    # Reset Array
    successSteps = []
    restarts = []

    # Random Restart Hill Climbing With Sideways
    for i in range(100):
        # Create hill climber
        climber = HillClimber(n)
        climber.randomRestart(sideways=True)

        # Track the number of steps needed for failures and successes
        if climber.success:
            successSteps.append(climber.steps)
            restarts.append(climber.restarts)

    # Print Info
    print("\nRandom Restart Hill Climbing With Sideways")
    print("Average Steps: ", np.average(successSteps))
    print("Average Restarts: ", np.average(restarts))
        

main()