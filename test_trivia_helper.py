from trivia_helper import get_options, get_file, match_keywords, choose
import io
import csv
import pytest

def test_get_options():
    assert get_options(["test_file.csv", "camelCase.csv", "PeRfEcT_cAsInG.CsV"], ".csv", "_") == [["test", "file"], ["PeRfEcT", "cAsInG"]]
    assert get_options(["bad_ext.lol", "space separator.csv"], ".csv", " ") == [["space", "separator"]]
    assert get_options([]) == []

def test_get_file():
    with get_file("test", "good", "test_csv", ".csv", "_") as file_exact:
        assert isinstance(file_exact, io.TextIOBase) == True
    with get_file("TeSt", "gOoD", "test_csv", ".CSV", "_") as file_casing:
        assert isinstance(file_casing, io.TextIOBase) == True
    with pytest.raises(FileNotFoundError):
        get_file("does_not", "exist", "test_csv", ".lol", "?")
    with pytest.raises(FileNotFoundError):
        get_file("test_missing", "directory", "bad_directory", ".lol", "?")


#'test_good.csv' and 'test_bad.csv' files are needed in directory 'test_csv' to complete this test
#'test_good.csv' should have appropriate keys and values, while 'test_bad.csv' has invalid keys for testing
def test_match_keywords():
    with open("test_csv/test_good.csv") as file:
        reader = csv.DictReader(file)
        assert next(match_keywords(reader, ["hello"], "question", "answer")) == "GOODBYE"
    with open("test_csv/test_bad.csv") as file:
        reader = csv.DictReader(file)
        with pytest.raises(KeyError):
            next(match_keywords(reader, ["oh well"], "key1", "key2"))

#Need to run pytest with a -s argument as input is required for this test
#Entering either 'hello' or 'test' when prompted to match a list element is required
def test_choose():
    assert choose([["test"], ["hello"]]) == ["test"] or ["hello"]
    assert choose([["single"]]) == ["single"]
    with pytest.raises(IndexError):
        choose([])
    with pytest.raises(TypeError):
        choose("string")