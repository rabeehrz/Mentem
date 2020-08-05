import spacy
import numpy as np
from flask import Flask,request
import json
import os

app = Flask(__name__)

dataReceived = "Hi"
dataReceivedFlag = False

@app.route('/')
def index():
    return "Flask server"
    
@app.route('/postdata', methods = ['POST'])
def postdata():
    data = request.get_json()
    print("postdatatoFlask")
    global dataReceivedFlag
    dataReceivedFlag = True
    global dataReceived
    dataReceived = data
    print(data)

    os.system('kill ')
    return {"status": 200}
    
def getInput():
    app.run(port=5000)
    while (not dataReceivedFlag):
        print("No data")


# initialization
nlp = spacy.load("en_core_web_md")  # make sure to use larger model!

# Conversation Samples
CONV_SAMPLES = [['greetings'], ['destitute'], ['marriage', 'husband', 'wife', 'spouse', 'divorce'], ['depressed', 'sad', 'lonely', 'melancholic', 'need care', 'anxious', 'insomnia', 'bad sleep', 'guilt']]
initialTest = 0

# Stores the analysis
analysis = [[], [], [], [], [], [], [], [], [], [], [], [], []]

# Output control for the web
outputToWeb = {"code": 0, "value": "initial", "response": "Hello I am Invictus.\nLet us start off by asking, is the consulting person from a poor background?"}

