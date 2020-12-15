"""Finding word sound-like associations using Datamuse api."""
import asyncio

from .datamuse import get_soundlike_words, extract_frequency


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
        """Get limited associations."""
        return self._associations[:self.limit]

    @property
    def grade(self):
        """Calculating association grade."""
        return sum([word.grade for word in self._associations])

    def to_dictionary(self):
        """Transform self object to formatted dictionary."""
        return {
            "word": self.word,
            "associations": self.associations,
        }

    def __repr__(self):
        return f"{self.word}"


async def fetch_associations(word, limit):
    """Generate associations from Datamuse api.
    
    * Get sound-like words.
    * Sort them by frequency.
    * Calculate the grade of the associations.
    """
    response = await get_soundlike_words(word)
    associations = get_datamuse_formatted_response(response)

    # Sort by associations frequency.
    associations.sort(key=lambda association: association.frequency,
                      reverse=True)

    return WordAssociations(word, associations, limit)


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


def get_datamuse_formatted_response(response):
    """Get from datamuse response formatted associations list."""
    return [Association(
        word=data.word,
        score=int(data.score),
        has_definition="defs" in data,
        frequency=extract_frequency(data.tags))
        for data in response]
