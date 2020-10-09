"""Finding word sound-like associations using datamuse api."""
import requests
from statistics import mean
from attrdict import AttrDict

class Association:
    """Single word association.
    
    Attributes:
        name (str): Word association.
        score (str): Similarity score.
        frequency (float): How frequent this word in the english language.
        
    Notes:
        The value is the number of times the word (or multi-word phrase) occurs 
        per million words of English text according to Google Books Ngrams.
    """
    def __init__(self, word, score, frequency):
        self.name = word
        self.score = score
        self.frequency = frequency
        
    def __repr__(self):
        return f"({self.name}:{self.frequency}, {self.score})"
        
class WordAssociations:
    """Word associations from Datamuse api.
    
    Attributes:
        word (str): Target word.
        grade (float): All associations grade. 
        associations (list): List of associations.
    """
    API_BASE_URL = "https://api.datamuse.com/words"

    def __init__(self, word, limit=10):
        self.word = word
        self.grade = None
        self.limit = limit
        self._associations = None
        self.generate_associations()
        
    def generate_associations(self):
        """Generate associations from Datamust api.
        
        * Get sound-like words.
        * Sort them by frequency.
        * Limit the results.
        * Calculate the grade of the associations.
        """
        response = requests.get(f"{self.API_BASE_URL}", params={
            "sl": self.word,    # Sound-like.
            "md": "f"           # Stands for frequency metadata.
        }).json()

        response = map(AttrDict, response)

        # Create formatted frequency list.
        self._associations = [Association(word=data.word, score=int(data.score), 
        frequency=self.extract_frequency(data.tags)) for data in response]
        
        # Sort by associations frequency.
        self._associations.sort(key=lambda association: association.frequency,
                               reverse=True)

        # Calculate total associations grade.
        self.grade = self.calculate_associations_grade(self.associations)
    
    @property
    def associations(self):
        return self._associations[:self.limit]

    def calculate_associations_grade(self, associations):
        scores_sum = sum(map(lambda word: word.score / 100, self.associations))
        frequencies = sum(map(lambda word: word.frequency * word.score / 100, 
                              self.associations))
        # TODO: think about better weighted mean.
        return (frequencies / scores_sum)        

    @staticmethod
    def extract_frequency(frequency):
        """Extract nemeric frequency from Datamuse frequency format."""
        return float(frequency[0][2:])
    
    def __repr__(self):
        return f"{self.word}: ({self.grade}, {self.associations})"
        
        
class AssociationsMatcher:
    """Matching to specific word associations.
    
    Matcher search for the most associative word split. For each split of the
    word will be attached most compatible associations.
    """
    def __init__(self, word):
        self.word = word
        self.possible_splits = []
        self.debug = []
        self.generate_possible_splits()
    
    def generate_possible_splits(self):
        if len(self.word) <= 3:
            word_associations = WordAssociations(self.word)
            self.possible_splits.append(AttrDict({
                "first": word_associations,
                "second": None,
                "grade": word_associations.grade,
            }))
            return

        for split_index in range(2, len(self.word)-1):
            first = WordAssociations(self.word[:split_index])
            second = WordAssociations(self.word[split_index:])
            split_grade = min([first.grade, second.grade]) * (1/(max(first.grade, second.grade) - min(first.grade, second.grade)))  # TODO: Refactor
            self.possible_splits.append(AttrDict({
                "first": first,
                "second": second,
                "grade": split_grade,
            }))
            # print(split_grade)

    @property
    def most_associative(self):
        max_graded_split = self.possible_splits[0]
        for split in self.possible_splits:
            if split.grade > max_graded_split.grade:
                max_graded_split = split
        return max_graded_split
    
words = [
    "misgivings",
    "gut",
    "surpass",
    "evolute",
    "obsolete",
    "endorsement",
    "deprivation",
    "pavement",
    "forewarned",
    "soreness",
    "annexation",
    "woos",
    "predominantly",
    "exemption",
    "subtle"
]
for target_word in words:
    match = AssociationsMatcher(target_word).most_associative
    if match.second is None:
        print(f"{match.first.word} {match.first.grade} {match.first.associations}")        
    else:
        print(f"{match.first.word} {match.first.grade} {match.first.associations}") 
        print(f"{match.second.word} {match.first.grade} {match.second.associations}")
    print()