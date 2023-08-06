from io import StringIO

import pytest

from gaphor import UML
from gaphor.services.eventmanager import EventManager
from gaphor.storage import storage
from gaphor.UML.elementfactory import ElementFactory


@pytest.fixture
def element_factory():
    return ElementFactory(EventManager())


@pytest.fixture
def diagram(element_factory):
    return element_factory.create(UML.Diagram)


@pytest.fixture
def loader(element_factory):
    def load(data):
        """
        Load data from specified string.
        """
        element_factory.flush()
        assert not list(element_factory.select())

        f = StringIO(data)
        storage.load(f, factory=element_factory)
        f.close()

    return load
