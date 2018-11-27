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
    def __init__(self, n, dims=(), act=0.0):
        """
        Initializes a representation with a certain number of tokens,
        with a given number of dimensions with their distributions and activation level
        :param n: Number of tokens to initialize the Representation object with
        :param dims: List of dimensions, where each dimension is a triplet of the form:
                     ('name', mean, sd)
        """
        list.__init__(self, [])
        self.dimensions = {dim[0]: (dim[1], dim[2]) for dim in dims}
        self.starting_act = act
        self.n = n

    def __str__(self):
        meta = "Representation with " + str(len(self)) + \
               " tokens\nDimensions: " + str(self.dimensions) + '\n'
        elements = list.__str__(self)
        return meta + elements


    def update_meta(self):
        """
        Updates the attributes automatically based on the properties of the set.
        :return: None, changes representation in place
        """
        for dim in self.dimensions:
            self.dimensions[dim] = (stat.mean([token[dim] for token in self]),
                                    stat.stdev([token[dim] for token in self]))
        self.n = len(self)


    def populate(self):
        """
        Populates a set with the required number of tokens of desired distribution.
        :return: None, changes representation in place
        """
        for i in range(self.n):
            element = {dim: random.gauss(v[0], v[1]) for (dim, v) in self.dimensions.items()}
            element['act'] = self.starting_act
            self.append(element)
        self.update_meta()


    def forget(self, m):
        """
        "Forgets" m number of elements. Tokens will be shuffled in the process.
        :param m: Number of elements to delete from representation
        :return: None, changes representation in place
        """
        random.shuffle(self)
        for i in range(m):
            popped = self.pop()
        self.update_meta()


    def incorporate_new(self, new_token):
        """
        Incorporate a new token into the representation, metadata of representation gets updated
        :param new_token: Token to be added
        :return: None, changes representation in place
        """
        self.append(new_token)
        self.update_meta()


    def produce_new(self, starting_act=None):
        if starting_act == None:
            starting_act = self.starting_act
        activated = [token for token in self if token['act'] != 0]
        token = {"act": starting_act}
        try:
            for dim in self.dimensions:
                token[dim] = sum([token[dim] * token['act'] for token in activated]) /\
                             sum([token['act'] for token in activated])
            return token
        except ZeroDivisionError:
            print('You have no activated tokens')


    ### TODO: define activation functions
    def activate_1(self, token, n, added_act):
        """
        Vanilla activation function: after a new token is added
        n closest exemplars get activate. Their activation levels
        are incremented by a fixed amount.
        :param token: New token that causes activation
        :param n: Number of tokens to activate
        :param added_act: How much to increment activation levels by
        :return: None, changes representation in place
        """
        pass

    def activate_2(self, token):
        """
        Activation function: after a new token is added
        all exemplars in the representation are activated.
        Their activation levels are incremented by an amount
        proportionate to their distance from the new token.
        :param token: New token that causes activation
        :return: None, changes representation in place
        """
        pass

    def activate_3(self, token, n):
        """
        Activation function: after a new token is added the closest
        n number of exemplars in the representation are activated.
        Their activation levels are incremented by an amount
        proportionate to their distance from the new token.
            Hybrid of activate_1() and activate_2()
        :param token: New token that causes activation
        :param n: Number of tokens to activate
        :return: None, changes representation in place
        """
        pass


# Deactivation functions: fixed and flexible
    def deactivate_fix(self, amount):
        """
        Decreases the activation level of all exemplars
        by a fixed amount
        :param amount: Decrease to be implemented
        :return: None, changes representation in place
        """
        for token in self:
            if token['act'] > amount:
                token['act'] -= amount
            else:
                token['act'] = 0

    def deactivate_flex(self):
        """
        Decreases the activation level of all exemplars
        by the amount of the lowest non-zero activation level.
        :return: None, changes representation in place
        """
        act_levels = {token['act'] for token in self if token['act'] != 0}
        self.deactivate_fix(min(act_levels))


# Debugging
if __name__ == '__main__':
    rep1 = Representation(n=50, dims=[('thing', 10, 0.5)], act=0.1)
    print(rep1)
    rep1.populate()
    print(rep1)
    rep1.forget(m=2)
    print(rep1)
    token = rep1.produce_new()
    print(token)