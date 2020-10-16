# TODO: Refactor with pytests.
import asyncio
from matcher import AssociationsMatcher

words = [
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
        match = AssociationsMatcher(target_word)
        await match.generate_possible_splits()
        print(time.ctime())
        print(match.most_associative)


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
loop.close()