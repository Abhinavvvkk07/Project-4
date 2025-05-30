# -*- coding: utf-8 -*-
"""RL_Project4_template.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15dQFm-u5nKq4Kr7xUVb4Ec4UzNwALE57

<a href="https://colab.research.google.com/github/DS-Aditya-928/CartPoleProject4/blob/main/RL_Project4_template.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
"""

'''

Imports! The first 3 are for our cartpole simulation, numpy is for our bot, tqdm is a super easy way to
draw progress bars, and the last one is used to play the video of the simulation.

'''
import gymnasium as gym
from gym import logger as gymlogger
from gym.wrappers import RecordVideo, RecordEpisodeStatistics

import numpy as np
from tqdm import tqdm

import moviepy.editor

"""#📌 Before we go any further:

Let's have a look over what we're trying to accomplish.

<br>

Reinforcement learning is a machine learning algorithm where we let the algorithm make its own descisions in an attempt to maximize a "reward". This reward can be a high score in a game, or more relevant to our project here, the time our algorithm is able to balance a pole mounted on a cart for.


To train our algorithm, we're going to be using something called Q learning.

<br>


---

#📌 What is Q-learning?

This bit is pretty complex, and this video explains Q learning better than I ever could :p

https://www.youtube.com/watch?v=TiAXhVAZQl8  
  
<br>

The basic idea however, is that we are going to maintain a table (appropriately called a Q table) that holds expected changes in score for all of our possible actions at a give state.

<br>

I.E, for the cart pole example, let's say the pole is 5 degrees off centre, and has a velocity of 1 m/s. Our algorithm is going to go to the corresponding cell in our table, and see which one of the possible actions (in the cartpole example, those are moving left or right) will result in the greatest increase in score. So, the cell holds an array with expected score changes for each action.

Let's say the cell for the case described above has this array:  [-1.0, +2.5], with the first value corresponding to the expected change in score if we move to the left, and the other if we move to the right. Moving to the right gives us a score change of +2.5, so we're going to move to the right.


<br>

The training bit here involves having the model change these values in the q table so that it makes better and better decisions over time. We'll delve more into the specifics of how to accomplish this later.

<br>
Got all that? It's ok if you didn't. I'm still wrapping my head around it myself. Feel free to ask us questions during office hours and USE THE INTERNET. It can teach you anything if you use it right.

---


This here is the CartPoleBot class; all the functions you'll need to implement are in here.
"""