# This is to analyse the sentences given
def get_response(u_query):
    mostSimilarity = 0
    mostSimilarityValue = 0
    global outputToWeb
    global initialTest

    # Analysing the input
    for i in range (len (CONV_SAMPLES)):
        for j in range( len(CONV_SAMPLES[i])):
            if (nlp(u_query).similarity(nlp(CONV_SAMPLES[i][j])) > mostSimilarityValue):
                mostSimilarity = i
                mostSimilarityValue = nlp(u_query).similarity(nlp(CONV_SAMPLES[i][j]))
        
    # Print current analysis
    print(analysis)

    # Checking for destitute possibility
    if (initialTest == 0):
        initialTest = 1

        if (nlp(u_query).similarity(nlp("Yes")) > nlp(u_query).similarity(nlp("No"))):
            outputToWeb = {"code": 0, "value": "initial", "response": "Is the person being consulted a destitute?"}
            print(outputToWeb)
            print("RESPONSE:\nIs the person being consulted a destitute?")

            u_query = input()

            # The NGO has been assigned
            if (nlp(u_query).similarity(nlp("Yes")) > nlp(u_query).similarity(nlp("No"))):
                outputToWeb = {"code": 1, "value": "NGO-Yes", "response": "A volunteer will be sent to your location."}
                analysis[1].append("NGO")
                analysis[1].append("Yes")
            
            # NGO has not been assigned
            else:
                outputToWeb = {"code": 2, "value": "NGO-No", "response": "Could you tell me more about your problem?"}
                analysis[1].append("NGO")
                analysis[1].append("No")
        
        print(outputToWeb)
        print("RESPONSE:\nTell me your problems and your concerns.")

    # Checking sleep
    elif (initialTest == 1):
        initialTest = 2

        
    # Checking diet
    elif (initialTest == 2):
        initialTest = 3

        # Person has a good diet
        if (nlp(u_query).similarity(nlp("good")) > nlp(u_query).similarity(nlp("bad")) or nlp(u_query).similarity(nlp("yes")) > nlp(u_query).similarity(nlp("no"))):
            outputToWeb = {"code": 0, "value": "Diet-Yes", "response": "Tell me about your problem"}
            analysis[3].append("Diet")
            analysis[3].append("Good")

        # Person may suffer from diseases that cause lose of appetite
        else:    
            outputToWeb = {"code": 0, "value": "Diet-No", "response": "Tell me about your problem"}
            analysis[3].append("Diet")
            analysis[3].append("Bad")
        
        print(outputToWeb)
        print("RESPONSE:\nTell me about your problem")

    # Check for greetings
    elif CONV_SAMPLES[mostSimilarity][0] == 'greetings':

        # This is used to check greetings.
        outputToWeb = {"code": 0, "value": "greeting", "response": "Hello, nice to meet you.\nI am Invictus.\nI am here to help"}
        print("RESULT:\n\nHello, nice to meet you.\nI am Invictus.\nI am here to help\n")

    # Check for marriage related problems
    elif CONV_SAMPLES[mostSimilarity][0] == 'marriage':
        analysis[4].append("Marriage")

        # Gives the various connection to marriage related keywords
        print("Mariage report:")
        print("abuse", nlp(u_query).similarity(nlp("abuse")))
        print("beat", nlp(u_query).similarity(nlp("beat")))
        print("cheat", nlp(u_query).similarity(nlp("cheat")))
        print("rape", nlp(u_query).similarity(nlp("rape")))

        # Categorizing the marriage problems
        if (nlp(u_query).similarity(nlp("abuse")) > 0.5 or nlp(u_query).similarity(nlp("beat")) > 0.5):
            analysis[4].append("abuse")
        if (nlp(u_query).similarity(nlp("rape")) > 0.5):
            analysis[4].append("rape")
        if (nlp(u_query).similarity(nlp("cheat")) > 0.5 or nlp(u_query).similarity(nlp("affair")) > 0.5 or nlp(u_query).similarity(nlp("extramarital")) > 0.5):
            analysis[4].append("affair")
        if (nlp(u_query).similarity(nlp("physical")) > 0.5 or nlp(u_query).similarity(nlp("romance")) > 0.5):
            analysis[4].append("romance")
        
        # Finding the intensity of the problem
        strength = 0
        if ("romance" in analysis[4] or "affair" in analysis[4]):
            strength = strength + 1

        if ("abuse" in analysis[4] or "rape" in analysis[4]):
            strength = strength + 3

        # A severe case that needs attention
        if (strength > 2):
            outputToWeb = {"code": 4, "value": "marriage", "response": "I see that you are facing extreme issues at your home.\nYou will be given a priority in our cuncellor queue."}
            print("RESULT:\n\nI see that you are facing extreme issues at your home.\nYou will be given a priority in our cuncellor queue.")
        
        # A mild case that needs to checked
        elif (strength > 0):
            outputToWeb = {"code": 3, "value": "marriage", "response": "I hear your problems.\nI would suggest that you book a session with our councellor"}
            print("RESULT:\n\nI hear your problems.\nI would suggest that you book a session with our councellor")
            
    # Destitute checking
    elif CONV_SAMPLES[mostSimilarity][0] == 'destitute':

        # We rerun the program and consider the situation of a less privilaged person
        outputToWeb = {"code": 0, "value": "initial", "response": "Is the consulting person from a poor background?"}
        print("RESULT:\nis the consulting person from a poor background?")
        initialTest = True

    # Depressed person
    elif CONV_SAMPLES[mostSimilarity][0] == 'depressed':
        
        outputToWeb = {"code": 0, "value": "Sleep-No", "response": "How is your sleep schedule?"}
        print(outputToWeb)
        print("RESPONSE:\nHow is your sleep schedule?")
        u_query = input()

        # Person has a good sleep routine
        if (nlp(u_query).similarity(nlp("good")) + nlp(u_query).similarity(nlp("long")) + nlp(u_query).similarity(nlp("yes"))> nlp(u_query).similarity(nlp("bad")) + nlp(u_query).similarity(nlp("short")) + nlp(u_query).similarity(nlp("no"))):
            outputToWeb = {"code": 0, "value": "Sleep-Yes", "response": "How is your appetite?"}
            analysis[2].append("Sleep")
            analysis[2].append("Good")
        
        # Person might suffer from diseases pertaining to lack of sleep
        else:    
            outputToWeb = {"code": 0, "value": "Sleep-No", "response": "How is your appetite?"}
            analysis[2].append("Sleep")
            analysis[2].append("Bad")
        
        print(analysis)
        print(outputToWeb)
        print("RESPONSE:\nHow is your appetite?")
        u_query = input()

        strength = 0
        if ("Bad" in analysis[2]):
            strength = strength + 1

        if ("Bad" in analysis[3]):
            strength = strength + 1

        print(analysis)
        
        # Checking for the possibility of depression
        outputToWeb = {"code": 0, "value": "initial", "response": "Do you feel a sudden change in your weight?"}
        print(outputToWeb)
        u_query = input()

        # Case with sudden weight change
        if (nlp(u_query).similarity(nlp("yes")) > 0.6):
            strength = strength + 1
            analysis[5].append("weight-change")
            analysis[5].append("yes")

        # Case with no significant weight change
        else:
            analysis[5].append("weight-change")
            analysis[5].append("no")

        outputToWeb = {"code": 0, "value": "initial", "response": "Do you have any suicidal tendancy or uncontrollable emotions?"}
        print(outputToWeb)
        u_query = input()

        # Suicidal tendency check
        # Chance for a suicide attempt
        if (nlp(u_query).similarity(nlp("yes")) > 0.6):
            strength = strength + 1
            analysis[6].append("suicidal")
            analysis[6].append("yes")
            outputToWeb = {"code": 5, "value": "suicide", "response": "We will now redirect you to the human councellor"}
            print("RESULT:\nWe will now redirect you to the human councellor")
            return
        
        # Case with no suicide case
        else:
            strength = strength + 1
            analysis[6].append("suicidal")
            analysis[6].append("no")    

        # Analyse the attention span of the person
        outputToWeb = {"code": 0, "value": "initial", "response": "Are you unable to concentrate in your place of work or study?"}
        print(outputToWeb)
        u_query = input()

        # Case with low attention span
        if (nlp(u_query).similarity(nlp("no")) > 0.6):
            strength = strength + 1

        # Finding the possibility of depression
        if (strength >= 3):
            analysis[7].append("depression")
            analysis[7].append("yes")    
            outputToWeb = {"code": 6, "value": "depression", "response": "We suggest that you to attend group therapy"}
            print("RESULT:\nWe suggest that you to attend group therapy")

            # Check for schizophrenia
            outputToWeb = {"code": 0, "value": "depression", "response": "Do you feel a lack of hygiene?"}
            print("RESULT:\nDo you feel a lack of hygiene?")

            strength2 = 0

            # Checking for sudden hygiene mannersim change
            if (nlp(u_query).similarity(nlp("yes")) > 0.6):
                strength2 = strength2 + 1 

            outputToWeb = {"code": 0, "value": "initial", "response": "Are you having trouble expressing your emotions?"}
            print("RESULT:\nAre you having trouble expressing your emotions?")

            # Trouble emotionally expressing oneself
            if (nlp(u_query).similarity(nlp("yes")) > 0.6):
                strength2 = strength2 + 1 
            
            # Schizophrenia confrimed
            if (strength2  > 1):
                outputToWeb = {"code": 7, "value": "schizophrenia", "response": "We would suggest that you take the video test for further analysis."}
                print("RESULT:\nWe would suggest that you take the video test for further analysis.")
    
    print("Analysis:\n\n", analysis)
    return 0

# Begin of program

print("Hello I am Invictus.\nLet us start off by asking, is the consulting for another person?")
app.run(port=5000)
UQUERY=input("You: ")

# Repeated input request, "bye" gets you out
while (UQUERY != 'bye'):
    get_response(UQUERY)
    UQUERY=input("You: ")

# Exit condition
outputToWeb = {"code": 10, "value": "exit", "response": "Have a great day!"}
print("RESULT:\nHave a great day!")
