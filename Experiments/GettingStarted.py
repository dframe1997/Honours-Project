# ----- Discourse indicators ----- #
supportiveIndicators = ['therefore','thus','hence']
conflictingIndicators = ['however', 'but', 'despite']
linkedWords = []
numberOfLinksFound = 0;

def findRelations(inputText):
    global numberOfLinksFound
    inputTextList = inputText.split()
    for word in inputTextList:
        if word in supportiveIndicators:
            linkedWords.append(inputText.split(word))
            print "'" + linkedWords[numberOfLinksFound][0] + "'" + ' implies that ' + "'" + linkedWords[numberOfLinksFound][1] + "'"
            numberOfLinksFound = numberOfLinksFound + 1
        elif word in conflictingIndicators:
            linkedWords.append(inputText.split(word))
            print "'" + linkedWords[numberOfLinksFound][0] + "'" + ' conflicts with ' + "'" + linkedWords[numberOfLinksFound][1] + "'"
            numberOfLinksFound = numberOfLinksFound + 1

findRelations('I love chocolate, therefore I am fat.')
findRelations('Obama is no longer the president of the united states, hence there is someone else running the USA.')
findRelations('I would go to the cinema but it is closed')