from collections import defaultdict
class CartPoleBot:

  env:gym.Env
  learningRate:float
  discountFactor:float

  def __init__(self, env: gym.Env, learningRate: float,
               initalEpsilon: float, epsilonDecay: float, finalEpsilon: float,
               discountFactor: float):
    '''
    Constructor. Don't change anything here. READ ALL THE COMMENTS THOUGH, they're hella useful.
    '''
    self.env = env #Our cartpole environment.

    self.learningRate = learningRate #The rate at which we update values in our Q-table.

    self.epsilon = initalEpsilon
    self.epsilonDecay = epsilonDecay
    self.finalEpsilon = finalEpsilon

    '''
    Does the word epsilon scare you? Fortunately, it's a fairly simple concept.

    At first, the values in the Q-table are going to be very wrong, so it makes sense to
    have the algorithm make random decisions instead, then take note of what happens and use that
    information to update our Q-table. We'll get into how we update the Q-table later.

    Whether or not our algorithm makes a random decision or looks up the Q-table value depends on epsilon.
    Specifically, we are going to generate a random number between 0 and 1 and check if epsilon is higher than
    it. If it is, we pick a random action. If epsilon is lower than the random value, we look up the Q-table value.

    So, our initial epsilon is going to be a fairly high value (epsilon is between 0 and 1)
    which means that we're going to make more random decisions at the start, but we're going to lower it over time
    as our algorithm learns, preferring the values from the (hopefully now correct) Q-table.

    Initial epsilon and final epsilon are both self explanatory, and epsilonDecay is the rate at which
    epsilon decreases.
    '''

    self.qTable = defaultdict(lambda: np.zeros(self.env.action_space.n))

    '''
    the line above creates our Q table!
    #The idea is this: when we look up the specific state we are at in the dictionary
    #above, we'll have an array that has expected score changes for each action. (That's why each array
    # is env.action_space.n long. the action_space holds all possible actions, and .n returns its length.)
    #So if going left is action 0, then the value at index 0 in the aforementioned array is
    #the expected score change from going left.
    '''

    self.discountFactor = discountFactor#we'll get into what this does later.

  def discConv(self, obs):
    '''
    When we look up values in the Q-Table (represented as a dictionary), the key
    will be the state of the simulation, which is a numpy array.

    This sounds straightforward enough, but there are a few challenges:

    1.) The simulation values take the form of a numpy array, which is non-hashable and thus
    can't be used as a key for our dictionary.

    2.) Because there are infinite number of numbers, it's highly unlikely that we will
    run into the exact same values more than once (if at all). So, we shall generalise a bit
    and break down each range of sim values into discrete chunks. I've chosen 10 chunks for
    each here, but feel free to experiment.

    This function takes a numpy array representing the simulation state and returns a
    hashable tuple, with the values "rounded" to the closest chunk, keeping us from having multiple
    Q-Table entries for values that are very close but not exactly the same.
    '''
    #DO NOT CHANGE.
    posSpace = np.linspace(-2.4, 2.4, 10)
    velSpace = np.linspace(-4, 4, 10)
    angSpace = np.linspace(-.2095, .2095, 10)
    angVSpace = np.linspace(-4, 4, 10)
    lTodArray = [posSpace, velSpace, angSpace, angVSpace]
    tR = []
    for i in range(len(obs)):
      tR += [np.digitize(obs[i], lTodArray[i])]

    return(tuple(tR))

  def getAction(self, observation):
    #TO DO
    '''
    Your job here is to generate a random number, check if it's higher than epsilon and
    then, based on that, choose a random action or look up the Q-table's reccomended action.

    Use numpys random function to generate a random number.
    Here's the gymnasium library documentation: https://gymnasium.farama.org/. It should tell you how to
    get a random action.
    '''

    #Your code here.
    if np.random.rand() < self.epsilon:
      return self.env.action_space.sample()  # random action
    else:
      state = self.discConv(observation)
      return np.argmax(self.qTable[state])  # best known action



  def update(self, pastObv, action, reward, terminated, currObv):
    '''
    This is where we put everything we learned about Q-learning into practice.

    Just so we're clear, when this function is called, we've already taken an action based on what getAction
    returned, and we're now adjusting our q values based on how good/bad said action was.

    First, let's go over inputs:
    pastObv: State of the simulation(i.e angle of the pole, velocity etc.) BEFORE we took an action.
    action: The action we TOOK (generated by getAction).
    reward: the reward given to us by the environment.
    terminated: Whether the simulation ended or not because we failed (truncated is when the simulation ends
                because we balanced the pole for long enough).
    currObv: The state of the simulation AFTER the action from getAction was taken.

    In a broad sense, what we are trying to do here is calculate new values for a given
    cell in the Q-Table, and then make a small adjustment to the existing values accordingly.

    To do this, let's first calculate the temporal difference.

    temporalDiff = (reward for the current state) + (max(qTable[currObv])) - qTable[pastObv][action]

    The temporal difference is the difference between the q table value of the old position (before action),
    and the value based on the reward and the maximum increase in score that we can obtain by making a move from
    our new position (after the action) (NOTE: This value is 0 if the simulation ended!). Note that the
    maximum increase from this point isn't given equal weightage. Instead, we shall multiply it
    by the discontFactor before using it to calculate the temporalDiff. This is because we want our model to
    make decisions that are better in the short term as opposed to a possible reward gain another move later.

    The sum of the reward and max increase is what the q value should actually be,
    so we adjust qTable[pastObv][action] by the temporal diff * learning rate.

    Again, the video linked at the beginning is a must watch IMO, it'll make everything way easier to visualize.
    '''
    pastObv = self.discConv(pastObv)
    currObv = self.discConv(currObv)

    #Your code here:
    if terminated:
      future_q = 0
    else:
      future_q = np.max(self.qTable[currObv])

    current_q = self.qTable[pastObv][action]
    temporal_diff = reward + self.discountFactor * future_q - current_q
    self.qTable[pastObv][action] += self.learningRate * temporal_diff



  def decayEpsilon(self):
    #TO DO
    '''
    This is pretty easy; when this function is called, you're going to decrease
    epsilon by epsilonDecay. But remember, there is a minimum value that epsilon cannot drop below.
    '''

    #Your code here:
    self.epsilon = max(self.finalEpsilon, self.epsilon - self.epsilonDecay)

env = RecordVideo(gym.make("CartPole-v1", render_mode = "rgb_array"), "/content", episode_trigger= lambda x: (x%5000 == 0), new_step_api= True)#Generate a .mp4 video of our simulation every 5000 episodes.

#Hyperparameters
#these values aren't.... great, but they do get the job done eventually. I definitely recommend fiddling with these.
learningRate = 0.05
nEps = 60_000
startEpsilon = 1.0
epsilonDecay = (1.0/30_000.0)
finalEpsilon = 0.1
discountFactor = 0.95

#Initialize the bot.
balanceAgent = CartPoleBot(env, learningRate, startEpsilon, epsilonDecay, finalEpsilon, discountFactor)

for i in tqdm(range(nEps)):
  observation, info = env.reset()#reset the environment at the start of every episode

  done = False
  while not done:#We're done once we either fail (terminated) or pass (truncated)
    action = balanceAgent.getAction(observation)
    newObv, reward, terminated, truncated, info = env.step(action)

    balanceAgent.update(observation, action, reward, terminated, newObv)

    done = terminated or truncated
    observation = newObv

  balanceAgent.decayEpsilon()#Epsilon is reduced every episode.

env.close()

#call this to play one of the generated mp4s. Replace N with the episode count. Or just download it idk im not ur dad
moviepy.editor.ipython_display("/content/rl-video-episode-5000.mp4")