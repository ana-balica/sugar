# Copyright (C) 2014 Ana Balica
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import logging
from gettext import gettext as _

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk

from sugar3.graphics import style
from sugar3.graphics.toolbutton import ToolButton


_logger = logging.getLogger('ViewSocial')


def setup_view_social(activity):
    window_xid = activity.get_xid()
    if window_xid is None:
        _logger.error('Activity without a window xid')
        return

    view_social = ViewSocial(window_xid, activity.get_title())
    view_social.show()


class ViewSocial(Gtk.Window):
    __gtype_name__ = 'SugarViewSocial'

    def __init__(self, window_xid, title):
        Gtk.Window.__init__(self)

        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_border_width(style.LINE_WIDTH)
        self.set_has_resize_grip(False)

        width = Gdk.Screen.width() - style.GRID_CELL_SIZE * 3
        height = Gdk.Screen.height() - style.GRID_CELL_SIZE * 3
        self.set_size_request(width, height)

        self._parent_window_xid = window_xid

        vbox = Gtk.VBox()
        self.add(vbox)
        vbox.show()

        toolbar = Toolbar(title)
        vbox.pack_start(toolbar, False, True, 0)
        toolbar.connect('stop-clicked', self.__stop_clicked_cb)
        toolbar.show()

        # TODO: display a context dependent label
        sugar_irc_label = Gtk.Label(_("IRC channel #sugar"))
        sugar_irc_button = Gtk.Button(_("Connect"))
        # TODO: this is a draft UI design (maybe even the lack of it)
        vbox.pack_start(sugar_irc_label, False, False, 0)
        vbox.pack_start(sugar_irc_button, False, False, 0)
        sugar_irc_label.show()
        sugar_irc_button.show()

    def __stop_clicked_cb(self, widget):
        self.destroy()


class Toolbar(Gtk.Toolbar):
    __gsignals__ = {
        'stop-clicked': (GObject.SignalFlags.RUN_FIRST, None, ([])),
    }

    def __init__(self, activity_name):
        Gtk.Toolbar.__init__(self)

        title = _('Social Help for ') + activity_name

        self._add_separator(False)

        label = Gtk.Label()
        label.set_markup('<b>%s</b>' % title)
        label.set_alignment(0, 0.5)
        self._add_widget(label)

        self._add_separator(True)

        stop = ToolButton(icon_name='dialog-cancel')
        stop.set_tooltip(_('Close'))
        stop.connect('clicked', self.__stop_clicked_cb)
        self.insert(stop, -1)
        stop.show()

    def __stop_clicked_cb(self, widget):
        self.emit('stop-clicked')

    def _add_widget(self, widget):
        tool_item = Gtk.ToolItem()
        tool_item.add(widget)
        widget.show()
        self.insert(tool_item, -1)
        tool_item.show()

    def _add_separator(self, expand=False):
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        if expand:
            separator.set_expand(True)
        else:
            separator.set_size_request(style.DEFAULT_SPACING, -1)
        self.insert(separator, -1)
        separator.show()
