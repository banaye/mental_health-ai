from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random


# Create your views here.

class Chatbot:
    def __init__(self):
        self.responses = {
            "greeting": [
                "Hello! How can I assist you today?",
                "Hi there! I'm here to help. What would you like to talk about?",
                "Greetings! How are you feeling today?"
            ],
            "farewell": [
                "Goodbye! Take care of yourself.",
                "See you later! Remember, I'm always here if you need to talk.",
                "Farewell! Wishing you all the best."
            ],
            "default": [
                "I'm here to listen. Please tell me more.",
                "That sounds important. Can you elaborate?",
                "I'm sorry to hear that. How can I support you?"
            ],
            "anxious":[
                "It's okay to feel anxious sometimes. Take deep breaths and try to focus on the present moment.",
                "Remember, you're not alone. Many people experience anxiety, and there are ways to manage it.",
                "If your anxiety feels overwhelming, consider reaching out to a mental health professional for support."
            ],
            "sad":[
                "It's okay to feel sad sometimes. Allow yourself to experience your emotions and take care of yourself.",
                "Remember, you're not alone. Many people go through tough times, and there are ways to find support.",
                "If your sadness persists or feels overwhelming, consider reaching out to a mental health professional for help."
            ],
            "stressed":[
                "It's important to take breaks and practice self-care when you're feeling stressed. Try to find activities that help you relax.",
                "Remember, you're not alone. Many people experience stress, and there are ways to manage it effectively.",
                "If your stress feels overwhelming or persistent, consider reaching out to a mental health professional for support."
            ],
            "lonely":[
                "It's okay to feel lonely sometimes. Reach out to friends, family, or support groups to connect with others.",
                "Remember, you're not alone. Many people experience loneliness, and there are ways to find companionship and support.",
                "If your loneliness persists or feels overwhelming, consider reaching out to a mental health professional for help."
            ],
            "angry":[
                "It's normal to feel angry sometimes. Try to find healthy ways to express and manage your anger.",
                "Remember, you're not alone. Many people experience anger, and there are strategies to cope with it effectively.",
                "If your anger feels overwhelming or persistent, consider reaching out to a mental health professional for support."
            ],
            "overwhelmed":[
                "It's okay to feel overwhelmed sometimes. Take a step back, prioritize your tasks, and focus on one thing at a time.",
                "Remember, you're not alone. Many people experience overwhelm, and there are strategies to manage it effectively.",
                "If your feelings of overwhelm persist or feel unmanageable, consider reaching out to a mental health professional for support."
            ],
            "depressed":[
                "It's important to remember that you're not alone. Many people experience depression, and there are ways to find support and treatment.",
                "Consider reaching out to a mental health professional who can provide guidance and assistance tailored to your needs.",
                "Engaging in activities you enjoy, maintaining a routine, and connecting with loved ones can also help improve your mood."
            ]
        }
        #coping strategies
        self.coping_strategies = {
            "breathing":
                "breathe in deeply through your nose for four counts"
                "hold your breath for seven counts"
                "breathe out slowly through your mouth for eight counts"
                "repeat this cycle three to four times",
            
            "mindfulness":
                "find a quiet and comfortable place to sit or lie down"
                "close your eyes and focus on your breath"
                "notice the sensation of your breath as it enters and leaves your body"
                "if your mind starts to wander, gently bring your attention back to your breath"
                "practice this for five to ten minutes",
            "grounding":
                "find a comfortable and safe place to sit or stand"
                "take a few deep breaths and focus on your surroundings"
                "identify five things you can see, four things you can touch, three things you can hear, two things you can smell, and one thing you can taste"
                "focus on each sensation for a few moments before moving on to the next",
            "coping":
                "engage in physical activity, such as going for a walk or doing yoga"
                "practice relaxation techniques, such as progressive muscle relaxation or guided imagery"
                "connect with supportive friends or family members"
                "engage in hobbies or activities that bring you joy",
            "self-care":
                "ensure you're getting enough sleep, eating nutritious meals, and staying hydrated"
                "set aside time for activities you enjoy, such as reading, listening to music, or taking a bath"
                "practice positive self-talk and challenge negative thoughts",
                
        }
        #detect crisis keywords in user input

    def detect_crisis(self, text):
        crisis_keywords = [
            "suicide", "self-harm", "harm myself", "end my life", "kill myself"
        ]
        return any(keyword in text.lower() for keyword in crisis_keywords)

    #analyze sentiment of user input 
    def analyze_sentiment(self, text):
        text_lower = text.lower()

        mood_keywords = {
            "anxious": ["anxious", "nervous", "worried", "tense"],
            "sad": ["sad", "down", "unhappy", "depressed"],
            "stressed": ["stressed", "overwhelmed", "pressured", "tense"],
            "lonely": ["lonely", "isolated", "alone", "abandoned"],
            "angry": ["angry", "mad", "frustrated", "irritated"],
            "overwhelmed": ["overwhelmed", "swamped", "burdened", "stressed"],
            "depressed": ["depressed", "hopeless", "worthless", "guilty"],
            "frustrated": ["frustrated", "annoyed", "irritated", "disappointed"],
            "fearful": ["fearful", "scared", "afraid", "nervous"],
        }
        #check for mood keywords
        for mood, keywords in mood_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return mood

        return "neutral"

    #generate response based on user input
    def generate_response(self, user_input):
        # Check for coping strategies keywords
        for strategy, response in self.coping_strategies.items():
            if strategy in user_input.lower():
                return response

        mood = self.analyze_sentiment(user_input)
        if mood != "neutral" and mood in self.responses:
            return random.choice(self.responses[mood])

        # Check for crisis keywords
        defaults = [
            "I'm here to listen. Please tell me more.",
            "That sounds important. Can you elaborate?",
            "I'm sorry to hear that. How can I support you?"
        ]
        return random.choice(defaults)

#initialize chatbot instance
chatbot = Chatbot()


def index(request):
    return render(request, 'chatbot/index.html')

@csrf_exempt
def get_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message', '')
            
            is_crisis = chatbot.detect_crisis(user_input)
            response = chatbot.generate_response(user_input)
            
            if is_crisis:
                response = ("It sounds like you're going through a really tough time. "
                            "Please consider reaching out to a mental health professional or a trusted person in your life for support. "
                            "You can also contact a crisis hotline for immediate help."
                            "Your life is valuable, and there are people who care about you and want to help.")
                
            
            return JsonResponse({
                'response': response,
                'crisis': is_crisis
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
                
              
              
          

    
