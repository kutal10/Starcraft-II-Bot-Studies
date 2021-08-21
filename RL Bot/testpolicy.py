import gym
from gym.wrappers import Monitor
from time import time 

from sc2env.envs import DZBEnv
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO
from absl import flags

FLAGS = flags.FLAGS
FLAGS([''])

env = gym.make('defeat-zerglings-banelings-v0')
""" env = Monitor(env,'./videos/' + str(time()) + '/', video_callable=lambda episode_id: True,force=True)
 """

#load pretrained model
model = PPO.load("model/dbz_ppo", env=env)

obs = env.reset()
frames = []

while True:
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
