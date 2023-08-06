# `gym-yagw` Yet Another Grid World

This repository contains an RL environment based on the Gridworld from Sutton & Barto (1998).
The environment can be used together with OpenAI gym.

<p align="center"> 
<img src="./resources/yagw.gif">
</p>

<p align="center"> 
<img src="./resources/episode_lengths.png">
</p>

<p align="center"> 
<img src="./resources/episode_returns.png">
</p>

Table of Contents
=================
  
   * [Useful Commands](#Useful-Commands)
   * [Requirements](#Requirements)
   * [Usage](#Usage)
   * [MDP Model](#MDP-Model)
   * [Author & Maintainer](#Author-&-Maintainer)
   * [Copyright and license](#copyright-and-license)

## Useful Commands

```bash
# local install from source
$ pip install -e gym-yagw
# force upgrade deps
$ pip install -e gym-yagw --upgrade

# git clone and install from source
git clone https://github.com/Limmen/gym-yagw
cd gym-yagw
pip3 install -e .
```

## Requirements
- Python 3.5+
- OpenAI Gym
- NumPy
- Pyglet (OpenGL 3D graphics)
- GPU for 3D graphics acceleration (optional)

## Usage
The environment can be accessed like any other OpenAI environment with `gym.make`. 
Once the environment has been created, the API functions
`step()`, `reset()`, `render()`, and `close()` can be used to train any RL algorithm of
your preference.
```python
import gym
> env = gym.make("gym_yagw:yagw-v1", width=5, height=5)
> env.action_space
: Discrete(4)
> env.observation_space
: Box(2,)
> env.metadata
: "{'render.modes': ['human', 'rgb_array'], 'video.frames_per_second': 50}
> obs = env.reset()
> obs
: array([0, 0])
> s_prime, reward, done, info = env.step(1) # Move right
s_prime
: array([1, 0])
> reward
:-1
> done
:False
```

The environment ships with an implementation of the tabular Q(0) algorithm, see the example code below.

```python
import gym
from gym_yagw.algorithms.q_learning import QAgent

env = gym.make("gym_yagw:yagw-v1", width=5, height=5)
q_agent = QAgent(env, gamma=0.99, alpha=0.2, epsilon=1, render=False, eval_sleep=0.3,
                     min_epsilon=0.1, eval_epochs=2, log_frequency=100, epsilon_decay=0.999, video=False,
                     video_fps = 5, video_dir="./videos")
episode_rewards, episode_steps, epsilon_values = q_agent.run(5000)
q_agent.print_state_values(height=env.height, width=env.width)
q_agent.eval()
```

## MDP Model
$width \in R, height \in mathbb{R}$
$S = \{(x,y) | x \in [0, width), \land y \in [0, height)\}$
$\mathcal{A} = \{0,1,2,3\}$
$\mathcal{A}_{\text{labels}} = \{\text{Left}, \text{Right}, \text{Up}, \text{Down}\}$
$\mathcal{R}_{ss^{\prime}}^{a} = +1 \text{ if } s^{\prime} = \text{ goal state else} -1$
$\mathcal{P}_{ss^{\prime}}^a$ is deterministic, illegal operations (e.g moving into a wall) are 
treated as no-ops and yield a negative reward.

## Manual game

You can run the environment in a mode of "manual control" as well:

```python
from gym_yagw.envs.rendering.viewer import Viewer
viewer = Viewer(width=300, height=400, rect_size=50, manual=True)
viewer.manual_start()
``` 

## Future Work

- Debug UI to inspect policy/state-values
- Unit tests

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

MIT

(C) 2020, Kim Hammar