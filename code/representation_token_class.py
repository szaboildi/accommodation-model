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
## and its utility functions             ##
###########################################

import random
import statistics as stats
from scipy.spatial import distance
import math
import numpy as np
from sklearn.neighbors import KernelDensity


def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def proportionate_inverse(x):
    return sigmoid(1/x)

class Token:
    def __init__(self, t_dims=None, t_act=None, t_label=None):
        """
        Initializes a token with a given number of values along certain phonetic dimensions
        and with a certain activation level and label (lexical information)
        :param dims: Tuple of dimensions, where each dimension is a pair of the form:
                     ('name', value)
        :param act: Activation of new token
        :param label: Label of token
        :return:
        """

        #dict.__init__(self, {})
        if t_dims is None:
            t_dims=()
        self.dimensions = {dim[0]: dim[1] for dim in t_dims}

        if t_act is None:
            self.act=0.0
        else:
            self.act = t_act

        if t_label is None:
            self.label = ""
        else:
            self.label = t_label


    def __str__(self):
        str_output = "Token with " + str(self.dimensions) + \
            ", Label: " + str(self.label) + \
            ", Activation: " + str(self.act)

        return str_output


class Representation:
    def __init__(self, n=None, dims=None, act=None, label=None):
        """
        Initializes a representation with a certain number of tokens,
        with a given number of dimensions with their distributions and activation level
        :param n: Number of tokens to initialize the Representation object with
        :param dims: Tuple of dimensions, where each dimension is a triplet of the form:
                     ('name', mean, standard deviation)
        :param act: Starting activation of tokens
        :param label: Label of the representation
        """
        #list.__init__(self, [])
        if n is None:
            self.n=0
        else:
            self.n = n

        if dims is None:
            self.dimensions=()
        else:
            self.dimensions = {dim[0]: (dim[1], dim[2]) for dim in dims}

        if act is None:
            self.starting_act=0.0
        else:
            self.starting_act = act

        if label is None:
            self.label = ""
        else:
            self.label = label

        self.tokens=[]

    def __str__(self):
        elements = self.tokens
        meta = "Representation of category " + str(self.label) + " with " + str(len(elements)) + \
               " tokens\nDimensions: " + str(self.dimensions) + '\n'

        if elements==[]:
            return meta

        #elements_str = {str(element) for element in elements}
        elements_str=""
        return meta + str(elements_str)


    def update_meta(self):
        """
        Updates the attributes automatically based on the properties of the set.
        :return: None, changes representation in place
        """
        for dim in self.dimensions.keys():
            self.dimensions[dim] = (stats.mean([token.dimensions[dim] for token in self.tokens]),
                                    stats.stdev([token.dimensions[dim] for token in self.tokens]))
        self.n = len(self.tokens)

    def populate(self):
        """
        Populates a set with the required number of tokens of desired distribution.
        :return: None, changes representation in place
        """
        for i in range(self.n):
            #token = Token(t_dims=None, t_act=None, t_label=None)
            dims_for_token = ((dim, random.gauss(v[0], v[1])) for (dim, v) in self.dimensions.items())
            t = Token(dims_for_token, self.starting_act, self.label)
            #token = Token()
            t.dimensions = {dim: random.gauss(v[0], v[1]) for dim, v in self.dimensions.items()}
            t.act = self.starting_act
            t.label = self.label
            # ((dim, random.gauss(v[0], v[1])) for (dim, v) in self.dimensions.items())
            # element['eucl'] = abs(reduce(lambda x, y: x*y, element.values()))

            self.tokens.append(t)
        self.update_meta()



    def forget(self, f):
        """
        "Forgets" f number of elements. Tokens will be shuffled in the process.
        :param f: Number of elements to delete from representation
        :return: None, changes representation in place
        """
        random.shuffle(self)
        for i in range(f):
            popped = self.tokens.pop()
        self.update_meta()


    def incorporate(self, new_token):
        """
        Incorporate a new token into the representation, metadata of representation gets updated
        :param new_token: Token to be added
        :return: None, changes representation in place
        """
        self.tokens.append(new_token)
        self.update_meta()


    def produce_new(self, label, starting_act=None):
        """
        :param label:
        :param starting_act:
        :return:
        """
        if starting_act is None:
            starting_act = self.starting_act
        activated = [act_t for act_t in self.tokens if act_t.act != 0 and act_t.label == label]
        token = Token()
        token.dimensions={}
        token.label = label

        try:
            for dim in self.dimensions.keys():
                token.dimensions[dim] = sum([token.dimensions[dim] * token.act for token in activated]) /\
                             sum([token.act for token in activated]) + (random.random() *
                                                                        random.choice([-2, -1, 1, 2]))
                # token['eucl'] = abs(reduce(lambda x, y: x * y, token.values()))
                token.act = starting_act
            return token
        except ZeroDivisionError:
            print('You have no activated tokens')



    def combine(self, other_rep):
        """
        Combines two representations into one
        :param other_rep: The representation to combine with self
        :return: New representation with a potentially multimodal distribution
        """
        new_rep = Representation(n=self.n+other_rep.n,
                                 act=None)
        new_rep.dimensions={dim_k: (self.dimensions[dim_k][0],
                                    self.dimensions[dim_k][1])
                            for dim_k in self.dimensions.keys()}
        new_rep.tokens = self.tokens + other_rep.tokens

        if self.label == other_rep.label:
            new_rep.label = self.label
        else:
            new_rep.label = self.label + "AND" + other_rep.label

        new_rep.update_meta()

        return new_rep

    def filter_by_label(self, label):
        """
        Returns a representation, with all the tokens from the bigger representation with a given label
        :param label: Label to filter by
        :return: Representation
        """
        new_rep = Representation(label=label)
        new_rep.dimensions = {dim_k: (self.dimensions[dim_k][0],
                                      self.dimensions[dim_k][1])
                              for dim_k in self.dimensions.keys()}
        new_rep.tokens = [t for t in self.tokens if t.label==label]

        new_rep.update_meta()

        return new_rep


    def closest_neighbors(self, input_token, k):
        """
        Provides the closest k neighbors of input token
        :param input_token: Input token (class: Token)
        :param k: How many closest neighbors to return
        :return: List of k closest neighbors (integer)
        """

        self.tokens.sort(key=lambda t: distance.euclidean(
            [v for k, v in t.dimensions.items()],
            [v for k, v in input_token.dimensions.items()]))

        neighbors = self.tokens[:k]

        return neighbors


    def label_match(self, input_token, k):
        """
        Estimates how fitting the input token's label is
        based on the k closest neighbors in a given representation
        (the representation should contain tokens of varying labels).
        :param input_token: Input token (class: Token)
        :param k: Number of neighbors to take into account
        :return: Match coefficient (integer)
        """
        neighbors = self.closest_neighbors(input_token, k)
        matching_neighbor_labels = [nb for nb in neighbors if nb.label == input_token.label]

        m = len(matching_neighbor_labels) / len(neighbors)

        return m


    def fit_kernel(self, dimname, value):
        #bw = (self.n * 3/4) ** (-1 / 5)
        #bw = self.n ** (-1/5)
        #print(bw)
        bw= 2.5

        # fit density
        obs_values= np.asarray([t.dimensions[dimname] for t in self.tokens])
        model = KernelDensity(bandwidth=bw, kernel='gaussian')
        obs_values = obs_values.reshape((len(obs_values), 1))
        model.fit(obs_values)
        # sample probabilities for a range of outcomes
        #poss_values = np.asarray([value for value in range(minvalue, maxvalue)])
        value_format = np.asarray([value])
        value_format = value_format.reshape((len(value_format), 1))
        probability = model.score_samples(value_format)[0]
        probability = np.exp(probability)

        # plot the histogram and pdf
        #pyplot.hist(obs_values, bins=100, density=True)
        #poss_values = np.asarray([value for value in range(0, 200)])
        #poss_values = poss_values.reshape((len(poss_values), 1))
        #probabilities = model.score_samples(poss_values)
        #probabilities = np.exp(probabilities)
        #pyplot.plot(poss_values[:], probabilities)
        #pyplot.show()

        return probability



    def bayesian_prob(self, new_token, dim):
        label = new_token.label
        value = new_token.dimensions[dim]

        others_with_lab = self.filter_by_label(label)

        p_lab = len(others_with_lab.tokens) / len(self.tokens)
        p_value = self.fit_kernel(dim, value)
        p_of_value_within_lab = others_with_lab.fit_kernel(dim, value)

        bayesian = (p_lab * p_of_value_within_lab) / p_value

        return bayesian

    # Activation functions
    def activate_1(self, new_token, n, added_act):
        """
        Vanilla activation function: after a new token is added
        n closest exemplars get activate. Their activation levels
        are incremented by a fixed amount.
        :param new_token: New token that causes activation
        :param n: Number of tokens to activate
        :param added_act: How much to increment activation levels by
        :return: None, changes representation in place
        """
        # Sort exemplars by their distance from the new token
        self.tokens.sort(key=lambda t: distance.euclidean(
            [v for k, v in t.dimensions.items()],
            [v for k, v in new_token.dimensions.items()]))
        # Modify the first n token's activation levels
        for i in range(n):
            self.tokens[i].act += added_act

    def activate_2(self, new_token):
        """
        Activation function: after a new token is added
        all exemplars in the representation are activated.
        Their activation levels are incremented by an amount
        proportionate to their distance from the new token.
        :param new_token: New token that causes activation
        :return: None, changes representation in place
        """
        for t in self.tokens:
            dist = distance.euclidean(
                [v for k, v in t.dimensions.items()],
                [v for k, v in new_token.dimensions.items()])
            if dist == 0:
                dist = 0.001
            t.act += proportionate_inverse(dist)

    def activate_3(self, new_token, n):
        """
        Activation function: after a new token is added the closest
        n number of exemplars in the representation are activated.
        Their activation levels are incremented by an amount
        proportionate to their distance from the new token.
            Hybrid of activate_1() and activate_2()
        :param new_token: New token that causes activation
        :param n: Number of tokens to activate
        :return: None, changes representation in place
        """
        # Sort exemplars by their distance from the new token
        self.tokens.sort(key=lambda t: distance.euclidean(
            [v for k, v in t.dimensions.items()],
            [v for k, v in new_token.dimensions.items()]))
        # Modify the closest n exemplar's activation level
        for i in range(n):
            dist = distance.euclidean(
                [v for k, v in self.tokens[i].dimensions.items()],
                [v for k, v in new_token.dimensions.items()])
            if dist == 0:
                dist = 0.1
            self.tokens[i].act += proportionate_inverse(dist)


    def activate_4(self, new_token, n, coeff):
        """
        Activation function: after a new token is added,
        the closest n number of exemplars in the representation are activated.
        Their activation levels are incremented by an amount
        proportionate to their closeness to the new token multiplied by a coefficient.
            Hybrid of activate_1() and activate_2()
        :param new_token: New token that causes activation
        :param n: Number of tokens to activate
        :param coeff: Coefficient for degree of activation
        :return: None, changes representation in place
        """
        # Sort exemplars by their distance from the new token
        self.tokens.sort(key=lambda t: distance.euclidean(
            [v for k, v in t.dimensions.items()],
            [v for k, v in new_token.dimensions.items()]))
        # Modify the closest n exemplar's activation level
        for i in range(n):
            dist = distance.euclidean(
                [v for k, v in self.tokens[i].dimensions.items()],
                [v for k, v in new_token.dimensions.items()])
            if dist == 0:
                dist = 0.1
            if new_token.label == self.tokens[i].label:
                self.tokens[i].act += proportionate_inverse(dist) * coeff


