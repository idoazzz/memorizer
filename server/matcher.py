"""Match best associations to given word by splitting."""
import asyncio

from statistics import mean
from attrdict import AttrDict
from hyphenate import hyphenate_word
from associations import AssociationsGenerator

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
    
    async def add_splits_pair(self, first, second):
        """Add new splits pair asynchronously."""
        first_task = asyncio.create_task(first.generate_associations())
        second_task = asyncio.create_task(second.generate_associations())
        
        await asyncio.gather(first_task, second_task)
                                
        grades = (first.grade, second.grade)
        grades_range = max(*grades) - min(*grades)
        grades_mean = mean([first.grade, second.grade])

        self.possible_splits.append(AttrDict({
            "splits": [first, second,],
            "grade": grades_mean * (1 / (grades_range)),
        }))

    
    async def generate_possible_splits(self):
        # Handle short words (don't split - only one syllable).
        if len(hyphenate_word(self.word)) == 1:
            word_association = AssociationsGenerator(self.word)
            await word_association.generate_associations()
            self.possible_splits.append(AttrDict({
                "splits": [word_association,],
                "grade": word_association.grade,
            }))
            return

        tasks = []
        
        # Iterate each combination of the word and calculate associations grade.
        for split_index in range(2, len(self.word)-1):
            first_split = self.word[:split_index]
            second_split = self.word[split_index:]
            
            first = AssociationsGenerator(first_split)
            second = AssociationsGenerator(second_split)
            tasks.append(asyncio.create_task(self.add_splits_pair(first, second)))
            
        await asyncio.gather(*tasks)
        
    
    @property
    def most_associative(self):
        """Get most associative splits."""
        max_graded_split = self.possible_splits[0]
        for split in self.possible_splits:
            if split.grade > max_graded_split.grade:
                max_graded_split = split
        return max_graded_split