from typing import List
from abc import ABC, abstractmethod


class DBInterface(ABC):
    # All Database getter methods will return Python dictionary objects (or a list of Python dictionary objects)

    def __init__(self):
        # Some initialisation can be done here in an implementing class
        pass

    @abstractmethod
    def get_indexed_documents_by_term(self, term: str, sort_entries: bool = False):
        # Given a term, returns an iterable of inverted index entries
        raise NotImplementedError()
