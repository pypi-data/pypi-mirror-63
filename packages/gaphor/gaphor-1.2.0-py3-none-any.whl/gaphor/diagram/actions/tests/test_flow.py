from gaphas.canvas import Context, instant_cairo_context

import gaphor.UML as UML
from gaphor.diagram.actions.flow import FlowItem
from gaphor.tests.testcase import TestCase


class FlowTestCase(TestCase):
    def test_flow(self):
        self.create(FlowItem, UML.ControlFlow)

    def test_name(self):
        """
        Test updating of flow name text.
        """
        flow = self.create(FlowItem, UML.ControlFlow)
        name = flow.shape_tail.children[1]

        flow.subject.name = "Blah"

        assert "Blah" == name.text()

        flow.subject = None

        assert "" == name.text()

    def test_guard_text_update(self):
        flow = self.create(FlowItem, UML.ControlFlow)
        guard = flow.shape_middle

        assert "" == guard.text()

        flow.subject.guard = "GuardMe"
        assert "GuardMe" == guard.text()

        flow.subject = None
        assert "" == guard.text()

    def test_draw(self):
        flow = self.create(FlowItem, UML.ControlFlow)
        context = Context(
            cairo=instant_cairo_context(), hovered=True, focused=True, selected=True
        )

        flow.draw(context)
