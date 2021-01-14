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

############################################
## Setting up and running simulations     ##
#  with the use of                        ##
## the Representation and Token classes   ##
############################################

import random
import os

# For vowel simulations
# from representation_class import  Representation

from representation_token_class import Representation, Token


def main():
    random.seed(1)

    ## VOT simulation -- voiceless 'p' stimuli
    # Setting up the speaker's representational categories
    # (English, based on subject F08)
    speaker_vless_asp = Representation(n=10000, dims=[('VOT', 73.834, 19.932)], act=0.1, label='p')
    speaker_vless_asp.populate()
    speaker_vd_no_asp = Representation(n=7616, dims=[('VOT', 13.993, 5.751)], act=0.1, label='b')
    speaker_vd_no_asp.populate()
    speaker_vd_prevved = Representation(n=2384, dims=[('VOT', -89.980, 34.551)], act=0.1, label='b')
    speaker_vd_prevved.populate()
    speaker_vd = speaker_vd_no_asp.combine(speaker_vd_prevved)
    speaker_reps = speaker_vd.combine(speaker_vless_asp)


    # Choosing stimulus (Interlocutor's token)
    # From the experimental conditions
    # ('p' or 'b'; 'Extr. Asp.' condition or 'Extr. Prev.' condition)
    i_token_p_prev = Token(t_dims=[('VOT', 15)], t_label= 'p')
    #i_token_b_prev = Token(t_dims=[('VOT', -130)], t_label= 'b')
    #i_token_p_asp = Token(t_dims=[('VOT', 130)], t_label='p')
    #i_token_b_asp = Token(t_dims=[('VOT', 15)], t_label='b')

    i_token = i_token_p_prev


    # Speaker's initial production (before interaction with Interlocutor)
    # To simulate starting activation level
    vless_production = [
        'Speaker (initial): ' + str(speaker_vless_asp),
        'Interlocutor: ' + str(i_token)]
    vd_production = [
        'Speaker (initial): ' + str(speaker_vd),
        'Interlocutor: ' + str(i_token)]


    t0 = speaker_vless_asp.produce_new(i_token.label)
    m0 = speaker_reps.bayesian_prob(t0, 'VOT')
    speaker_vless_asp.activate_4(t0, 100, m0)


    for i in range(20):
        # Token from the Interlocutor activates the Speaker's representational categories
        # Based on the Bayesian probability of the token belonging to the given category
        m_i = speaker_reps.bayesian_prob(i_token, 'VOT')
        # print(m_i)
        speaker_vless_asp.activate_4(i_token, 100, m_i)
        speaker_vless_asp.incorporate(i_token)
        speaker_reps.incorporate(i_token)

        # Speaker produces their own token based on the activation pattern
        sp_token = speaker_vless_asp.produce_new(i_token.label, starting_act=0.1)
        # Token from Speaker further activates the Speaker's representational categories
        m_sp = speaker_reps.bayesian_prob(sp_token, 'VOT')
        speaker_vless_asp.activate_4(sp_token, 100, m_sp)
        speaker_vless_asp.incorporate(sp_token)
        speaker_reps.incorporate(sp_token)
        vless_production.append(str(sp_token.dimensions['VOT']))
        # Activation incrementally decreasing (fading) over time
        #speaker_vless_asp.deactivate_flex()


    # Write productions to .txt file
    with open(os.path.join(*(os.pardir, 'outputs', 'VOT',
                             'plain_p_F08_VOT.txt')), 'w', encoding='utf-8') as asp_f:
        for item in vless_production:
            asp_f.write(item + '\n')

    """
    with open(os.path.join(*(os.pardir, 'outputs', 'VOT',
                             'non_aspirating_VOT.txt')), 'w', encoding='utf-8') as no_asp_f:
        for item in no_asp_production:
            no_asp_f.write(item + '\n')
    """


    """
    ## Vowel simulation
    male_front_low = Representation(n=150000, dims=[('F1', 6.5, 0.5), ('F2', 11.8, 0.5)], act=0.1)
    male_front_low.populate()
    fem_front_low = Representation(n=150000, dims=[('F1', 8.2, 0.5), ('F2', 12.1, 0.5)], act=0.1)
    fem_front_low.populate()
    interloc_front_low = Representation(n=4000, dims=[('F1', 5.9, 0.1), ('F2', 11.2, 0.1)])
    interloc_front_low.populate()



    male_production = [
        'Speaker (initial): ' + str(male_front_low),
        'Interlocutor: ' + str(interloc_front_low)]
    female_production = [
        'Speaker (initial): ' + str(fem_front_low),
        'Interlocutor: ' + str(interloc_front_low)]




    # "Male" model
    for i in range(60):
        token = random.choice(interloc_front_low)
        male_front_low.activate_3(token, 200)

        # Comment out following line for dual-pool simulation
        male_front_low.incorporate(token)

        sp_token = male_front_low.produce_new(starting_act=0.1)
        male_front_low.incorporate(sp_token)
        male_production.append(str(sp_token['F1']) + '\t' + str(sp_token['F2']))
        male_front_low.deactivate_flex()

    # "Female" model
    for i in range(60):
        token = random.choice(interloc_front_low)
        fem_front_low.activate_3(token, 200)

        # Comment out following line for dual-pool simulation
        fem_front_low.incorporate(token)

        sp_token = fem_front_low.produce_new(starting_act=0.1)
        fem_front_low.incorporate(sp_token)
        female_production.append(str(sp_token['F1']) + '\t' + str(sp_token['F2']))
        fem_front_low.deactivate_flex()



    # Writing
    with open(os.path.join(*(os.pardir, 'outputs', 'vowels',
                        'frontlow_male_F1F2_single_60i.txt')), 'w', encoding='utf-8') as male_f:
        for item in male_production:
            male_f.write(item + '\n')


    with open(os.path.join(*(os.pardir, 'outputs', 'vowels',
                        'frontlow_female_F1F2_single_60i.txt')), 'w', encoding='utf-8') as female_f:
        for item in female_production:
            female_f.write(item + '\n')

    """


if __name__ == '__main__':
    main()