# Deactivation functions: fixed and flexible
    def deactivate_fix(self, amount):
        """
        Decreases the activation level of all exemplars
        by a fixed amount
        :param amount: Decrease to be implemented
        :return: None, changes representation in place
        """
        for token in self.tokens:
            if token.act > amount:
                token.act -= amount
            else:
                token.act = 0

    def deactivate_flex(self):
        """
        Decreases the activation level of all exemplars
        by the amount of the lowest non-zero activation level.
        :return: None, changes representation in place
        """
        act_levels = {token.act for token in self.tokens if token.act != 0}
        self.deactivate_fix(min(act_levels))



# Debugging
if __name__ == '__main__':
    random.seed(0)
    rep1 = Representation(n=50, dims=[('dummy_d', 10, 0.5)], act=0.1, label="foo")
    rep1.populate()
    #print(rep1)
    rep2 = Representation(n=15, dims=[('dummy_d', 100, 0.5)], act=0.1, label="bar")
    rep2.populate()
    #print(rep2)
    # print(rep1.dimensions)
    # print(rep1.dimensions.keys())
    # print(list(rep1.dimensions.keys())[0])
    rep_sum = rep1.combine(rep2)
    #print(str(rep_sum))

    input_token = Token(t_dims=[('dummy_d', 55)], t_label="foo")
    #[print(t) for t in rep_sum.closest_neighbors(input_token, 10)]
    #[print(t) for t in rep2.closest_neighbors(input_token, 10)]
    #print(input_token.dimensions)
    m = rep_sum.label_match(input_token, 10)
    #print(m)

    #rep1.forget(m=2)
    #token1 = rep1.produce_new()
    #rep1.incorporate(token1)
    #rep1.activate_1(token1, 20, 0.1)
    #rep1.activate_2(token1)
    #rep1.activate_3(token1, 20)
    #token2 = rep1.produce_new()
    # rep1.deactivate_fix(0.1)
    # rep1.deactivate_flex()

    #[print(t.act) for t in rep1.tokens if t.act > 0.1]