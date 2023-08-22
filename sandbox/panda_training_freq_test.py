#!/usr/bin/env python3
"""Small script that can be used to profile the training frequency.

You can get the training frequency by checking the frequency of the
`/panda_arm_joint1_effort_controller/command` topic. This is done using the
`rostopic hz /panda_arm_joint1_effort_controller/command` command.
"""
from pathlib import Path

import gymnasium as gym
import numpy
import rospy
import torch

# Script parameters.
# CONTROL_TYPE = "trajectory"
# CONTROL_TYPE = "end_effector"
# CONTROL_TYPE = "position"
CONTROL_TYPE = "effort"
TASK_ENV = "ros_gazebo_Gym:PandaReach-v1"
# TASK_ENV = "os_gazebo_Gym:PandaPickAndPlace-v1"
# TASK_ENV = "os_gazebo_Gym:PandaPush-v1"
# TASK_ENV = "os_gazebo_Gym:PandaSlide-v1"
N_STEPS = 1000
N_EPISODES = 5

if __name__ == "__main__":
    # rospy.init_node("panda_train_freq_test", anonymous=True, log_level=rospy.WARN)

    # Create ros_gazebo_gym environments.
    env = gym.make(TASK_ENV, control_type=CONTROL_TYPE)

    # Create the Gym environment.
    rospy.loginfo("Gym environment done")
    rospy.loginfo("Starting Learning")

    # Set the logging system.
    outdir = Path(__file__).parent.joinpath("data/training_results")
    last_time_steps = numpy.ndarray(0)

    # Set max_episode_steps.
    env._max_episode_steps = N_STEPS

    # Convert goal gym env to normal gym env.
    env = gym.wrappers.FlattenObservation(env)

    # Perform simulated training loop.
    # NOTE: Here we use random actions and do not train a network.
    torch.cuda.empty_cache()
    rospy.logwarn("Starting training loop")
    obs = env.reset()
    for x in range(N_EPISODES):
        done = False
        for i in range(N_STEPS):
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            if done:
                obs = env.reset()

    env.close()
