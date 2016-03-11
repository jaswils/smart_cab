import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.potential_actions = ('left',  'forward',  'right', None)
        
        self.q = dict()
        self.alpha = 0.5
        self.gamma = 0.7
        
        self.trial = 0
        self.total_reward = 0
        self.deadline=0
        

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        
        self.total_reward = 0
        self.trial += 1
        

        #Compute max Q(s',a')
    def qmax(self, s):
        v= list()

        for k in self.potential_actions:
            v.append(self.q.get((s, k), 0))

        return max(v) 

        #Compute the action based on the argmax_a' (Q(s',a'))
    def qargmax(self, s):
        v= list()

        for k in self.potential_actions:
            v.append(self.q.get((s, k), 0))

        return self.potential_actions[v.index(max(v))]    

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        self.deadline = self.env.get_deadline(self)

        # TODO: Update state
        # Inputs to choose from for state include {'light': 'red', 'oncoming': None, 'right': None, 'left': None}
        self.state_ = (self.next_waypoint, inputs['light'])
        
        # TODO: Select action according to your policy
        epsilon = 1.0 / (self.trial/2 + 1.0)
        #epsilon = 0.0
        if (random.random() < epsilon):
            action = random.choice(self.potential_actions)
            print 'Random Action'
        else:
            action = self.qargmax(self.state_)
            print 'Learned Action'

        # Execute action and get reward
        reward = self.env.act(self, action)
        self.total_reward += reward
        print 'Deadline: ', self.deadline, ' Action: ', action, ' Reward: ', reward , 'State', self.state_       

        # TODO: Learn policy based on state, action, reward
        
        #Sense s' state 
        self.next_waypoint = self.planner.next_waypoint()
        inputs = self.env.sense(self)
        self.state=(self.next_waypoint, inputs['light'])
        
        #Update Q value
        self.q[(self.state_, action)] = self.q.get((self.state_, action),0) * (1-self.alpha) + self.alpha * (reward + self.gamma * self.qmax(self.state))
        

        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]





def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=.001)  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()

