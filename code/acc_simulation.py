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
## Setting up simulations with the use of ##
## the Representation class               ##
############################################

import random
import os
from representation_class import Representation


def main():
    random.seed(1)
    """
    #VOT
    speaker_vless_asp = Representation(n=550, dims=[('VOT', 70, 5)], act=0.1)
    speaker_vless_asp.populate()
    speaker_vless_no_asp = Representation(n=550, dims=[('VOT', 15, 5)], act=0.1)
    speaker_vless_no_asp.populate()
    interloc_vless = Representation(n=550, dims=[('VOT', 140, 5)])
    interloc_vless.populate()

    asp_production = [
        'Speaker (initial): ' + str(speaker_vless_asp),
        'Interlocutor: ' + str(interloc_vless)]
    no_asp_production = [
        'Speaker (initial): ' + str(speaker_vless_no_asp),
        'Interlocutor: ' + str(interloc_vless)]

    for i in range(20):
        token = random.choice(interloc_vless)
        speaker_vless_asp.activate_3(token, 50)
        speaker_vless_asp.incorporate(token)
        sp_token = speaker_vless_asp.produce_new(starting_act=0.1)
        speaker_vless_asp.incorporate(sp_token)
        # print(sp_token)
        asp_production.append(str(sp_token['VOT']))
        speaker_vless_asp.deactivate_flex()

    for i in range(20):
        token = random.choice(interloc_vless)
        speaker_vless_no_asp.activate_3(token, 50)
        speaker_vless_no_asp.incorporate(token)
        sp_token = speaker_vless_no_asp.produce_new(starting_act=0.1)
        speaker_vless_no_asp.incorporate(sp_token)
        # print(sp_token)
        no_asp_production.append(str(sp_token['VOT']))
        speaker_vless_no_asp.deactivate_flex()

    with open(os.path.join(*(os.pardir, 'outputs', 'VOT',
                             'aspirating_VOT.txt')), 'w', encoding='utf-8') as asp_f:
        for item in asp_production:
            asp_f.write(item + '\n')

    with open(os.path.join(*(os.pardir, 'outputs', 'VOT',
                             'non_aspirating_VOT.txt')), 'w', encoding='utf-8') as no_asp_f:
        for item in no_asp_production:
            no_asp_f.write(item + '\n')

    """

    # Vowels
    male_front_low = Representation(n=550, dims=[('F1', 6.5, 0.5), ('F2', 11.8, 0.5)], act=0.1)
    male_front_low.populate()
    fem_front_low = Representation(n=550, dims=[('F1', 8.2, 0.5), ('F2', 12.1, 0.5)], act=0.1)
    fem_front_low.populate()
    interloc_front_low = Representation(n=550, dims=[('F1', 5.9, 0.1), ('F2', 11.2, 0.1)])
    interloc_front_low.populate()

    male_production = [
        'Speaker (initial): ' + str(male_front_low),
        'Interlocutor: ' + str(interloc_front_low)]
    female_production = [
        'Speaker (initial): ' + str(fem_front_low),
        'Interlocutor: ' + str(interloc_front_low)]

    print('Male:')
    for i in range(20):
        token = random.choice(interloc_front_low)
        male_front_low.activate_3(token, 50)
        # Comment out following line for dual-pool simulation
        # male_front_low.incorporate(token)
        sp_token = male_front_low.produce_new(starting_act=0.1)
        male_front_low.incorporate(sp_token)
        male_production.append(str(sp_token['F1']) + '\t' + str(sp_token['F2']))
        print(sp_token)
        male_front_low.deactivate_flex()

    print('Female:')
    for i in range(20):
        token = random.choice(interloc_front_low)
        fem_front_low.activate_3(token, 50)
        # Comment out following line for dual-pool simulation
        # fem_front_low.incorporate(token)
        sp_token = fem_front_low.produce_new(starting_act=0.1)
        fem_front_low.incorporate(sp_token)
        female_production.append(str(sp_token['F1']) + '\t' + str(sp_token['F2']))
        print(sp_token)
        fem_front_low.deactivate_flex()

    with open(os.path.join(*(os.pardir, 'outputs', 'vowels',
                        'frontlow_male_F1F2_dual.txt')), 'w', encoding='utf-8') as male_f:
        for item in male_production:
            male_f.write(item + '\n')

    with open(os.path.join(*(os.pardir, 'outputs', 'vowels',
                        'frontlow_female_F1F2_dual.txt')), 'w', encoding='utf-8') as female_f:
        for item in female_production:
            female_f.write(item + '\n')



if __name__ == '__main__':
    main()