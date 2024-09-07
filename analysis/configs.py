'''
configs & settings are defined in this file
'''


from os.path import join
from os.path import abspath
from os.path import dirname
from os import pardir
from datetime import datetime

import numpy as np


class Config(object):

    tabu_child_nodes = ['corner_type', 'defense_type']


    # defense_type	corner_type	 dynamic_movement	shot_attempt	closely_marked	attacking_setup
    
    tabu_parent_nodes = ['shot_attempt']


    tabu_edges = [
                     ('corner_type', 'closely_marked'),

                     ('attacking_setup', 'closely_marked'),

                     ('dynamic_movement', 'attacking_setup'),

                     ('closely_marked', 'attacking_setup'),

    ]


    edge_threshold = 0.2


config = Config()
