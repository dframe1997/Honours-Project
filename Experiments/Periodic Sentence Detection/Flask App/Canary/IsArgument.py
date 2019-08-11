def isArgument(sentence):
    if 'if' in sentence.tokens:
        print('true')
        return True
    else:
        print('false')
        return False