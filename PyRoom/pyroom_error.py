# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# PyRoom - A clone of WriteRoom
# Copyright (c) 2007 Nicolas P. Rougier & NoWhereMan
# Copyright (c) 2008 The Pyroom Team - See AUTHORS file for more information
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------


"""
Errors raised within pyroom

"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import Pango
import traceback

class PyroomError(Exception):
    """our nice little exception"""
    message = None
    def __init__(self, msg):
        self.message = msg

def handle_error(exception_type, exception_value, exception_traceback):
    """display errors to the end user using dialog boxes"""
    if exception_type == PyroomError:
        message = exception_value.message
    elif exception_type == KeyboardInterrupt: # ctrl+c
        return
    else: # uncaught exception in code
        message = _("""There has been an uncaught exception in pyroom.\n
                    This is most likely a programming error. \
                    Please submit a bug report to launchpad""")

    error_dialog = Gtk.MessageDialog(parent=None, flags=Gtk.DialogFlags.MODAL,
                type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.NONE,
                message_format=message)
    error_dialog.set_title(_('Error'))
    error_dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
    if not exception_type == PyroomError:
        error_dialog.add_button (_("Details..."), 2)
    error_dialog.set_position(Gtk.WindowPosition.CENTER)
    error_dialog.set_gravity(Gdk.Gravity.CENTER)
    error_dialog.show_all()

    details_textview = Gtk.TextView()
    details_textview.show()
    details_textview.set_editable(False)
    details_textview.modify_font(Pango.FontDescription('Monospace'))

    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.show()
    scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    scrolled_window.add(details_textview)

    frame = Gtk.Frame()
    frame.set_shadow_type(Gtk.ShadowType.IN)
    frame.add(scrolled_window)
    frame.set_border_width(6)
    error_dialog.vbox.add(frame)

    details_buffer = details_textview.get_buffer()
    printable_traceback = "\n".join(
        traceback.format_exception(
            exception_type,
            exception_value,
            exception_traceback,
        )
    )
    details_buffer.set_text(printable_traceback)
    details_textview.set_size_request(
        Gdk.Screen.width() /1.5,  #/2
        Gdk.Screen.height()/2.25  #/3 testing new spacing to allow for more erros :/
    )

    error_dialog.details = frame

    while True:
        resp = error_dialog.run()
        if resp == 2:
            error_dialog.details.show()
            error_dialog.action_area.get_children()\
        [0].set_sensitive(0)
        else:
            break
    error_dialog.destroy()
