"""Classes related (dependency, implementation) adapter connections."""

from gaphor import UML
from gaphor.diagram.classes.association import AssociationItem
from gaphor.diagram.classes.dependency import DependencyItem
from gaphor.diagram.classes.generalization import GeneralizationItem
from gaphor.diagram.classes.implementation import ImplementationItem
from gaphor.diagram.connectors import (
    Connector,
    RelationshipConnect,
    UnaryRelationshipConnect,
)
from gaphor.diagram.presentation import Classified, ElementPresentation, Named


@Connector.register(Named, DependencyItem)
class DependencyConnect(RelationshipConnect):
    """Connect two Named elements using a Dependency."""

    def allow(self, handle, port):
        element = self.element

        # Element should be a NamedElement
        if not element.subject or not isinstance(element.subject, UML.NamedElement):
            return False

        return super().allow(handle, port)

    def reconnect(self, handle, port):
        line = self.line
        dep = line.subject
        assert isinstance(dep, UML.Dependency)
        if dep and handle is line.head:
            for s in dep.supplier:
                del dep.supplier[s]
        elif dep and handle is line.tail:
            for c in dep.client:
                del dep.client[c]
        self.reconnect_relationship(
            handle, line.dependency_type.supplier, line.dependency_type.client
        )

    def connect_subject(self, handle):
        """
        TODO: check for existing relationships (use self.relation())
        """

        line = self.line

        if line.auto_dependency:
            opposite = line.opposite(handle)

            other = self.get_connected(opposite)
            assert other
            if handle is line.head:
                client = other.subject
                supplier = self.element.subject
            else:
                client = self.element.subject
                supplier = other.subject
            line.dependency_type = UML.model.dependency_type(client, supplier)

        relation = self.relationship_or_new(
            line.dependency_type,
            line.dependency_type.supplier,
            line.dependency_type.client,
        )
        line.subject = relation


@Connector.register(Classified, GeneralizationItem)
class GeneralizationConnect(RelationshipConnect):
    """Connect Classifiers with a Generalization relationship."""

    def reconnect(self, handle, port):
        self.reconnect_relationship(
            handle, UML.Generalization.general, UML.Generalization.specific
        )

    def connect_subject(self, handle):
        relation = self.relationship_or_new(
            UML.Generalization, UML.Generalization.general, UML.Generalization.specific
        )
        self.line.subject = relation


@Connector.register(Classified, AssociationItem)
class AssociationConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: AssociationItem

    def allow(self, handle, port):
        element = self.element

        # Element should be a Classifier
        if not isinstance(element.subject, UML.Classifier):
            return None

        return super().allow(handle, port)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.canvas

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:
            head_type = c1.subject
            tail_type = c2.subject

            # First check if we do not already contain the right subject:
            if line.subject:
                assert isinstance(line.subject, UML.Association)
                end1 = line.subject.memberEnd[0]
                end2 = line.subject.memberEnd[1]
                if (end1.type is head_type and end2.type is tail_type) or (
                    end2.type is head_type and end1.type is tail_type
                ):
                    return

            # Create new association
            relation = UML.model.create_association(head_type, tail_type)
            relation.package = element.canvas.diagram.namespace

            line.head_end.subject = relation.memberEnd[0]
            line.tail_end.subject = relation.memberEnd[1]

            # Do subject itself last, so event handlers can trigger
            line.subject = relation

    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle):
        """
        Disconnect model element.
        Disconnect property (memberEnd) too, in case of end of life for
        Extension
        """
        opposite = self.line.opposite(handle)
        c1 = self.get_connected(handle)
        c2 = self.get_connected(opposite)
        if c1 and c2:
            old: UML.Association = self.line.subject
            del self.line.subject
            del self.line.head_end.subject
            del self.line.tail_end.subject
            if old and len(old.presentation) == 0:
                for e in list(old.memberEnd):
                    e.unlink()
                old.unlink()


@Connector.register(Named, ImplementationItem)
class ImplementationConnect(RelationshipConnect):
    """Connect Interface and a BehavioredClassifier using an Implementation."""

    def allow(self, handle, port):
        line = self.line
        element = self.element

        # Element at the head should be an Interface
        if handle is line.head and not isinstance(element.subject, UML.Interface):
            return None

        # Element at the tail should be a BehavioredClassifier
        if handle is line.tail and not isinstance(
            element.subject, UML.BehavioredClassifier
        ):
            return None

        return super().allow(handle, port)

    def reconnect(self, handle, port):
        line = self.line
        impl = line.subject
        assert isinstance(impl, UML.Implementation)
        if handle is line.head:
            for s in impl.contract:
                del impl.contract[s]
        elif handle is line.tail:
            for c in impl.implementatingClassifier:
                del impl.implementatingClassifier[c]
        self.reconnect_relationship(
            handle,
            UML.Implementation.contract,
            UML.Implementation.implementatingClassifier,
        )

    def connect_subject(self, handle):
        """
        Perform implementation relationship connection.
        """
        relation = self.relationship_or_new(
            UML.Implementation,
            UML.Implementation.contract,
            UML.Implementation.implementatingClassifier,
        )
        self.line.subject = relation
