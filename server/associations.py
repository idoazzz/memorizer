"""Finding word sound-like associations using Datamuse api."""
import asyncio

import datamuse
from statistics import mean
from abc import abstractmethod
import requests_async as requests

class Association:
    """Single word association.
    
    Attributes:
        name (str): Word association.
        score (str): Similarity score.
        frequency (float): How frequent this word in the english language.
        definitions (list): Word definitions.
    Notes:
        * The value is the number of times the word (or multi-word phrase) 
        occurs per million words of English text according to Google Books 
        Ngrams.
        * Similarity and frequency get normalized.
    """
    MAX_SIMILARITY = 100 
    MAX_FREQUENCY = 11000  # "that" word
    SIMILARITY_WEIGHT = 0.8
    FREQUENCY_WEIGHT = 1 - SIMILARITY_WEIGHT
    
    def __init__(self, word, score, has_definition, frequency=MAX_FREQUENCY):
        self.name = word
        self.has_definition = has_definition
        self.frequency = frequency / self.MAX_FREQUENCY
        self.similarity_score = score / self.MAX_SIMILARITY
    
    def __repr__(self):
        return f"({self.name}:{self.frequency}, {self.similarity_score})"

    @property
    def grade(self):
        """Association weighted grade."""
        return self.SIMILARITY_WEIGHT * self.similarity_score + \
            self.FREQUENCY_WEIGHT * self.frequency 

class WordAssociations:
    """Specific word associations holder.
    
    Attributes:
        word (str): Target word.
        limit (number): Limit of the returned associations.
        _associations (list): List of Associations objects.
    """
    def __init__(self, word, associations, limit):
        self.word = word
        self.limit = limit
        self._associations = associations

    @property
    def associations(self):
        return self._associations[:self.limit]

    @property
    def grade(self):
         return sum([word.grade for word in self._associations])
    
    def to_dictionary(self):
        return {
            "word": self.word,
            "associations": self.associations,
        }
    
async def fetch_associations(word, limit):
    """Generate associations from Datamuse api.
    
    * Get sound-like words.
    * Sort them by frequency.
    * Calculate the grade of the associations.
    """
    response = await datamuse.get_soundlike_words(word)
    associations = get_formatted_response(response)
    
    # Sort by associations frequency.
    associations.sort(key=lambda association: association.frequency,
                            reverse=True)
    
    return WordAssociations(word, associations, limit)

def get_formatted_response(response):
        return [Association(
                    word=data.word, 
                    score=int(data.score), 
                    has_definition="defs" in data,
                    frequency=datamuse.extract_frequency(data.tags)) 
                for data in response]
        
def calculate_associations_grade(associations):
    """Calculate a grade for all given associations."""
    return sum([word.grade for word in associations])

async def get_associations(words, limit):
    """Search associations asynchronously.
    
    Returns:
        list. List of WordAssociations objects.
    """
    tasks = [asyncio.create_task(fetch_associations(word, limit))
             for word in words]
    words_associations = await asyncio.gather(*tasks)
    return words_associations
