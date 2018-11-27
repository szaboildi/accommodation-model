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
from representation_class import Representation

def main():
    random.seed(1)
    speaker_vless = Representation(n=250, dims=[('VOT', 70, 2)], act=0.1)
    speaker_vless.populate()
    interloc_vless = Representation(n=250, dims=[('VOT', 140, 10)])
    interloc_vless.populate()

    for i in range(20):
        token = random.choice(interloc_vless)
        speaker_vless.activate_3(token, 20)
        speaker_vless.incorporate(token)
        sp_token = speaker_vless.produce_new(starting_act=0.1)
        speaker_vless.incorporate(sp_token)
        print(sp_token)
        speaker_vless.deactivate_flex()


if __name__ == '__main__':
    main()