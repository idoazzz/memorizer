# TODO: Refactor with pytests.
import asyncio
from matcher import get_auto_splits_associations

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
        match = await get_auto_splits_associations(target_word, limit=10)
        print(time.ctime())
        if len(match) == 2:
            print(f"{target_word} {match[0].word} {match[1].word}")
        else:
            print(f"{target_word} {match[0].word}")

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
loop.close()