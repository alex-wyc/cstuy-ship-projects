import nltk

def stemSentence(text):
    return [token for token in text if token[1][0] in ['N', 'V', 'R', 'J']]

def splitParagraph(textBlock):
    sentences = []
    startPos = 0
    endPos = 0
    tokens = nltk.pos_tag(nltk.word_tokenize(textBlock))
    for i in range(0, len(tokens)):
        if tokens[i][1][0] in ['.', 'C', 'I']:
            endPos = i
            sentences.append(stemSentence(tokens[startPos:endPos]))
            startPos = i
    return sentences

if __name__ == '__main__':
    print splitParagraph(raw_input("text to stem: "))
