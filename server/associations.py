"""Finding word sound-like associations using Datamuse api."""
from statistics import mean
from attrdict import AttrDict
from abc import abstractmethod
import requests_async as requests

class Association:
    """Single word association.
    
    Attributes:
        name (str): Word association.
        score (str): Similarity score.
        frequency (float): How frequent this word in the english language.
        
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
    
    def __init__(self, word, score, frequency=MAX_FREQUENCY):
        self.name = word
        self.frequency = frequency / self.MAX_FREQUENCY
        self.similarity_score = score / self.MAX_SIMILARITY
        
    def __repr__(self):
        return f"({self.name}:{self.frequency}, {self.similarity_score})"

    @property
    def grade(self):
        """Association weighted grade."""
        return self.SIMILARITY_WEIGHT * self.similarity_score + \
            self.FREQUENCY_WEIGHT * self.frequency 

class AbstractAssociationsGenerator:
    """Word associations from Datamuse api.
    
    Attributes:
        word (str): Target word.
        grade (float): All associations grade. 
        associations (list): List of associations.
    """
    DEFAULT_LIMIT = 10

    def __init__(self, word, limit=DEFAULT_LIMIT):
        self.word = word
        self.grade = None
        self.limit = limit
        self.associations = None
                 
    @abstractmethod
    async def get_associations(self):
        """Fetching associations from outer source."""
        return NotImplementedError
    
    @abstractmethod    
    def get_formatted_response(self, response):
        """Format the response from outer source."""
        return NotImplementedError
    
    async def generate_associations(self):
        """Generate associations from outer source.
        
        * Get sound-like words.
        * Sort them by frequency.
        * Calculate the grade of the associations.
        """
        self.associations = await self.get_associations()
        
        # Sort by associations frequency.
        self.associations.sort(key=lambda association: association.frequency,
                               reverse=True)

        # Calculate total associations grade.
        self.grade = self.calculate_associations_grade(self.associations)
        
        # Limit associations amount.
        self.associations = self.associations[:self.limit]

    def calculate_associations_grade(self, associations):
        """Calculate a grade for all given associations."""
        return sum([word.grade for word in self.associations])        

    def __repr__(self):
        return f"{self.word}: ({self.grade}, {self.associations})"


class AssociationsGenerator(AbstractAssociationsGenerator):
    """Word associations from Datamuse api.
    
    Attributes:
        word (str): Target word.
        grade (float): All associations grade. 
        associations (list): List of associations.
    """
    API_BASE_URL = "https://api.datamuse.com/words"
    
    def get_formatted_response(self, response):
        response = map(AttrDict, response.json())
        return [Association(
                    word=data.word, 
                    score=int(data.score), 
                    frequency=self.extract_frequency(data.tags)) 
                for data in response]
                 
    
    async def get_associations(self):
        response = await requests.get(f"{self.API_BASE_URL}", params={
            "sl": self.word,    # Sound-like.
            "md": "f"           # Stands for frequency metadata.
        })
        return self.get_formatted_response(response)            
    
    @staticmethod
    def extract_frequency(frequency):
        """Extract nemeric frequency from Datamuse frequency format."""
        return float(frequency[0][2:])