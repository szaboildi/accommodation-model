# Modeling accommodation
*A single-pool model of accommodation & imitation*

During a conversation, one often adjusts their speech to be more similar to (or sometimes more different from) the person they are talking to - people who speak to each other often, start sounding like each other a little bit. This process is called accommodation. Accommodation can affect speech in many ways: it can affect speech sounds, affixes, words or syntactic patterns. This repository contains code and sample simulation files to model phonetic accommodation, i.e. accommodation affecting speech sounds, and is based on the model outlined in Szabó (2020). The first section explains how the model works, and the second section explains how it is implemented in this repository.

## The model
The model offers a theory for the internal, covert processes that take place when a speaker hears a token (instance) of a speech sound from their interlocutor, and produces a token of their own as a response. In a laboratory environment, this could happen during a shadowing task, where the participant hears a token (e.g. a recording of the word _pin_), and then is instructed to "identify the word by saying it out loud" themselves. In this model, categories (like /p/) are represented as a set of individual instances, each described along one or multiple phonetic measurements. In the examples in this repository, bilabial voiceless and voiced stops (tokens of \[p\] and \[b\]) are represented along a single dimension, Voice Onset Time (VOT). The categories of /p/ and /b/ are two sets of these one-dimensions datapoints.

When the speaker encounters a token, it creates an activation pattern in the speaker's pre-existing phonological representations - i.e. it activates the tokens already stored by the speaker (from previous interactions) to varying degrees. This activation level is affected by (at least) two factors. First, tokens in the representation are activated in inverse proportion to their distance from the interlocutor's token 
- i.e. pre-existing tokens that resemble the new token more closely are activated to a higher degree. Second, not all interlocutor tokens are equally prototypical representations of their category. For instance, in English, a \[p\] token with 60ms VOT (Voice Onset Time) is going to be more prototypical than a \[p\] token with 25ms VOT. The activation effect of each incoming interlocutor token is proportionate to how prototypical the token is, i.e. how well its phonetic properties correspond to its phonological label (its label given by lexical information and context). In this implementation, prototypicality is determined through Bayesian probabilities.

Once activation took place, the speaker produces a token of their own, whose phonetic properties will be the weighted averages of all the activates tokens, where the weights are the activation level of the given token. Optionally, this can be followed by a deactivation step, where the activation pattern is reset or somewhat diminished, which represents how activation fades over time. This model accounts for effects of pre-existing phonological representations limiting the extent to which accommodation can take place (e.g. not all inputs trigger convergent accommodation), and also allows for representations dynamically changing over time as a result of exposure to other people's speech.


## Repo structure
The ```code/``` folder contains the scripts that make up the model, and the ```outputs/``` folder includes some sample outputs of these scripts. 

### New classes and utility functions and methods
The ```representation_token_class.py``` defines two new classes. The ```Token``` class is used for representing individual instances of speech sounds (e.g. an individual instance of a \[p\] sound), and the ```Representation``` class represents an entire set of them (e.g. /p/: all the \[p\]'s the speaker encountered). While an instantiation of the ```Token``` class has attributes, describing the phonetic details of the given token along one or more dimensions (e.g. F2 of 212.7Hz or 45.1ms VOT), an instantiation of the  ```Representation``` class includes a set of instantiations of ```Token```, as well as some metadata about the distributions of these tokesn (mean and standard deviation along each dimension, number of tokens in the representation). The number and name of dimensions is up to the user's specification.

```Representation``` also has some utility methods, such as ```.update_metadata()```, ```.incorporate(token)```, ```.produce_new()```, and ```.populate()```, which populates the representation based on parameters (how many tokens it should be populated with, and what distribution the tokens should be randomly chosen from). On top of these utility methods, activation and deactivation methods are also implemented, which can be used to model different theories for how activation and deactivation could happen. There are four activation functions: 
* ```.activate_1(t, n, a)``` increments the activation level of the _n_ closest tokens to the incoming token _t_ by an amount _a_.
* ```.activate_2(t)``` increments the activation level of all tokens in the representation, and the amount of the increment is inversely proportionate to the given token's distance from incoming token _t_.
* ```.activate_3(t, n)``` does the same as ```.activate_2(t)```, but rather than incrementing the activation level of all tokens in the representation, only the closest _n_ number of tokens are affected.
* ```activate_4(t, n, coeff)``` increments the activation level of the closest _n_ number of tokens to the incoming token _t_, and their  activation levels are incremented by an amount proportionate to their closeness to the new token _t_ multiplied by a coefficient _coeff_.
In addition there are 2 versions of the deactivation function:
* ```.deactivate_fix(a)``` decreases the activation level of all tokens by a fixed custom amount _a_, with a floor of 0.
* ```.deactivate_flex()``` decreases the activation level of all tokens by the amount of the lowest non-zero activation level.

This file also defines some mathematical functions, necessary for somee of the ```Representation``` methods.

The ```representation_class.py``` file is deprecated.


### Simulations
The ```acc_simulation.py``` file showcases how the new classes and their methods can be used to run simulations. This example uses English /p/ and /b/ representations, and VOT as a phonetic dimension. First, the speaker's starting /p/ and /b/ representations are set up with 10,000 tokens each. The distribution of these representations are based on recorded data from a particular speaker in Szabó (2020), F08. The simulated speaker creates a first, baseline token of the same label as the stimuli (in this example, /p/) with the same VOT as the group average. This baseline token activates the 100 tokens in the representation which are closest to it. This is done using ```Representation.activate_4(t, n, coeff)```, where _coeff_ is the Bayesian probability of the token having the phonetic properties (the average VOT) given its phonological label (/p/). This represents the speaker's resting activation state. For the baseline token, this _coeff_ will be high, since it is a highly representative instantiation of the category.

The speaker is then exposed to a \[p\] token with 15ms VOT (although the script has 3 other commented out stimuli options: a \[p\] with 130ms VOT, a \[b\] with 15ms VOT, and a \[b\] with -130ms VOT). The speaker has to produce a \[p\] after each exposure. This is repeated 20 times. In every iteration the exposure token activates the 100 closest tokens in the representation in the same way. The _coeff_ will be relatively small, because 15ms is an uncommon VOT value for English /p/ - _coeff_ would be higher with the \[p\] with 130ms VOT, or with the \[b\] with 15ms VOT. After activation, the speaker produces a /p/ based on the current activation pattern, which in turn also activates a 100 tokens in the representation in a similar way. This new token is then also incorporated to the representation. No deactivation step takes place in this simulation, i.e. the activation of tokens does not fade away over time.

The baseline and the 20 speaker productions are outputted into a ```.txt``` file.

Aside from the other three alternatives for stimuli, this scripts includes a commented out simulation for vowel formants as well. This simulation works similarly, but uses the deprecated ```representation_class.py``` file, which has to be imported instead of ```representation_token_class.py```.


## Reference
Szabó, Ildikó Emese. 2020. _Representational limitations and consequences of phonetic accommodation: English and Hungarian speakers’ imitation of word-initial voiced and voiceless stops_. Doctoral dissertation at NYU. Available at: [https://lingbuzz.net/lingbuzz/005497](url)
