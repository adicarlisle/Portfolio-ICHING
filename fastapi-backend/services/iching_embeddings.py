import numpy as np
from typing import List, Dict, Tuple
import os
import pickle
from tqdm import tqdm

class ICHingEmbeddingService:
    def __init__(self, glove_path="./glove/glove.6B.300d.txt"):
        # Initialize with 64 I Ching hexagrams with their names and Unicode characters
        self.hexagrams = [
            # 1-8
            (1, "Creative", "creative", "䷀"), (2, "Receptive", "receptive", "䷁"), 
            (3, "Difficulty at the Beginning", "difficulty", "䷂"), (4, "Youthful Folly", "youthful", "䷃"),
            (5, "Waiting", "waiting", "䷄"), (6, "Conflict", "conflict", "䷅"),
            (7, "The Army", "army", "䷆"), (8, "Holding Together", "holding", "䷇"),
            # 9-16
            (9, "Small Taming", "small", "䷈"), (10, "Treading", "treading", "䷉"),
            (11, "Peace", "peace", "䷊"), (12, "Standstill", "standstill", "䷋"),
            (13, "Fellowship", "fellowship", "䷌"), (14, "Great Possession", "possession", "䷍"),
            (15, "Modesty", "modesty", "䷎"), (16, "Enthusiasm", "enthusiasm", "䷏"),
            # 17-24
            (17, "Following", "following", "䷐"), (18, "Work on the Decayed", "work", "䷑"),
            (19, "Approach", "approach", "䷒"), (20, "Contemplation", "contemplation", "䷓"),
            (21, "Biting Through", "biting", "䷔"), (22, "Grace", "grace", "䷕"),
            (23, "Splitting Apart", "splitting", "䷖"), (24, "Return", "return", "䷗"),
            # 25-32
            (25, "Innocence", "innocence", "䷘"), (26, "Great Taming", "taming", "䷙"),
            (27, "Nourishment", "nourishment", "䷚"), (28, "Great Preponderance", "preponderance", "䷛"),
            (29, "The Abysmal", "abysmal", "䷜"), (30, "The Clinging", "clinging", "䷝"),
            (31, "Influence", "influence", "䷞"), (32, "Duration", "duration", "䷟"),
            # 33-40
            (33, "Retreat", "retreat", "䷠"), (34, "Great Power", "power", "䷡"),
            (35, "Progress", "progress", "䷢"), (36, "Darkening of the Light", "darkening", "䷣"),
            (37, "The Family", "family", "䷤"), (38, "Opposition", "opposition", "䷥"),
            (39, "Obstruction", "obstruction", "䷦"), (40, "Deliverance", "deliverance", "䷧"),
            # 41-48
            (41, "Decrease", "decrease", "䷨"), (42, "Increase", "increase", "䷩"),
            (43, "Breakthrough", "breakthrough", "䷪"), (44, "Coming to Meet", "meeting", "䷫"),
            (45, "Gathering Together", "gathering", "䷬"), (46, "Pushing Upward", "pushing", "䷭"),
            (47, "Exhaustion", "exhaustion", "䷮"), (48, "The Well", "well", "䷯"),
            # 49-56
            (49, "Revolution", "revolution", "䷰"), (50, "The Cauldron", "cauldron", "䷱"),
            (51, "The Arousing", "arousing", "䷲"), (52, "Keeping Still", "keeping", "䷳"),
            (53, "Development", "development", "䷴"), (54, "The Marrying Maiden", "marrying", "䷵"),
            (55, "Abundance", "abundance", "䷶"), (56, "The Wanderer", "wanderer", "䷷"),
            # 57-64
            (57, "The Gentle", "gentle", "䷸"), (58, "The Joyous", "joyous", "䷹"),
            (59, "Dispersion", "dispersion", "䷺"), (60, "Limitation", "limitation", "䷻"),
            (61, "Inner Truth", "truth", "䷼"), (62, "Small Exceeding", "small_exceeding", "䷽"),
            (63, "After Completion", "completion", "䷾"), (64, "Before Completion", "incompletion", "䷿")
        ]
        
        # Create lookup dictionaries
        self.hexagram_lookup = {hex_data[2]: (hex_data[0], hex_data[1], hex_data[3]) for hex_data in self.hexagrams}
        
        # Load GloVe embeddings
        self.glove_embeddings = self._load_glove_embeddings(glove_path)
        
        # Initialize hexagram vectors using GloVe
        self.hexagram_vectors = self._initialize_hexagram_vectors()
        
        # Default vector dimension
        self.vector_dim = 300
        
    def _load_glove_embeddings(self, glove_path: str) -> Dict[str, np.ndarray]:
        """Load pre-trained GloVe embeddings"""
        cache_path = glove_path + ".cache.pkl"
        
        # Check if we have a cached version
        if os.path.exists(cache_path):
            print("Loading cached GloVe embeddings...")
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        
        # Check if GloVe file exists
        if not os.path.exists(glove_path):
            print(f"GloVe file not found at {glove_path}. Using random embeddings as fallback.")
            return {}
        
        print("Loading GloVe embeddings from file...")
        embeddings = {}
        
        with open(glove_path, 'r', encoding='utf-8') as f:
            for line in tqdm(f, desc="Loading GloVe"):
                values = line.split()
                word = values[0]
                vector = np.array(values[1:], dtype='float32')
                embeddings[word] = vector
        
        # Cache the embeddings
        print("Caching GloVe embeddings...")
        with open(cache_path, 'wb') as f:
            pickle.dump(embeddings, f)
        
        return embeddings
    
    def _get_word_vector(self, word: str) -> np.ndarray:
        """Get GloVe vector for a word, with fallback for OOV words"""
        word_lower = word.lower()
        
        if word_lower in self.glove_embeddings:
            return self.glove_embeddings[word_lower]
        
        # For out-of-vocabulary words, use average of character-level embeddings
        # or random initialization
        return np.random.randn(self.vector_dim) * 0.1
    
    def _initialize_hexagram_vectors(self) -> Dict[int, np.ndarray]:
        """Initialize hexagram vectors using GloVe embeddings"""
        vectors = {}
        
        # Extended keywords for each hexagram to capture more semantic meaning
        hexagram_keywords = {
            1: ["creative", "heaven", "strong", "initiating", "yang", "father"],
            2: ["receptive", "earth", "yielding", "responsive", "yin", "mother"],
            3: ["difficulty", "beginning", "sprouting", "initial", "struggle"],
            4: ["youthful", "folly", "inexperience", "learning", "student"],
            5: ["waiting", "patience", "nourishment", "rain", "delay"],
            6: ["conflict", "opposition", "litigation", "arguing", "dispute"],
            7: ["army", "collective", "discipline", "organization", "leadership"],
            8: ["holding", "together", "unity", "alliance", "cooperation"],
            9: ["small", "taming", "restraint", "gentle", "accumulation"],
            10: ["treading", "conduct", "careful", "tiger", "danger"],
            11: ["peace", "harmony", "prosperity", "communication", "balance"],
            12: ["standstill", "stagnation", "obstruction", "blocked", "separation"],
            13: ["fellowship", "community", "people", "harmony", "cooperation"],
            14: ["possession", "great", "wealth", "abundance", "sovereignty"],
            15: ["modesty", "humility", "equalizing", "mountain", "earth"],
            16: ["enthusiasm", "thunder", "movement", "inspiration", "music"],
            17: ["following", "adapting", "flexibility", "influence", "leadership"],
            18: ["work", "decay", "corruption", "restoration", "repair"],
            19: ["approach", "nearing", "advance", "spring", "growth"],
            20: ["contemplation", "viewing", "observation", "wind", "example"],
            21: ["biting", "through", "justice", "punishment", "clarity"],
            22: ["grace", "beauty", "form", "ornament", "mountain"],
            23: ["splitting", "apart", "decay", "mountain", "stripping"],
            24: ["return", "turning", "renewal", "winter", "solstice"],
            25: ["innocence", "unexpected", "natural", "spontaneous", "heaven"],
            26: ["great", "taming", "restraint", "potential", "mountain"],
            27: ["nourishment", "jaws", "nutrition", "caring", "mountain"],
            28: ["preponderance", "great", "excess", "critical", "pressure"],
            29: ["abysmal", "water", "danger", "pit", "flowing"],
            30: ["clinging", "fire", "clarity", "dependence", "light"],
            31: ["influence", "wooing", "attraction", "stimulation", "lake"],
            32: ["duration", "perseverance", "endurance", "marriage", "thunder"],
            33: ["retreat", "withdrawal", "yielding", "mountain", "heaven"],
            34: ["power", "great", "strength", "vigor", "thunder"],
            35: ["progress", "advancing", "prosperity", "sunrise", "fire"],
            36: ["darkening", "light", "injury", "hiding", "adversity"],
            37: ["family", "clan", "home", "relationships", "wind"],
            38: ["opposition", "contradiction", "misunderstanding", "fire", "lake"],
            39: ["obstruction", "difficulty", "impediment", "water", "mountain"],
            40: ["deliverance", "release", "liberation", "thunder", "rain"],
            41: ["decrease", "loss", "restraint", "mountain", "lake"],
            42: ["increase", "benefit", "augmenting", "wind", "thunder"],
            43: ["breakthrough", "determination", "resolution", "lake", "heaven"],
            44: ["meeting", "encounter", "temptation", "heaven", "wind"],
            45: ["gathering", "assembly", "accumulation", "lake", "earth"],
            46: ["pushing", "ascending", "growth", "earth", "wood"],
            47: ["exhaustion", "oppression", "adversity", "lake", "water"],
            48: ["well", "source", "unchanging", "water", "wood"],
            49: ["revolution", "molting", "change", "lake", "fire"],
            50: ["cauldron", "vessel", "nourishment", "fire", "wood"],
            51: ["arousing", "shock", "thunder", "movement", "earthquake"],
            52: ["keeping", "still", "meditation", "mountain", "rest"],
            53: ["development", "gradual", "progress", "wind", "mountain"],
            54: ["marrying", "maiden", "subordinate", "thunder", "lake"],
            55: ["abundance", "fullness", "peak", "thunder", "fire"],
            56: ["wanderer", "traveler", "stranger", "fire", "mountain"],
            57: ["gentle", "penetrating", "wind", "influence", "wood"],
            58: ["joyous", "lake", "pleasure", "satisfaction", "marsh"],
            59: ["dispersion", "dissolution", "scattering", "wind", "water"],
            60: ["limitation", "restraint", "articulation", "water", "lake"],
            61: ["truth", "inner", "sincerity", "wind", "lake"],
            62: ["small", "exceeding", "preponderance", "thunder", "mountain"],
            63: ["completion", "after", "equilibrium", "water", "fire"],
            64: ["incompletion", "before", "transition", "fire", "water"]
        }
        
        for hex_id, hex_name, hex_key, hex_unicode in self.hexagrams:
            # Get keywords for this hexagram
            keywords = hexagram_keywords.get(hex_id, [hex_key])
            
            # Get vectors for all keywords
            keyword_vectors = []
            for keyword in keywords:
                words = keyword.split()
                word_vectors = [self._get_word_vector(w) for w in words]
                if word_vectors:
                    keyword_vectors.append(np.mean(word_vectors, axis=0))
            
            # Average all keyword vectors for this hexagram
            if keyword_vectors:
                vectors[hex_id] = np.mean(keyword_vectors, axis=0)
            else:
                vectors[hex_id] = np.random.randn(self.vector_dim) * 0.1
                
        return vectors
    
    def process_query(self, query: str) -> Tuple[List[float], List[Dict]]:
        """
        Process a query string using GloVe embeddings and return both 
        the average vector embedding and the calculated hexagram set
        """
        # Tokenize query
        words = query.lower().split()
        
        # Get vectors for each word
        word_vectors = []
        for word in words:
            vector = self._get_word_vector(word)
            word_vectors.append(vector)
        
        # Calculate query vector as average of word vectors
        if word_vectors:
            query_vector = np.mean(word_vectors, axis=0)
        else:
            query_vector = np.zeros(self.vector_dim)
        
        # Calculate hexagram set based on vector similarity
        hexagram_set = self._calculate_hexagram_set(query_vector)
        
        return query_vector.tolist(), hexagram_set
    
    def _calculate_hexagram_set(self, query_vector: np.ndarray, top_k: int = 6) -> List[Dict]:
        """
        Calculate the most relevant hexagrams based on cosine similarity
        Returns top K hexagrams with their similarity scores
        """
        similarities = []
        
        # Normalize query vector
        query_norm = np.linalg.norm(query_vector)
        if query_norm > 0:
            query_vector = query_vector / query_norm
        
        # Calculate cosine similarity with each hexagram
        for hex_id, hex_vector in self.hexagram_vectors.items():
            # Normalize hexagram vector
            hex_norm = np.linalg.norm(hex_vector)
            if hex_norm > 0:
                hex_vector_norm = hex_vector / hex_norm
            else:
                hex_vector_norm = hex_vector
            
            # Cosine similarity (already normalized)
            similarity = np.dot(query_vector, hex_vector_norm)
            
            # Get hexagram info
            hex_data = next(h for h in self.hexagrams if h[0] == hex_id)
            hex_name = hex_data[1]
            hex_unicode = hex_data[3]
            
            similarities.append({
                "hexagram_id": hex_id,
                "hexagram_name": hex_name,
                "hexagram_unicode": hex_unicode,
                "score": float(similarity)
            })
        
        # Sort by similarity score and return top K
        similarities.sort(key=lambda x: x["score"], reverse=True)
        
        # Normalize scores to 0-1 range (they should already be close due to cosine similarity)
        # But ensure they're in proper range
        if similarities:
            # Apply softmax-like transformation for better score distribution
            scores = np.array([s["score"] for s in similarities[:top_k]])
            exp_scores = np.exp(scores * 2)  # Scale factor for better distribution
            normalized_scores = exp_scores / np.sum(exp_scores)
            
            for i, score in enumerate(normalized_scores):
                similarities[i]["score"] = float(score)
        
        return similarities[:top_k]