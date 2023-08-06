# gym-simple-cliffworld

A simplified version of Cliffworld in an OpenAI Gym Environment.

This is a project by [Winder Research](https://WinderResearch.com), a Cloud-Native Data Science consultancy.

## Installation

`pip install gym-simple-cliffworld`

## Usage

```python
import gym
import gym_simple_cliffworld

env = gym.make("SimpleCliffworld-v0")
episode_over = False
rewards = 0
while not episode_over:
    state, reward, episode_over, _ = env.step(env.action_space.sample())
    print(state, reward)
    rewards += reward
print("Total reward: {}".format(rewards))
```

## Credits

Gitlab icon made by [Payungkead](https://www.flaticon.com/authors/payungkead) from [www.flaticon.com](https://www.flaticon.com/).