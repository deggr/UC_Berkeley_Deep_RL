#!/usr/bin/env bash

source /home/dg/envs/rl/bin/activate

export PYTHONPATH=/home/dg/Projects/training/UC_Berkeley_Deep_RL/hw2

python run_hw2_policy_gradient.py --env_name CartPole-v0 -n 50 -b 1000 -dsa --exp_name sb_no_rtg_dsa
python run_hw2_policy_gradient.py --env_name CartPole-v0 -n 50 -b 1000 -rtg -dsa --exp_name sb_rtg_dsa 
python run_hw2_policy_gradient.py --env_name CartPole-v0 -n 50 -b 1000 -rtg --exp_name sb_rtg_na 
python run_hw2_policy_gradient.py --env_name CartPole-v0 -n 50 -b 5000 -dsa --exp_name lb_no_rtg_dsa 
python run_hw2_policy_gradient.py --env_name CartPole-v0 -n 50 -b 5000 -rtg -dsa --exp_name lb_rtg_dsa 
python run_hw2_policy_gradient.py --env_name CartPole-v0 -n 50 -b 5000 -rtg --exp_name lb_rtg_na 

