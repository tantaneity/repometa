import pytest

from repometa.errors import RepoReferenceError
from repometa.models import RepoRef


def should_split_owner_and_name_when_reference_valid():
    ref = RepoRef.parse("tantaneity/repometa")
    assert ref.owner == "tantaneity"
    assert ref.name == "repometa"


def should_trim_whitespace_around_segments():
    ref = RepoRef.parse(" tantaneity / repometa ")
    assert str(ref) == "tantaneity/repometa"


@pytest.mark.parametrize("value", ["repometa", "a/b/c", "/repometa", "owner/"])
def should_raise_when_reference_malformed(value):
    with pytest.raises(RepoReferenceError):
        RepoRef.parse(value)
