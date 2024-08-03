# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from Helpers.game import *
from Helpers.learningAgents import ReinforcementAgent
from Helpers.featureExtractors import *

import random, Helpers.util, math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - getQValue
        - computeValueFromQValues
        - computeActionFromQValues
        - getAction
        - update

      Instance variables you have access to:
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
        - self.qVals (the Q-Table)

      Functions you will use:
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)
        self.eval = False
        self.qVals = {}
        

    def getQValue(self, state, action):
        action = action.capitalize()
        """
          Returns the Q-value of the (state,action) pair.
          Should return 0 if we have never seen the state,
          and initialize that state in the Q-Table.
        """
        "*** YOUR CODE HERE ***"
        if state in self.qVals:
          return self.qVals[state][action]
        else:
          self.qVals[state] = { 'North': 0, 'South': 0, 'East': 0, 'West': 0, 'Stop': 0, 'Exit': 0 }
          return 0

      
    def computeValueFromQValues(self, state): 
        if len(self.getLegalActions(state)) == 0:
          return 0
        else:
          return self.getQValue(state, self.computeActionFromQValues(state))

        """
          Returns the Q-value of the best action to take in this state.  
          Note that if there are no legal actions, which is the case at 
          the terminal state, you should return a value of 0.
        """
        "*** YOUR CODE HERE ***"


    def computeActionFromQValues(self, state):
        """
          Returns the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legal_moves = self.getLegalActions(state)
        if len(legal_moves) == 0:
          return None
        lista = []
        maxi = float("-inf")
        for m in legal_moves:
            if self.getQValue(state, m) >= maxi:
              maxi = self.getQValue(state, m)
        
        for m in legal_moves:
          if self.getQValue(state, m) == maxi:
            lista.append(m)
        return random.choice(lista)


    def getAction(self, state):
        """
          Select the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          Use random.random() to generate a random number between 0-1
          Use random.choice(list) to pick a random item from a list
        """
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if random.random() > self.epsilon:
          return self.computeActionFromQValues(state)
        else:
          return random.choice(legalActions)


    def update(self, state, action, nextState, reward):
        action = action.capitalize()
        """
          You should do your Q-Value updates here.

          NOTE: You should never call this function,
          it will be called for you.
        """
        "*** YOUR CODE HERE ***"
        qstat = self.getQValue(state, action)
        self.qVals[state][action] = qstat + self.alpha*(reward+(self.discount*self.computeValueFromQValues(nextState)) - qstat)
    

    #************Do Not Touch Anyting Below***************

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


