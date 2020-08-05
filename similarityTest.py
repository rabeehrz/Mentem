import spacy

nlp = spacy.load("en_core_web_md")  # make sure to use larger model!

description=input()

tokens = nlp(description)
testToken =[ {"key": 319, "value": nlp("hurt")},{"key": 300, "value": nlp("murder")},{"key": 304, "value": nlp("Dowry")},{"key": 312, "value": nlp("miscarriage")}]

keyOutput = []

for token in testToken:
    similarityValue = tokens.similarity(token["value"])
    print(tokens.text, token["value"].text, similarityValue)
    if(similarityValue > .5):
        keyOutput.append({"key": token["key"], "value": 1})
    else:
        keyOutput.append({"key": token["key"], "value": 0})

print(keyOutput)