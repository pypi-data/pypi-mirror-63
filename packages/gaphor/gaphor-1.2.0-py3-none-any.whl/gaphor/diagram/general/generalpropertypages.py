from gi.repository import Gtk

from gaphor import UML
from gaphor.core import gettext, transactional
from gaphor.diagram.propertypages import PropertyPageBase, PropertyPages


@PropertyPages.register(UML.Comment)
class CommentItemPropertyPage(PropertyPageBase):
    """Property page for Comments."""

    order = 0

    def __init__(self, subject):
        self.subject = subject
        self.watcher = subject and subject.watcher()

    def construct(self):
        subject = self.subject
        page = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)

        if not subject:
            return page

        label = Gtk.Label(label=gettext("Comment"))
        label.set_justify(Gtk.Justification.LEFT)
        page.pack_start(label, False, True, 0)

        buffer = Gtk.TextBuffer()
        if subject.body:
            buffer.set_text(subject.body)
        text_view = Gtk.TextView()
        text_view.set_buffer(buffer)
        text_view.set_size_request(-1, 100)

        frame = Gtk.Frame()
        frame.add(text_view)

        text_view.show()
        frame.show()

        page.pack_start(frame, True, True, 0)

        changed_id = buffer.connect("changed", self._on_body_change)

        def handler(event):
            if not text_view.props.has_focus:
                buffer.handler_block(changed_id)
                buffer.set_text(event.new_value)
                buffer.handler_unblock(changed_id)

        self.watcher.watch("body", handler).subscribe_all()
        text_view.connect("destroy", self.watcher.unsubscribe_all)

        return page

    @transactional
    def _on_body_change(self, buffer):
        self.subject.body = buffer.get_text(
            buffer.get_start_iter(), buffer.get_end_iter(), False
        )
