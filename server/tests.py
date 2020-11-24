# TODO: Refactor with pytests.
import asyncio
from matcher import AssociationsMatcher

words = [
    "productiv",
    "production",
    "adventure",
    "mentorize",
    "billing",
    "consider",
    "consideration", # Get high score because there are many forms of the same word (consider).
    "forewarned",
    "predominantly",
    "misgivings",
    "gut",
    "surpass",
    "evolute",
    "obsolete",
    "endorsement",
    "deprivation",
    "pavement",
    "soreness",
    "annexation",
    "woos",
    "exemption",
    "subtle"
]

import time
print(time.ctime())

async def test():
    for target_word in words:
        match = AssociationsMatcher(target_word, associations_limit=10)
        await match.generate_possible_splits()
        print(time.ctime())
        print(f"{target_word} {match.most_associative}")


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
loop.close()