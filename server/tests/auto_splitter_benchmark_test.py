"""Test auto splitter with datamuse online."""
import pytest

from server.associations_manager.auto_splitter import \
    get_auto_splits_associations

SUCCESS_RATE = 0.5

words = {
    "production": ["pro", "duction"],
    "adventure": ["adven", "ture"],
    "mentorize": ["men", "torize"],
    "billing": ["billing", ],
    "consider": ["consi", "der"],
    "consideration": ["consider", "eration"],
    "forewarned": ["fore", "warned"],
    "predominantly": ["predomi", "nantly"],
    "misgivings": ["misgi", "vings"],
    "gut": ["gut", ],
    "surpass": ["sur", "pass"],
    "evolute": ["evo", "lute"],
    "obsolete": ["obs", "olete"],
    "endorsement": ["endor", "sement"],
    "deprivation": ["depri", "vation"],
    "pavement": ["pave", "ment"],
    "soreness": ["sore", "ness"],
    "annexation": ["annex", "ation"],
    "woos": ["woos"],
    "exemption": ["exem", "ption"],
    "subtle": ["sub", "tle"],
    "indictment": ["indict", "ment"],
    "inversion": ["in", "version"],
    "genocide": ["geno", "cide"],
    "renovate": ["reno", "vate"],
    "headquarters": ["head", "quarters"],
    "allegiance": ["alle", "giance"],
    "withdrawing": ["with", "drawing"],
}


@pytest.mark.asyncio
async def test_benchmark():
    """Test something."""
    differences = []
    for word, expected_result in words.items():
        result = await get_auto_splits_associations(word, limit=5)
        result = list(map(lambda association: association.word, result))
        if expected_result != result:
            print(f"Difference. Expected: {expected_result}, Found: {result}")
            differences.append((expected_result, result))

    success_rate = 1 - (len(differences) / len(words))
    assert success_rate >= SUCCESS_RATE
