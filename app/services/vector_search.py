"""
AI Semantic Taxonomy Classifier Engine with AI Core Head Noun & Language Preprocessing.
Preprocesses product descriptions to extract the primary Head Noun and detect language (DE/EN),
weighting the core product noun at 15.0x prior to vector search against official eCl@ss 7.1 categories.
"""

import re
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from app.data.eclass_db import ECLASS_7_1_DATABASE
from app.models.catalog_schema import EClassMatch

STOP_WORDS = {
    "versch", "sorten", "verschiedene", "inkl", "ca", "max", "min", "abb", "pos",
    "art", "nr", "stück", "stk", "pack", "beutel", "flasche", "dose", "schale",
    "mit", "und", "oder", "aus", "für", "im", "in", "von", "zu", "auf"
}

KNOWN_BRANDS = {
    "ehrmann", "jacobs", "söhnlein", "danone", "coppenrath", "philadelphia",
    "persil", "nutella", "gerolsteiner", "paulaner", "blaubrand", "din", "iso"
}


def extract_core_product_head_noun_and_language(title: str) -> Tuple[str, str]:
    """
    AI Preprocessing Layer:
    1. Detects description language ('de' vs 'en').
    2. Isolates the Core Head Noun (e.g., 'Ehrmann Almighurt Joghurt gekühlt' -> 'joghurt').
    """
    text = title.strip()
    
    # 1. Detect language
    lang = "de" if re.search(r'[äöüß]|gekühlt|gemahlen|mit|oder|aus|für|ohne|trocken|waschmittel', text, re.I) else "en"

    # 2. Filter out brands, attributes, units, package descriptions
    clean = re.sub(r'^(ehrmann|jacobs|söhnlein|danone|coppenrath|philadelphia|persil|nutella|gerolsteiner|paulaner|blaubrand®?|din\s*\d+|iso\s*\d+)\b', '', text, flags=re.I)
    clean = re.sub(r'\b(gekühlt|gemahlen|trocken|alkoholfrei|tiefgekühlt|versch|sorten|ohne|knochen|kl\.\s*i|mit|bifidus-kulturen|fett|milchanteil|0,75|500g|100g|200g|1kg|schale|beutel|20x0,5|6x1,5|liter|zzgl|pfand)\b', '', clean, flags=re.I)
    
    words = [w.lower() for w in re.findall(r'\b[a-zA-ZäöüÄÖÜß]{3,}\b', clean) if w.lower() not in KNOWN_BRANDS and w.lower() not in STOP_WORDS]
    
    core_noun = words[-1] if words else (title.split()[0].lower() if title.split() else "product")
    
    return core_noun, lang


def _extract_word_and_subword_tokens(text: str) -> List[Tuple[str, float]]:
    """Extracts normalized word tokens and character subword roots with weight factors."""
    text_clean = text.lower()
    raw_words = re.findall(r'\b[a-z0-9äöüß]{2,}\b', text_clean)

    tokens_with_weights = []

    for word in raw_words:
        if word in STOP_WORDS or len(word) < 2:
            continue

        tokens_with_weights.append((word, 5.0))

        if len(word) >= 5:
            for i in range(len(word) - 3):
                sub = word[i:i+4]
                if sub not in STOP_WORDS:
                    tokens_with_weights.append((sub, 1.0))

    return tokens_with_weights


class VectorSearchEngine:
    def __init__(self):
        self.categories = ECLASS_7_1_DATABASE
        self._build_index()

    def _build_index(self):
        """Constructs semantic document-term matrix from official eCl@ss category names and descriptions."""
        self.vocabulary: Dict[str, int] = {}
        category_weighted_tokens = []

        for cat in self.categories:
            combined_semantic_text = f"{cat['name']} {cat['segment']} {cat['main_group']} {cat['description']}"
            weighted_tokens = _extract_word_and_subword_tokens(combined_semantic_text)
            category_weighted_tokens.append(weighted_tokens)

            for token, _ in weighted_tokens:
                if token not in self.vocabulary:
                    self.vocabulary[token] = len(self.vocabulary)

        vocab_size = max(len(self.vocabulary), 1)
        num_cats = len(self.categories)

        self.matrix = np.zeros((num_cats, vocab_size), dtype=np.float32)

        for cat_idx, weighted_tokens in enumerate(category_weighted_tokens):
            cat = self.categories[cat_idx]
            cat_name_lower = cat["name"].lower()

            for token, weight in weighted_tokens:
                col_idx = self.vocabulary[token]
                final_weight = weight
                if token in cat_name_lower and len(token) >= 3:
                    final_weight += 8.0
                self.matrix[cat_idx, col_idx] += final_weight

        norms = np.linalg.norm(self.matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.matrix_norm = self.matrix / norms

    def search(self, title: str, description: str = "", specs: Dict[str, str] = None, keywords: List[str] = None, top_k: int = 4) -> List[EClassMatch]:
        """
        AI Preprocessor Layer isolates Core Head Noun and language before computing vector similarity.
        """
        if specs is None:
            specs = {}
        if keywords is None:
            keywords = []

        # 1. AI Preprocessor Layer: Extract Core Head Noun and detect language
        core_noun, lang = extract_core_product_head_noun_and_language(title)

        query_text = f"{title} {description} {' '.join(keywords)} {' '.join(specs.values())}"
        query_weighted_tokens = _extract_word_and_subword_tokens(query_text)

        # 2. Boost Core Head Noun with 15.0x Primary Vector Weight
        if core_noun:
            query_weighted_tokens.append((core_noun, 15.0))
            if len(core_noun) >= 4:
                query_weighted_tokens.append((core_noun[:4], 5.0))

        vocab_size = max(len(self.vocabulary), 1)
        query_vec = np.zeros((1, vocab_size), dtype=np.float32)

        matched_terms_per_cat: Dict[int, List[str]] = {i: [] for i in range(len(self.categories))}

        for token, weight in query_weighted_tokens:
            if token in self.vocabulary:
                col_idx = self.vocabulary[token]
                query_vec[0, col_idx] += weight
                for cat_idx in range(len(self.categories)):
                    if self.matrix[cat_idx, col_idx] > 0 and len(token) >= 3:
                        matched_terms_per_cat[cat_idx].append(token)

        q_norm = np.linalg.norm(query_vec)
        if q_norm == 0:
            q_norm = 1.0
        query_vec_norm = query_vec / q_norm

        # Compute Cosine Similarity Vector
        similarities = np.dot(self.matrix_norm, query_vec_norm.T).flatten()

        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            cat = self.categories[idx]
            raw_score = float(similarities[idx])
            confidence = min(99.0, max(45.0, round((raw_score * 1.8 + 0.35) * 100, 1)))

            unique_matches = sorted(list(set(matched_terms_per_cat[idx])), key=lambda x: len(x), reverse=True)[:5]

            results.append(EClassMatch(
                code=cat["code"],
                name=cat["name"],
                segment=cat["segment"],
                main_group=cat["main_group"],
                description=cat["description"],
                confidence=confidence,
                matched_terms=unique_matches
            ))

        return results


# Global singleton instance
vector_engine = VectorSearchEngine()
