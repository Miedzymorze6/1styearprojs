import speech_recognition as sr
from transformers import BertTokenizer, BertForSequenceClassification   #pip install speechrecognition transformers
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting for input...\n")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    
def analyze_sentiment_with_bert(text):
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    model = BertForSequenceClassification.from_pretrained(model_name)
    tokenizer = BertTokenizer.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    predicted_class = outputs.logits.argmax().item()
    sentiment_labels = ['very negative', 'negative', 'neutral', 'positive', 'very positive']
    sentiment = sentiment_labels[predicted_class]
    confidence_score = outputs.logits.softmax(dim=1).max().item()
    return sentiment, confidence_score

if __name__ == "__main__":
    while True:
        spoken_text = speech_to_text()
        if spoken_text:
            print(f"\nText: {spoken_text}")
            sentiment, score = analyze_sentiment_with_bert(spoken_text)
            print(f"Sentiment: {sentiment}")
            print(f"Confidence Score: {score}\n")
        else:
            print("No speech detected. Returning to Loop...")
