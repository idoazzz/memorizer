"""Match best associations to given word by auto splitting."""
import asyncio

from statistics import mean
from hyphenate import hyphenate_word
from .associations import get_associations

MIN_WORD_LENGTH = 5
MIN_ASSOCIATION_LENGTH = 3


async def get_auto_splits_associations(word, limit):
    """Get the most associative splits automatically.
    
    Args:
        word (str): Target words.
        limit (int): Associations limit.
    """
    tasks = []
    max_graded_pair = 0
    most_associative_pair = None

    # Handle short words (don't split - only one syllable or len <=
    # MIN_WORD_LENGTH).
    if len(hyphenate_word(word)) == 1 or len(word) < MIN_WORD_LENGTH:
        result = await get_associations([word], limit)
        return result

    # Get associations of all word splits combinations async.
    for split_index in range(MIN_ASSOCIATION_LENGTH,
                             len(word) - MIN_ASSOCIATION_LENGTH + 1):
        tasks.append(
            asyncio.create_task(
                get_associations(
                    [word[:split_index], word[split_index:]],
                    limit=limit),
            )
        )
    pairs_results = await asyncio.gather(*tasks)

    for pair in pairs_results:
        current_grade = calculate_splits_grade(*[x.grade for x in pair])
        if current_grade > max_graded_pair:
            max_graded_pair = current_grade
            most_associative_pair = pair
    return most_associative_pair


def calculate_splits_grade(*grades):
    """Give a grade for word splits."""
    grades_mean = mean(grades)
    grades_range = max(*grades) - min(*grades)
    return grades_mean * (
                1 / grades_range) if grades_range != 0 else grades_mean
