# Modelling accommodation
*A single-pool model of accommodation & imitation*

During a conversation, one often adjusts their speech to be more similar to (or sometimes more different from) the person they are talking to -- people who speak to each other often, start sounding like each other a little bit. This process is called accommodation. Accommodation can affect speech in many ways: it can affect speech sounds, affixes, words or syntactic patterns. This repository contains code and sample simulation files to model phonetic accommodation, i.e. accommodation affecting speech sounds, and is based on the model outlined in Szabó (2020). The first section explains how the model works, and the second section explains how it is implemented in this repository.

## The model
The model offers a theory for the internal, covert processes that take place when a speaker hears a token (instance) of a speech sound from their interlocutor, and produces a token of their own as a response. In a laboratory environment, this could happen during a shadowing task, where the participant hears a token (e.g. a recording of the word _pin_), and then is instructed to "identify the word by saying it out loud" themselves. In this model, categories (like /p/) are represented as a set of individual instances, each described along one or multiple phonetic measurements. In the examples in this repository, bilabial voiceless stops (tokens of \[p\] and \[b\]) are represented along a single dimension, Voice Onset Time (VOT). The categories of /p/ and /b/ are two sets of these one-dimensions datapoints.

When the speaker encounters a token, it creates an activation pattern in the speaker's pre-existing phonological representations -- i.e. it activates the tokens already stored by the speaker (from previous interactions) to varying degrees. This activation level is affected by (at least) two factors. First, tokens in the representation are activated in inverse proportion to their distance from the interlocutor's token -- i.e. pre-existing tokens that resemble the new token more closely are activated to a higher degree. Second, not all interlocutor tokens are equally prototypical representations of their category. For instance, in English, a \[p\] token with 60ms VOT (Voice Onset Time) is going to be more prototypical than a \[p\] token with 25ms VOT. The activation effect of each incoming interlocutor token is proportionate to how prototypical the token is, i.e. how well its phonetic properties correspond to its phonological label (its label given by lexical information and context). In this implementation, prototypicality is determined through Bayesian probabilities.

Once activation took place, the speaker produces a token of their own, whose phonetic properties will be the weighted averages of all the activates tokens, where the weights are the activation level of the given token. Optionally, this can be followed by a deactivation step, where the activation pattern is reset or somewhat diminished, which represents how activation fades over time. This model accounts for effects of pre-existing phonological representations limiting the extent to which accommodation can take place (e.g. not all inputs trigger convergent accommodation), and also allows for representations dynamically changing over time as a result of 


## Repo structure
The ```code/``` folder contains the scripts that make up the model, and the ```outputs/``` folder includes some sample outputs of these scripts.


## References
Szabó, Ildikó Emese. 2020.
