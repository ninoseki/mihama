from app.core import datastructures


def test_unique_csv():
    csv = datastructures.UniqueCommaSeparatedStrings("a,a,a")
    assert list(csv) == ["a"]
