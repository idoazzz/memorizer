import pytest
from attrdict import AttrDict
from fastapi.testclient import TestClient

import server.main
from server.associations_manager.associations import WordAssociations

client = TestClient(server.main.app)

LEGAL_LIMIT = 5
LEGAL_WORD = "Hey"

ILLEGAL_WORDS = ["Hey_",
                 "_Hey",
                 "Ma3n",
                 "He.y",
                 "!@",
                 ""]

# Mocking

NUMBER_OF_MOCKED_SPLITS = 3
MOCKED_WORD_ASSOCIATIONS = WordAssociations(word=LEGAL_WORD,
                                            associations=[],
                                            limit=LEGAL_LIMIT)

MOCKED_DEFINITIONS = [
    "a",
    "b",
    "c",
]

MOCKED_NONEMPTY_DEFINITION = {
    "word": LEGAL_WORD,
    "definitions": MOCKED_DEFINITIONS
}

MOCKED_EMPTY_DEFINITION = {
    "word": LEGAL_WORD,
    "definitions": []
}


async def mocked_get_closest_word_with_definition(_):
    """Mocked get closest word (with definition) method."""
    return AttrDict({
        "word": LEGAL_WORD,
        "defs": MOCKED_DEFINITIONS,
    })


async def mocked_get_closest_word_without_definition(_):
    """Mocked get closest word (without definition) method."""
    return AttrDict({
        "word": LEGAL_WORD,
    })


async def mocked_get_associations(_, __):
    """Mocked get associations method."""
    return [MOCKED_WORD_ASSOCIATIONS]


async def mocked_get_auto_splits_associations(_, __):
    """Mocked get associations with auto splitter method."""
    return [MOCKED_WORD_ASSOCIATIONS for _ in range(NUMBER_OF_MOCKED_SPLITS)]


# Tests

@pytest.mark.parametrize("word, limit",
                         [(LEGAL_WORD, -4), (LEGAL_WORD, 0)] +
                         [(word, LEGAL_LIMIT) for word in ILLEGAL_WORDS])
def test_invalid_associations_calls(word, limit):
    """Test associations endpoint with illegal words and limits."""
    response = client.get(f"/associations/{word}?limit={limit}&split=0")
    assert response.status_code == 404


@pytest.mark.parametrize("word", ILLEGAL_WORDS)
def test_invalid_definitions_calls(word):
    """Test associations endpoint with illegal words and limits."""
    response = client.get(f"/definitions/{word}")
    assert response.status_code == 404


@pytest.mark.parametrize("word", ILLEGAL_WORDS)
def test_invalid_closest_word_calls(word):
    """Test associations endpoint with illegal words and limits."""
    response = client.get(f"/closest/{word}")
    assert response.status_code == 404


def test_valid_associations_call_without_splitting(mocker):
    """Test valid associations response without splitting.

    Without splitting we get only associations of the exact word.
    """
    mocker.patch.object(server.main, "get_associations",
                        mocked_get_associations)
    response = client.get(
        f"/associations/{LEGAL_WORD}?limit={LEGAL_LIMIT}&split=0")
    assert response.status_code == 200
    assert response.json() == \
           {"splits": [MOCKED_WORD_ASSOCIATIONS.to_dictionary()]}


def test_valid_associations_call_with_splitting(mocker):
    """Test valid associations response without splitting.

    Without splitting we get only associations of the exact word.
    """
    mocker.patch.object(server.main, "get_auto_splits_associations",
                        mocked_get_auto_splits_associations)
    response = client.get(
        f"/associations/{LEGAL_WORD}?limit={LEGAL_LIMIT}&split=1")
    assert response.status_code == 200
    assert response.json() == \
           {"splits": [MOCKED_WORD_ASSOCIATIONS.to_dictionary()
                       for _ in range(NUMBER_OF_MOCKED_SPLITS)]}


def test_valid_existing_definition_call(mocker):
    """Test valid associations response without splitting.

    Without splitting we get only associations of the exact word.
    """
    mocker.patch.object(server.main, "get_closest_word",
                        mocked_get_closest_word_with_definition)
    response = client.get(f"/definitions/{LEGAL_WORD}")
    assert response.status_code == 200
    assert response.json() == MOCKED_NONEMPTY_DEFINITION


def test_valid_nonexisting_definition_call(mocker):
    """Test valid associations response without splitting.

    Without splitting we get only associations of the exact word.
    """
    mocker.patch.object(server.main, "get_closest_word",
                        mocked_get_closest_word_without_definition)
    response = client.get(f"/definitions/{LEGAL_WORD}")
    assert response.status_code == 200
    assert response.json() == MOCKED_EMPTY_DEFINITION
