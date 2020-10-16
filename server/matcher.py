"""Match best associations to given word by splitting."""
from statistics import mean
from attrdict import AttrDict
from hyphenate import hyphenate_word
from associations import WordAssociations

class AssociationsMatcher:
    """Matching to specific word associations.
    
    Matcher search for the most associative word split. For each split of the
    word will be attached most compatible associations.
    
    Attributes:
        word (str): Given word.
        possible_splits (list): Possible splits with associations.
    """
    def __init__(self, word):
        self.word = word
        self.possible_splits = []
        self.generate_possible_splits()
    
    def generate_possible_splits(self):
        # Handle short words (don't split - only one syllable).
        if len(hyphenate_word(self.word)) == 1:
            word_associations = WordAssociations(self.word)
            self.possible_splits.append(AttrDict({
                "splits": [word_associations,],
                "grade": word_associations.grade,
            }))
            return

        # Iterate each combination of the word and calculate associations grade.
        for split_index in range(2, len(self.word)-1):
            first = WordAssociations(self.word[:split_index])
            second = WordAssociations(self.word[split_index:])
            grades = (first.grade, second.grade)
            grades_range = max(*grades) - min(*grades)
            grades_mean = mean([first.grade, second.grade])

            self.possible_splits.append(AttrDict({
                "splits": [first, second,],
                "grade": grades_mean * (1 / (grades_range)),
            }))

    @property
    def most_associative(self):
        """Get most associative splits."""
        max_graded_split = self.possible_splits[0]
        for split in self.possible_splits:
            if split.grade > max_graded_split.grade:
                max_graded_split = split
        return max_graded_split