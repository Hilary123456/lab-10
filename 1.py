import pyttsx3
import speech_recognition as sr
import requests
import webbrowser
import json

# Load intents from JSON file
with open("intents.json", "r") as file:
    intents_data = json.load(file)

# Initialize pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)


# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_vosk(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't get that.")
            return ""
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return ""


# Function to handle intents
def handle_intent(intent, parameters=None):
    if intent == "activity":
        speak(intents_data["intents"][0]["responses"][0])
    elif intent == "name":
        speak(intents_data["intents"][1]["responses"][0])
    elif intent == "participants":
        speak(intents_data["intents"][2]["responses"][0])
    elif intent == "save":
        speak(intents_data["intents"][3]["responses"][0])
    elif intent == "find":
        speak(intents_data["intents"][4]["responses"][0].format(parameters))
    elif intent == "meaning":
        meaning = "Definition"  # Replace with the actual meaning
        speak(intents_data["intents"][5]["responses"][0].format(parameters, meaning=meaning))
    elif intent == "link":
        webbrowser.open_new_tab(f"https://www.google.com/search?q={parameters}")
        speak(intents_data["intents"][6]["responses"][0].format(parameters))
    elif intent == "example":
        example = "Example"  # Replace with the actual example
        speak(intents_data["intents"][7]["responses"][0].format(parameters, example=example))


# Main function
def main():
    speak("Hello, I am your voice assistant. How can I help you?")
    while True:
        command = recognize_speech()

        if command == "":
            continue

        if "random" in command or "next activity" in command:
            handle_intent("activity")
        elif "name" in command:
            handle_intent("name")
        elif "participants" in command:
            handle_intent("participants")
        elif "save" in command:
            handle_intent("save")
        elif "find" in command:
            word = command.split("find")[-1].strip()
            handle_intent("find", word)
        elif "meaning" in command:
            word = command.split("meaning")[-1].strip()
            handle_intent("meaning", word)
        elif "link" in command:
            word = command.split("link")[-1].strip()
            handle_intent("link", word)
        elif "example" in command:
            word = command.split("example")[-1].strip()
            handle_intent("example", word)


if __name__ == "__main__":
    main()







