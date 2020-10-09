"""Finding word sound-like associations using datamuse api."""
import requests
from statistics import mean
from attrdict import AttrDict

class Association:
    """Word association representation.
    
    Attributes:
        name: Word association.
        score: Similarity score.
        frequency: How frequent this word in the english language.
        
    Notes:
    The value is the number of times the word (or multi-word phrase) occurs per 
    million words of English text according to Google Books Ngrams.
    """
    def __init__(self, word, score, frequency):
        self.name = word
        self.score = score
        self.frequency = frequency
        
    def __repr__(self):
        return f"{self.name}: {self.frequency}"
        
class WordAssociations:
    API_BASE_URL = "https://api.datamuse.com/words"

    def __init__(self, word):
        self.word = word
        self.grade = None
        self.associations = None
        self.generate_associations()
        
    def generate_associations(self, limit=10):
        response = requests.get(f"{self.API_BASE_URL}", params={
            "sl": self.word,  # Sound-like.
            "md": "f"    # Stands for frequency metadata.
        }).json()
        
        # Create formatted frequency list
        self.associations = [
            Association(word=data["word"],
                        frequency=self.extract_frequency(data["tags"]),
                        score=data["score"]) 
            for data in response]
        
        # Sort by associations frequency
        self.associations.sort(key=lambda association: association.frequency,
                               reverse=True)
        self.associations = self.associations[:limit]
        self.grade = self.calculate_associations_grade(self.associations[:limit])
    
    def calculate_associations_grade(self, associations):
        # TODO: Move to weigthed mean
        frequencies = list(map(lambda word: word.frequency, self.associations))
        return mean(frequencies)        
    
    @staticmethod
    def extract_frequency(frequency):
        """Extract nemeric frequency from datamuse frequency format."""
        return float(frequency[0][2:])
    
    def __repr__(self):
        return f"{self.word}: ({self.grade}, {self.associations})"
        
        
class WordAssociationSplits:
    def __init__(self, word):
        self.word = word
        self.splits = []
        for split_index in range(2, len(target_word)-1):
            first = WordAssociations(target_word[:split_index])
            second = WordAssociations(target_word[split_index:])
            split_grade = mean([first.grade, second.grade])
            self.splits.append(AttrDict({
                "first": first,
                "second": second,
                "grade": split_grade,
            }))
        for x in self.splits:
            print(x.first)
            print(x.second)
            print()
            
    @property
    def most_associative(self):
        max(map(lambda split: split.grade, self.splits))
        
# Pavement
target_word = "pavement"
w = WordAssociationSplits(target_word)
print(w.most_associative)