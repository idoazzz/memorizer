
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

for target_word in words:
    match = AssociationsMatcher(target_word).most_associative
    if match.second is None:
        print(f"{match.first.word} {match.first.associations}")        
    else:
        print(f"{match.first.word} {match.first.associations}") 
        print(f"{match.second.word} {match.second.associations}")
    print()