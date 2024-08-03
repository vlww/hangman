# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import Helpers.mdp, Helpers.util

from Helpers.learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = Helpers.util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for k in range(1, self.iterations + 1):
            new_v_values = []
            for state in self.mdp.getStates():
                possibleActions = self.mdp.getPossibleActions(state)
                if possibleActions:
                    q_values = [self.computeQValueFromValues(state, action) for action in possibleActions]
                    new_v_value = max(q_values)
                    new_v_values += [(state, new_v_value)]
            #After updating all state values for V_(k+1)
            for stateValuePair in new_v_values:
                state = stateValuePair[0]
                new_v_value = stateValuePair[1]
                self.values[state] = new_v_value

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        transitionFunc = dict(self.mdp.getTransitionStatesAndProbs(state, action))
        nextStates = self.getNextStates(state, action)
        #print transitionFunc
        return sum([transitionFunc[nextState]*(self.mdp.getReward(state, action, nextState) \
            + self.discount*self.values[nextState]) for nextState in nextStates])

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        QValueActionList = [[self.computeQValueFromValues(state, action), action] \
            for action in self.mdp.getPossibleActions(state)]
        maxQValueActionPair = max(QValueActionList)
        return maxQValueActionPair[1]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

    #Added helper function
    def getNextStates(self, state, action):
        "Returns list of next states from current state"
        return [nextStateActionPair[0] for nextStateActionPair in self.mdp.getTransitionStatesAndProbs(state, action)]
    
class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        iterCounter = 0

        while iterCounter < self.iterations:
            for state in self.mdp.getStates():
                Q_s = Helpers.util.Counter() # the Q values for given the specified state
            
                for action in self.mdp.getPossibleActions(state):
                    Q_s[action] = self.computeQValueFromValues(state, action)
            
                self.values[state] = Q_s[Q_s.argMax()]
                
                iterCounter += 1
                if iterCounter >= self.iterations:
                    return

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        mdp = self.mdp
        values = self.values
        discount = self.discount
        iterations = self.iterations
        theta = self.theta
        states = mdp.getStates()


        predecessors = {} # dict
        for state in states:
            predecessors[state] = set()

        pq = Helpers.util.PriorityQueue()

        # computes predecessors and puts initial stuff into pq
        for state in states:
            Q_s = Helpers.util.Counter()

            for action in mdp.getPossibleActions(state):
                # assigning predecessors
                T = mdp.getTransitionStatesAndProbs(state, action)
                for (nextState, prob) in T:
                    if prob != 0:
                        predecessors[nextState].add(state)

                # computing Q values for determining diff's for the pq
                Q_s[action] = self.computeQValueFromValues(state, action)

            if not mdp.isTerminal(state): # means: if non terminal state
                maxQ_s = Q_s[Q_s.argMax()]
                diff = abs(values[state] - maxQ_s)
                pq.update(state, -diff)


        # now for the actual iterations
        for i in range(iterations):
            if pq.isEmpty():
                return

            state = pq.pop()

            if not mdp.isTerminal(state):
                Q_s = Helpers.util.Counter()
                for action in mdp.getPossibleActions(state):
                    Q_s[action] = self.computeQValueFromValues(state, action)

                values[state] = Q_s[Q_s.argMax()]

            for p in predecessors[state]:
                Q_p = Helpers.util.Counter()
                for action in mdp.getPossibleActions(p):
                # computing Q values for determining diff's for the pq
                    Q_p[action] = self.computeQValueFromValues(p, action)

                #if not mdp.isTerminal(state): # means: if non terminal state
                maxQ_p = Q_p[Q_p.argMax()]
                diff = abs(values[p] - maxQ_p)
                
                if diff > theta:
                    pq.update(p, -diff)
