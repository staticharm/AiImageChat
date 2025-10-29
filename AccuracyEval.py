import time
import psutil
import csv
import google.generativeai as genai
import os
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv
# Initialize models
load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")
embedder = SentenceTransformer('all-MiniLM-L6-v2')


test_data = [
{"query": "What is Ayurveda?", "expected": "Ayurveda is an ancient Indian system of medicine that promotes holistic health through balance of body, mind, and spirit."},
{"query": "Name the three doshas.", "expected": "The three doshas are Vata, Pitta, and Kapha."},
{"query": "What does Pitta dosha represent?", "expected": "Pitta represents the fire and water elements, governing metabolism and digestion."},
{"query": "How to balance Kapha?", "expected": "Kapha can be balanced through light, warm foods and regular exercise."},
{"query": "Which herbs help improve digestion?", "expected": "Ginger, cumin, fennel, and turmeric are commonly used to aid digestion."},
{"query": "What are the five elements in Ayurveda?", "expected": "Earth, Water, Fire, Air, and Space."},
{"query": "Explain Vata imbalance symptoms.", "expected": "Vata imbalance causes anxiety, dry skin, constipation, and restlessness."},
{"query": "What is Panchakarma?", "expected": "Panchakarma is a detoxification therapy in Ayurveda that cleanses and rejuvenates the body."},
{"query": "Best foods for Pitta?", "expected": "Cool, sweet, and bitter foods like cucumber, coconut, and leafy greens help Pitta."},
{"query": "What causes Kapha imbalance?", "expected": "Overeating, lack of movement, and heavy foods can cause Kapha imbalance."},
{"query": "What is Rasayana therapy?", "expected": "Rasayana is a rejuvenation therapy to enhance vitality and longevity."},
{"query": "What is Triphala?", "expected": "Triphala is a combination of three fruits—Haritaki, Bibhitaki, and Amalaki—used for detoxification and digestion."},
{"query": "Which oil is used in Abhyanga massage?", "expected": "Sesame oil is commonly used in Abhyanga massage for nourishment."},
{"query": "What is the ideal time for meditation?", "expected": "Early morning (Brahma Muhurta) is considered ideal for meditation."},
{"query": "What are sattvic foods?", "expected": "Sattvic foods are pure, light, and nourishing, like fruits, milk, and whole grains."},
{"query": "What is Ayurveda’s view on sleep?", "expected": "Ayurveda recommends 7–8 hours of sound sleep for maintaining dosha balance."},
{"query": "Explain the concept of Ojas.", "expected": "Ojas is the essence of vitality and immunity formed through proper digestion and balance."},
{"query": "What is the Ayurvedic view on exercise?", "expected": "Exercise should be moderate and according to one’s body constitution (Prakriti)."},
{"query": "Which dosha is dominant in winter?", "expected": "Kapha is dominant in winter due to cold and heavy qualities."},
{"query": "Name two Ayurvedic detox methods.", "expected": "Virechana (purgation) and Basti (enema) are two Ayurvedic detox methods."},


{"query": "What is the purpose of this chatbot?", "expected": "It helps answer questions and analyze images using Gemini 2.5 API."},
{"query": "Can you explain what Gemini 2.5 is?", "expected": "Gemini 2.5 is Google’s multimodal AI model capable of processing text and images."},
{"query": "What does multimodal mean?", "expected": "It means the model can handle multiple input types like text, images, and audio."},
{"query": "How is API latency measured?", "expected": "Latency is measured as the time taken between sending a request and receiving a response."},
{"query": "What does real-time performance monitoring mean?", "expected": "It tracks CPU, memory, and latency while the model generates responses."},
{"query": "What programming language is used in this chatbot?", "expected": "Python is used with Streamlit for the interface and Google Gemini API for responses."},
{"query": "Can this chatbot analyze images?", "expected": "Yes, it supports multimodal interaction including image understanding."},
{"query": "What is the benefit of API streaming?", "expected": "It reduces response time by sending data incrementally rather than waiting for full generation."},
{"query": "Which library is used for embedding comparison?", "expected": "The SentenceTransformer library is used for semantic similarity evaluation."},
{"query": "What is a semantic similarity score?", "expected": "It measures how closely two sentences are related in meaning using embeddings."},
{"query": "How do you calculate response accuracy?", "expected": "By comparing the generated response with expected answers using cosine similarity."},
{"query": "What is the difference between accuracy and similarity?", "expected": "Accuracy is binary correctness; similarity measures semantic closeness."},
{"query": "What model version is used here?", "expected": "The model used is 'models/gemini-2.5-flash'."},
{"query": "How are test results stored?", "expected": "Metrics like latency, CPU, and accuracy are stored in a CSV file."},
{"query": "What does CPU(%) indicate?", "expected": "It shows how much processing power was used during inference."},
{"query": "What does memory(%) indicate?", "expected": "It shows how much RAM usage changed during the API call."},
{"query": "How can performance be improved?", "expected": "By using API streaming and optimizing model calls."},
{"query": "What framework is used for the UI?", "expected": "Streamlit is used for the web-based interface."},
{"query": "Can I use this chatbot offline?", "expected": "No, it requires internet access to call the Gemini API."},
{"query": "Is the Gemini model open source?", "expected": "No, it’s provided through Google’s API with an API key."},
]

results = []
accurate_count = 0
total_latency = 0

print("\n🚀 Starting Evaluation...\n")

for i, data in enumerate(test_data, start=1):
    start_time = time.time()
    cpu_start = psutil.cpu_percent(interval=None)
    mem_start = psutil.virtual_memory().percent

    response = model.generate_content(data["query"])
    response_text = response.text.strip()

    cpu_end = psutil.cpu_percent(interval=None)
    mem_end = psutil.virtual_memory().percent
    latency = time.time() - start_time
    total_latency += latency

    # Measure similarity
    expected_emb = embedder.encode(data["expected"], convert_to_tensor=True)
    response_emb = embedder.encode(response_text, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(expected_emb, response_emb).item()

    # Accuracy threshold
    correct = 1 if similarity >= 0.7 else 0
    accurate_count += correct

    results.append({
        "Query": data["query"],
        "Expected": data["expected"],
        "Response": response_text,
        "Similarity": round(similarity, 3),
        "Correct": correct,
        "Latency(s)": round(latency, 2),
        "CPU(%)": cpu_end - cpu_start,
        "Memory(%)": mem_end - mem_start
    })

# Summary metrics
accuracy = accurate_count / len(test_data) * 100
avg_latency = total_latency / len(test_data)

print(f"\n✅ Accuracy: {accuracy:.2f}%")
print(f"⚙️ Average Latency: {avg_latency:.2f}s")

# Save to CSV for proof
with open("evaluation_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\n📊 Results saved to 'evaluation_results.csv'")
