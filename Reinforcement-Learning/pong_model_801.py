# UNC Charlotte
# ITCS 5153 - Applied AI - Spring 2025
# Lab 5
# Reinforcement Learning
# This module implements the game Pong
# Student ID: 801


from stable_baselines3.common.env_util import make_atari_env
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3 import A2C

import ale_py

# There already exists an environment generator
# that will make and wrap atari environments correctly.
# Here we are also multi-worker training (n_envs=12 => 12 environments)
vec_env = make_atari_env("PongNoFrameskip-v4", n_envs=12, seed=0)
# Frame-stacking with 4 frames
vec_env = VecFrameStack(vec_env, n_stack=4)

model = A2C("CnnPolicy", vec_env, verbose=1)
model.learn(total_timesteps=2_500_000)

# Save the model
model.save("pong_model_801")

obs = vec_env.reset()
while True:
    action, _states = model.predict(obs, deterministic=False)
    obs, rewards, dones, info = vec_env.step(action)
    vec_env.render("human")
