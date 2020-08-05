from flask import Flask,request
import json
import spacy

# initialization
nlp = spacy.load("en_core_web_md")  # make sure to use larger model!

# Conversation Samples
CONV_SAMPLES = [['greetings'], ['destitute'], ['marriage', 'husband', 'wife', 'spouse', 'divorce'], ['depressed', 'sad', 'lonely', 'melancholic', 'need care', 'anxious', 'insomnia', 'bad sleep', 'guilt']]
initialTest = 2
depressedTest = 0
strength = 0

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
    global depressedTest
    global strength

    print("Strength", strength)

    # Analysing the input
    for i in range (len (CONV_SAMPLES)):
        for j in range( len(CONV_SAMPLES[i])):
            if (nlp(u_query).similarity(nlp(CONV_SAMPLES[i][j])) > mostSimilarityValue):
                mostSimilarity = i
                mostSimilarityValue = nlp(u_query).similarity(nlp(CONV_SAMPLES[i][j]))
        
    # Print current analysis
    print(analysis)

    # Check the initial condition for bystander
    if (initialTest == 0):
        initialTest = 1

        # Is a bystander
        if (nlp(u_query).similarity(nlp("Yes")) > nlp(u_query).similarity(nlp("No"))):
            
            # The output value
            outputToWeb = {"code": 0, "value": "initial", "response": "Is the person being consulted a destitute?"}
            print(outputToWeb)
            print("RESPONSE:\nIs the person being consulted a destitute?")
            
            # Return the output
            return outputToWeb
        
        # Not a bystander
        else:

            # Initialization
            initialTest  = 2    
            outputToWeb = {"code": 0, "value": "message", "response": "How are you feeling?"}

            # Returned value
            return outputToWeb

    # To check for the codition to send an NGO to the location
    elif (initialTest == 1):

        initialTest = 2

        # Send NGO to the location
        if (nlp(u_query).similarity(nlp("Yes")) > nlp(u_query).similarity(nlp("No"))):
            
            # The value is formatted
            outputToWeb = {"code": 1, "value": "NGO-Yes", "response": "A volunteer will be sent to your location."}
            analysis[1].append("NGO")
            analysis[1].append("Yes")
            
        # NGO has not been assigned
        else:
            
            # The person is not a destitute 
            outputToWeb = {"code": 2, "value": "NGO-No", "response": "How are you feeling now?"}
            analysis[1].append("NGO")
            analysis[1].append("No")
        
        # Return the output format value
        return outputToWeb


    # Destitute checking
    elif CONV_SAMPLES[mostSimilarity][0] == 'destitute':

        # We rerun the program and consider the situation of a less privilaged person
        outputToWeb = {"code": 0, "value": "initial", "response": "Is the consulting person from a poor background?"}
        print("RESULT:\nis the consulting person from a poor background?")
        initialTest = 1

        # Return the value
        return outputToWeb

    if CONV_SAMPLES[mostSimilarity][0] == 'depressed' or depressedTest > 0:
        
        if (depressedTest == 0):
            depressedTest = 1

            # Check the sleep schedule
            outputToWeb = {"code": 0, "value": "Sleep", "response": "How is your sleep schedule?"}
            print(outputToWeb)
            print("RESPONSE:\nHow is your sleep schedule?")

            # Return the required value
            return outputToWeb

        elif (depressedTest == 1):
            depressedTest = 2

            if (nlp(u_query).similarity(nlp("good")) + nlp(u_query).similarity(nlp("long")) + nlp(u_query).similarity(nlp("yes"))> nlp(u_query).similarity(nlp("bad")) + nlp(u_query).similarity(nlp("short")) + nlp(u_query).similarity(nlp("no"))):
                outputToWeb = {"code": 0, "value": "Sleep-Yes", "response": "How is your appetite?"}
                analysis[2].append("Sleep")
                analysis[2].append("Good")
        
            # Person might suffer from diseases pertaining to lack of sleep
            else:    
                outputToWeb = {"code": 0, "value": "Sleep-No", "response": "How is your appetite?"}
                analysis[2].append("Sleep")
                analysis[2].append("Bad")

            # Formatting the output
            print(analysis)
            print(outputToWeb)
            print("RESPONSE:\nHow is your appetite?")

            # Returning the value that is required
            return outputToWeb

        elif (depressedTest == 2):

            depressedTest = 3

            # Person has a good diet
            if (nlp(u_query).similarity(nlp("good")) + nlp(u_query).similarity(nlp("yes")) > nlp(u_query).similarity(nlp("bad")) + nlp(u_query).similarity(nlp("no"))):
                
                # Analyzing the output
                outputToWeb = {"code": 0, "value": "Diet-Yes", "response": "Do you know today's date or remember your neighbour's name?"}
                analysis[3].append("Diet")
                analysis[3].append("Good")

            # Person may suffer from diseases that cause lose of appetite
            else:    

                # Analyzing the output
                outputToWeb = {"code": 0, "value": "Diet-No", "response": "Do you know today's date or remember your neighbour's name?"}
                analysis[3].append("Diet")
                analysis[3].append("Bad")

            # Analyzing th strength of situation
            if ("Bad" in analysis[2]):
                strength = strength + 1

            if ("Bad" in analysis[3]):
                strength = strength + 1

            print(analysis)

            # Checking for the possibility of depression
            print(outputToWeb)
            
            # return value to get the output
            return outputToWeb

        # For a sudden weight change
        elif (depressedTest == 3):

            depressedTest = 4

            # Sudden weight change
            if (nlp(u_query).similarity(nlp("good")) + nlp(u_query).similarity(nlp("yes")) > nlp(u_query).similarity(nlp("bad")) + nlp(u_query).similarity(nlp("no"))):
                
                # Analyzing the output
                outputToWeb = {"code": 0, "value": "Weight-Change-Yes", "response": "Do you ever think of ending your life?"}
                analysis[5].append("Weight-change")
                analysis[5].append("Good")

            # No sudden wight change
            else:    

                # Analyzing the output
                outputToWeb = {"code": 0, "value": "Weight-Change-No", "response": "Do you ever think of ending your life?"}
                analysis[5].append("Weight-change")
                analysis[5].append("Bad")

            # Return the output needed
            return outputToWeb

        elif (depressedTest == 4):

            depressedTest = 5

            # Analyzing the suicide case
            if (nlp(u_query).similarity(nlp("good")) > nlp(u_query).similarity(nlp("bad")) or nlp(u_query).similarity(nlp("yes")) > nlp(u_query).similarity(nlp("no"))):

                strength = strength + 1
                analysis[6].append("suicidal")
                analysis[6].append("yes")
                outputToWeb = {"code": 5, "value": "suicide", "response": "We will now redirect you to the human councellor"}
                print("RESULT:\nWe will now redirect you to the human councellor")
                return outputToWeb
            
            # Case with no suicide case
            else:
                strength = strength + 1
                analysis[6].append("suicidal")
                analysis[6].append("no")    

                # Analyse the attention span of the person
                outputToWeb = {"code": 0, "value": "initial", "response": "Do you ever see, hear, smell, feel, or taste things that are not really there?"}
                print(outputToWeb)

                # Return the value
                return outputToWeb

        elif (depressedTest == 5):
            print("HAHAHA")
            depressedTest = 6

            # Case with low attention span
            print(strength)

            if (nlp(u_query).similarity(nlp("no")) > 0.6):
                strength = strength + 1

            # Finding the possibility of depression
            if (strength >= 3):

                # Analyze the output
                analysis[7].append("depression")
                analysis[7].append("yes")    

                # Get the return value
                outputToWeb = {"code": 6, "value": "depression", "response": "We suggest that you to attend group therapy"}
                print("RESULT:\nWe suggest that you to attend group therapy")

                # Return the value
                return outputToWeb

    elif CONV_SAMPLES[mostSimilarity][0] == 'greetings':

        # This is used to check greetings.
        outputToWeb = {"code": 0, "value": "greeting", "response": "Hello, nice to meet you.\nI am Invictus.\nI am here to help"}
        print("RESULT:\n\nHello, nice to meet you.\nI am Invictus.\nI am here to help\n")

        return outputToWeb
    
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

            # Return data
            return outputToWeb
        
        # A mild case that needs to checked
        elif (strength > 0):
            outputToWeb = {"code": 3, "value": "marriage", "response": "I hear your problems.\nI would suggest that you book a session with our councellor"}
            print("RESULT:\n\nI hear your problems.\nI would suggest that you book a session with our councellor")

            # Return data
            return outputToWeb

    return {"code": 999, "value": "Suggestion", "response": "We suggest that you listen to our prepared music.\nWe also suggest some exercises for you.\nIt will calm your mind."}

app = Flask(__name__)
    
@app.route('/')
def index():
    return "Flask server"
    
@app.route('/postdata', methods = ['POST'])
def postdata():
    data = request.get_data()
    data = data.decode("utf-8")

    print(type(data))
    print(data)
    print(data[5:])

    data = data[5:]
    newData = ""
    word = ""

    for i in range(len(data)):
        if (data[i].isalpha()):
            word = word + data[i]
        else:
            newData = newData + " " +word
            word = ""
    newData = newData + " " +word

    print(newData)
    OutputWeb = get_response(newData)

    print(OutputWeb)
    return OutputWeb
    
if __name__ == "__main__":
    app.run(port=5000)