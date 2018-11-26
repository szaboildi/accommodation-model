#!/usr/bin/python
"""
Copyright (C) 2018 Ildiko Emese Szabo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

###########################################
## Defining the class of representations ##
## and the class of tokens               ##
###########################################

import random
import statistics as stat

class Representation(list):
    def __init__(self, n, dims=(), act=0):
        """
        Initializes a representation with a certain number of tokens,
        with a given number of dimensions with their distributions and activation level
        :param n: Number of tokens to initialize the Representation object with
        :param dims: List of dimensions, where each dimension is a triplet of the form:
                     ('name', mean, sd)
        """
        self.dimensions = {dim[0]: (dim[1], dim[2]) for dim in dims}
        self.starting_act = act
        self.n = n

    def __str__(self):
        return "Representation with", str(self.n), "tokens\nDimensions:", str(self.dimensions)

    def populate(self):
        """
        Populates a set with the required number of tokens of desired distribution.
        :return: None, does it in place
        """
        for i in range(self.n):
            element = {dim: random.gauss(v[0], v[1]) for dim, v in self.dimensions}
            element['act'] = self.starting_act
            self.append(element)

        self.recalibrate_meta()

    def recalibrate_meta(self):
        """
        Updates the attributes automatically based on the properties of the set.
        :return: None, does it in place
        """
        for dim in self.dimensions:
            self.dimensions[dim] = (stat.mean([token[dim] for token in self]),
                                    stat.stdev([token[dim] for token in self]))
        self.n = len(self)

    def forget(self, m):
        """
        "Forgets" m number of elements. Tokens will be shuffled in the process.
        :param m: Number of elements to delete from representation
        :return: None, does it in place
        """
        random.shuffle(self)
        self = self[:self.n - m]
        self.recalibrate_meta()

    def incorporate_new(self, new_token):
        self.append(new_token)
        self.recalibrate_meta()

    def produce_new(self):
        activated = []
        token = {}
        try:
            for dim in self.dimensions:
                token[dim] = stat.mean([token[dim] * token['act'] for token in activated])
        except stat.StatisticsError:
            print('You have no activated tokens')



def EmptyError(Exception):
    """Raised when no tokens are activated"""
    pass