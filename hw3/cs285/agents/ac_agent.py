import numpy as np 
import tensorflow as tf 

from collections import OrderedDict

from .base_agent import BaseAgent
from cs285.policies.MLP_policy import MLPPolicyAC
from cs285.critics.bootstrapped_continuous_critic import BootstrappedContinuousCritic
from cs285.infrastructure.replay_buffer import ReplayBuffer
from cs285.infrastructure.utils import *

class ACAgent(BaseAgent):

    def __init__(self, sess, env, agent_params):
        super(ACAgent, self).__init__()

        self.env = env 
        self.sess = sess
        self.agent_params = agent_params

        self.gamma = self.agent_params['gamma']
        self.standardize_advantages = self.agent_params['standardize_advantages']

        self.actor = MLPPolicyAC(sess, 
                               self.agent_params['ac_dim'],
                               self.agent_params['ob_dim'],
                               self.agent_params['n_layers'],
                               self.agent_params['size'],
                               discrete=self.agent_params['discrete'],
                               learning_rate=self.agent_params['learning_rate'],
                               )
        self.critic = BootstrappedContinuousCritic(sess, self.agent_params)

        self.replay_buffer = ReplayBuffer()

    def estimate_advantage(self, ob_no, next_ob_no, re_n, terminal_n):
        
        # TODO Implement the following pseudocode:
            # 1) query the critic with ob_no, to get V(s)
            # 2) query the critic with next_ob_no, to get V(s')
            # 3) estimate the Q value as Q(s, a) = r(s, a) + gamma*V(s')
            # HINT: Remember to cut off the V(s') term (ie set it to 0) at terminal states (ie terminal_n=1)
            # 4) calculate advantage (adv_n) as A(s, a) = Q(s, a) - V(s)

        v_s = self.critic.forward(ob_no)
        v_s_next = self.critic.forward(next_ob_no)
        q_v = re_n + self.gamma * v_s_next * (1 - terminal_n)

        adv_n = q_v - v_s

        if self.standardize_advantages:
            adv_n = (adv_n - np.mean(adv_n)) / (np.std(adv_n) + 1e-8)
        return adv_n

    def train(self, ob_no, ac_na, re_n, next_ob_no, terminal_n):
        
        # TODO Implement the following pseudocode:

            # for agent_params['num_critic_updates_per_agent_update'] steps,
            #     update the critic

            # advantage = estimate_advantage(...)

            # for agent_params['num_actor_updates_per_agent_update'] steps,
            #     update the actor
        
        for i in range(self.agent_params['num_critic_updates_per_agent_update']):
            c_ls = self.critic.update(ob_no, next_ob_no, re_n, terminal_n)

        adv = self.estimate_advantage(ob_no, next_ob_no, re_n, terminal_n)

        for i in range(self.agent_params['num_actor_updates_per_agent_update']):
            a_ls = self.actor.update(ob_no, ac_na, adv)

        loss = OrderedDict()
        loss['Critic_Loss'] = c_ls  # put final critic loss here
        loss['Actor_Loss'] = a_ls  # put final actor loss here

        return loss

    def add_to_replay_buffer(self, paths):
        self.replay_buffer.add_rollouts(paths)

    def sample(self, batch_size):
        return self.replay_buffer.sample_recent_data(batch_size)
