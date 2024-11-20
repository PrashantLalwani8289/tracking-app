import google.generativeai as genai

from app.config import env_variables


class GPT:
    def __init__(self):
        self.api_key = "AIzaSyASbqO5mGhlq0nViOEGQA3mK4EnRgLfNXE"

    def query(self, input: str) -> list:
        genai.configure(api_key=self.api_key)
        prompt = f"""
        {{
            "task": "Generate a detailed travel guide for a specific destination based on the provided input.",
            "instruction": "Write a comprehensive travel guide for the given destination. The guide should be engaging and provide essential information for travelers. Use a professional and inviting tone to make the guide both informative and inspiring.",
            "input_destination": "{input}",
            "response_requirements": {{
                "title": "Create a compelling title for the travel guide that captures the essence of the destination.",
                "introduction": "Provide an engaging introduction that highlights why the destination is special or worth visiting.",
                "tips": "List travel tips specific to the destination, including best times to visit, local customs, and essential advice.",
                "adventure": "Describe adventurous activities and exciting experiences that travelers can enjoy at the destination.",
                "accommodationReview": "Offer an overview of accommodation options available at the destination, including budget and luxury choices.",
                "destinationGuides": "Provide a guide to the must-visit landmarks, attractions, and hidden gems of the destination.",
                "customerReview": "Summarize a fictional customer review that captures the general experience of a visitor to the destination.",
                "travelChallenges": "Highlight any travel challenges or considerations, such as weather conditions, accessibility, or cultural nuances.",
                "conclusion": "Finish with a positive conclusion that encourages readers to explore and discover the destination.",
                "latitude": "Include the latitude coordinate of the destination.",
                "longitude": "Include the longitude coordinate of the destination."
            }},
            "output_requirements": {{
                "ignore_generic_text": "If the destination input is generic or unrelated to a specific place (e.g., 'anywhere,' 'nowhere,' 'unknown'), return an empty string with no response.",
                "if_not_related_to_travel": "If the destination is not related to a specific travel location (e.g., random strings, calculations, unrelated topics), return an empty string with no response.",
                "no_additional_text": "Do not include any additional explanations or text or any special symbols like -, * , etc.",
                "keyword_check": "Generate a response only if the destination name includes words that indicate a specific place (e.g., city names, countries, landmarks, regions). Avoid responding to titles that are not clearly related to a travel destination.",
                "coordinates_check": "Only include latitude and longitude if they are relevant and accurate to the destination."
            }},
            "examples": [
                {{
                    "input_destination": "Bali",
                    "response": {{
                        "title": "Discover the Paradise of Bali",
                        "introduction": "Bali, known as the 'Island of the Gods,' is a haven for travelers seeking a blend of culture, adventure, and relaxation. With its stunning beaches, rich cultural heritage, and vibrant nightlife, Bali offers something for every kind of traveler.",
                        "tips": "Visit during the dry season (April to October) for the best weather. Dress modestly when visiting temples, and try local street food for an authentic experience.",
                        "adventure": "Surf the waves in Kuta, hike up Mount Batur for a sunrise view, or explore the lush rice terraces of Ubud.",
                        "accomodationReview": "From luxury resorts in Nusa Dua to budget-friendly hostels in Seminyak, Bali has accommodations to suit all budgets. Consider staying in a traditional Balinese villa for an authentic experience.",
                        "destinationGuides": "Don't miss the iconic Tanah Lot Temple, the Ubud Monkey Forest, and the breathtaking waterfalls of Sekumpul. Explore local markets for unique handicrafts.",
                        "customerReview": "A visitor’s paradise! The beaches were stunning, the locals were friendly, and the food was delicious. I can’t wait to go back!",
                        "travelChallenges": "Beware of the rainy season (November to March), which can bring heavy downpours. Traffic can be hectic, especially in tourist hotspots.",
                        "conclusion": "Whether you're looking for adventure or relaxation, Bali has it all. Pack your bags and get ready to explore this beautiful destination!",
                        "latitude": -8.3405,
                        "longitude": 115.0920
                    }}
                }},
                {{
                    "input_destination": "Paris",
                    "response": {{
                        "title": "Experience the Magic of Paris",
                        "introduction": "Paris, the 'City of Lights,' is a dream destination for many, offering a perfect blend of history, culture, and culinary delights. With its iconic landmarks and romantic ambiance, Paris never ceases to captivate.",
                        "tips": "Visit in spring (April to June) or fall (September to November) to avoid crowds. Learn a few basic French phrases for a warm reception, and book tickets to popular attractions in advance.",
                        "adventure": "Climb the Eiffel Tower, take a cruise on the Seine River, or explore the catacombs for a thrilling experience beneath the city.",
                        "accomodationReview": "Choose from charming boutique hotels in Montmartre to luxury suites with Eiffel Tower views. Paris has a wide range of accommodation options to cater to every traveler.",
                        "destinationGuides": "Explore the Louvre, marvel at the beauty of Notre-Dame Cathedral, and stroll through the artistic streets of Le Marais. Don’t forget to visit the bohemian cafes of Saint-Germain-des-Prés.",
                        "customerReview": "An unforgettable city with stunning architecture and delicious cuisine. I fell in love with the city’s charm and history.",
                        "travelChallenges": "Prepare for a busy atmosphere in popular areas, and be cautious of pickpockets around tourist spots. French bureaucracy can also be a challenge when navigating public services.",
                        "conclusion": "Paris is a city that every traveler should experience at least once. Its timeless elegance and rich culture will leave a lasting impression.",
                        "latitude": 48.8566,
                        "longitude": 2.3522
                    }}
                }}
            ]
        }}
        """
        self.model = genai.GenerativeModel("gemini-pro")
        response = self.model.generate_content(prompt, stream=True)
        data = ""
        for chunk in response:
            data += chunk.text
        print(data)
        return data
