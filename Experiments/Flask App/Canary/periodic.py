#Functions to detect periodic sentences
from Canary import SentenceFormat

#Launcher function
def process(sentences):
    #Loop through the sentences and assign each one as either periodic
    for sentence in sentences:
        sentence.periodic = isPeriodic(sentence)
        if sentence.periodic = true:
            sentence.argument = isArgument(sentence)
        #Otherwise the argument will default to false and won't be processed any further

    return sentences


def isPeriodic(sentence):
    return True

def isArgument(sentence):
    return True

