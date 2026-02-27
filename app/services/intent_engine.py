from typing import Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.intent_registry import INTENT_REGISTRY


class IntentEngine:
    def __init__(self):
        self.intent_names = []
        self.example_texts = []

        # Flatten examples from registry
        for intent, data in INTENT_REGISTRY.items():
            for example in data["examples"]:
                self.intent_names.append(intent)
                self.example_texts.append(example)

        # Vectorizer configuration
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2)
        )

        self.example_vectors = self.vectorizer.fit_transform(self.example_texts)

        # -------- SYSTEM INTENT KEYWORDS --------
        # These bypass similarity threshold for stability
        self.system_keywords = [
            "hello",
            "hi",
            "hey",
            "help",
            "what can you do",
            "how can you help",
            "what are your capabilities"
        ]

    def classify(self, transcript: str) -> Tuple[str, float]:
        transcript_lower = transcript.lower().strip()

        # -------- SYSTEM INTENT SHORT-CIRCUIT --------
        for keyword in self.system_keywords:
            if keyword in transcript_lower:
                return "greeting", 1.0

        # -------- TF-IDF CLASSIFICATION --------
        transcript_vector = self.vectorizer.transform([transcript])
        similarities = cosine_similarity(transcript_vector, self.example_vectors)

        best_index = similarities.argmax()
        best_score = similarities[0][best_index]
        best_intent = self.intent_names[best_index]

        return best_intent, float(best_score)


# Singleton instance (loaded once at startup)
intent_engine = IntentEngine()