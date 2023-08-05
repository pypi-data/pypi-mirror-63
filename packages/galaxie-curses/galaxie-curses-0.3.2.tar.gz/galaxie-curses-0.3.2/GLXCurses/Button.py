#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import GLXCurses
import curses
import logging


class Button(GLXCurses.Widget, GLXCurses.Movable):

    def __init__(self):
        # Load heritage
        GLXCurses.Movable.__init__(self)
        GLXCurses.Widget.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.Button'

        # Widgets can be named, which allows you to refer to them from a GLXCStyle
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # Make a Widget Style heritage attribute as local attribute
        # if self.style.attribute_states:
        #     self.attribute_states = self.style.attribute_states

        # Internal Widget Setting
        self.__text = None

        # Interface
        self.interface = '[  ]'
        self.interface_selected = '[<>]'
        self.button_border = self.interface

        # Size management
        self._update_preferred_sizes()

        # Justification: LEFT, RIGHT, CENTER
        self._justify = GLXCurses.GLXC.JUSTIFY_CENTER

        # PositionType: CENTER, TOP, BOTTOM
        self._position_type = GLXCurses.GLXC.POS_CENTER

        # Properties
        self.label = None

        # States
        self.curses_mouse_states = {
            curses.BUTTON1_PRESSED: 'BUTTON1_PRESS',
            curses.BUTTON1_RELEASED: 'BUTTON1_RELEASED',
            curses.BUTTON1_CLICKED: 'BUTTON1_CLICKED',
            curses.BUTTON1_DOUBLE_CLICKED: 'BUTTON1_DOUBLE_CLICKED',
            curses.BUTTON1_TRIPLE_CLICKED: 'BUTTON1_TRIPLE_CLICKED',

            curses.BUTTON2_PRESSED: 'BUTTON2_PRESSED',
            curses.BUTTON2_RELEASED: 'BUTTON2_RELEASED',
            curses.BUTTON2_CLICKED: 'BUTTON2_CLICKED',
            curses.BUTTON2_DOUBLE_CLICKED: 'BUTTON2_DOUBLE_CLICKED',
            curses.BUTTON2_TRIPLE_CLICKED: 'BUTTON2_TRIPLE_CLICKED',

            curses.BUTTON3_PRESSED: 'BUTTON3_PRESSED',
            curses.BUTTON3_RELEASED: 'BUTTON3_RELEASED',
            curses.BUTTON3_CLICKED: 'BUTTON3_CLICKED',
            curses.BUTTON3_DOUBLE_CLICKED: 'BUTTON3_DOUBLE_CLICKED',
            curses.BUTTON3_TRIPLE_CLICKED: 'BUTTON3_TRIPLE_CLICKED',

            curses.BUTTON4_PRESSED: 'BUTTON4_PRESSED',
            curses.BUTTON4_RELEASED: 'BUTTON4_RELEASED',
            curses.BUTTON4_CLICKED: 'BUTTON4_CLICKED',
            curses.BUTTON4_DOUBLE_CLICKED: 'BUTTON4_DOUBLE_CLICKED',
            curses.BUTTON4_TRIPLE_CLICKED: 'BUTTON4_TRIPLE_CLICKED',

            curses.BUTTON_SHIFT: 'BUTTON_SHIFT',
            curses.BUTTON_CTRL: 'BUTTON_CTRL',
            curses.BUTTON_ALT: 'BUTTON_ALT'
        }

        # Sensitive
        self.can_default = True
        self.can_focus = True
        self.sensitive = True
        self.states_list = None

        # Subscription
        self.connect('MOUSE_EVENT', Button._handle_mouse_event)
        # Keyboard
        self.connect('CURSES', Button._handle_key_event)

    def draw_widget_in_area(self):
        self.create_or_resize()

        if self.subwin is not None:
            self._check_selected()
            self._update_preferred_sizes()

            if len(self.text) > 0:
                self._draw_button()

    # Internal Widget functions
    def set_text(self, text):
        if self.__text != text:
            self.__text = text
            self._check_selected()
            self._update_preferred_sizes()

    def get_text(self):
        return self.__text

    @property
    def text(self):
        return self.__text

    # Justification: LEFT, RIGHT, CENTER
    def set_justify(self, justify):
        """
        Set the Justify of the Vertical separator

         Justify:
          - LEFT
          - CENTER
          - RIGHT

        :param justify: a Justify
        :type justify: str
        """
        if justify in [GLXCurses.GLXC.JUSTIFY_LEFT, GLXCurses.GLXC.JUSTIFY_CENTER, GLXCurses.GLXC.JUSTIFY_RIGHT]:
            if self.get_justify() != str(justify).upper():
                self._justify = str(justify).upper()
                # When the justify is set update preferred sizes store in Widget class
                self._update_preferred_sizes()
        else:
            raise TypeError('PositionType must be LEFT or CENTER or RIGHT')

    def get_justify(self):
        """
        Return the Justify of the CheckButton

         Justify:
          - LEFT
          - CENTER
          - RIGHT

        :return: str
        """
        return self._justify

    # PositionType: CENTER, TOP, BOTTOM
    def set_position_type(self, position_type):
        """
        Set the Position type

        PositionType:
         .GLXCurses.GLXC.POS_TOP
         .GLXCurses.GLXC.POS_CENTER
         .GLXCurses.GLXC.POS_BOTTOM

        :param position_type: a PositionType
        :type position_type: str
        """
        if position_type in [GLXCurses.GLXC.POS_TOP, GLXCurses.GLXC.POS_CENTER, GLXCurses.GLXC.POS_BOTTOM]:
            if self.get_position_type() != str(position_type).upper():
                self._position_type = str(position_type).upper()
                # When the position type is set update preferred sizes store in Widget class
                self._update_preferred_sizes()
        else:
            raise TypeError('PositionType must be CENTER or TOP or BOTTOM')

    def get_position_type(self):
        """
        Return the Position Type

        PositionType:
         .GLXCurses.GLXC.POS_TOP
         .GLXCurses.GLXC.POS_CENTER
         .GLXCurses.GLXC.POS_BOTTOM

        :return: str
        """
        return self._position_type

    # State
    def get_states(self):
        return self.states_list

    # Internal
    def _draw_button(self):
        self._check_selected()
        self._update_preferred_sizes()
        self._check_justify()
        self._check_position_type()

        if not self.sensitive:
            self._draw_the_good_button(
                color=self.style.get_color_pair(
                    foreground=self.style.get_color_text('text', 'STATE_NORMAL'),
                    background=self.style.get_color_text('bg', 'STATE_NORMAL')
                ) | curses.A_DIM
            )
        elif self.has_prelight:
            self._draw_the_good_button(
                color=self.style.get_color_pair(
                    foreground=self.style.get_color_text('dark', 'STATE_NORMAL'),
                    background=self.style.get_color_text('bg', 'STATE_PRELIGHT')
                )
            )
        elif self.state['NORMAL']:
            self._draw_the_good_button(
                color=self.style.get_color_pair(
                    foreground=self.style.get_color_text('text', 'STATE_NORMAL'),
                    background=self.style.get_color_text('bg', 'STATE_NORMAL')
                )
            )

    def _draw_the_good_button(self, color):
        try:
            # Interface management
            self.subwin.addstr(
                self.y_offset,
                self.x_offset,
                self.button_border[:int(len(self.button_border) / 2)],
                color
            )
        except curses.error:
            pass
        # Draw the Horizontal Button with Justification and PositionType
        message_to_display = GLXCurses.resize_text(self.text, self.width - 1 - len(self.button_border), '~')
        try:
            self.subwin.addstr(
                self.y_offset,
                self.x_offset + int(len(self.button_border) / 2),
                message_to_display,
                color
            )
        except curses.error:
            pass
        message_to_display = GLXCurses.resize_text(self.get_text(), self.width - 1 - len(self.button_border), '~')
        try:
            self.subwin.insstr(
                self.y_offset,
                self.x_offset + int(len(self.button_border) / 2) + len(message_to_display),
                self.button_border[-int(len(self.button_border) / 2):],
                color
            )
        except curses.error:
            pass

    def _handle_mouse_event(self, event_signal, event_args):
        if self.sensitive:
            (mouse_event_id, x, y, z, event) = event_args

            # Be sure we select really the Button
            y -= self.y
            x -= self.x

            x_pos_start = self.x_offset + len(self.button_border) + len(self.text) - 1
            x_pos_stop = self.x_offset
            y_pos_start = self.y_offset
            y_pos_stop = self.y_offset - self.preferred_height + 1

            that_for_me = (y_pos_start >= y >= y_pos_stop and x_pos_start >= x >= x_pos_stop)

            if that_for_me:
                self._grab_focus()


                # BUTTON1
                if event == curses.BUTTON1_PRESSED:
                    GLXCurses.Application().has_prelight = self
                    self.is_prelight = True
                    self.has_focus = True

                elif event == curses.BUTTON1_RELEASED:
                    GLXCurses.Application().has_prelight = None
                    self.has_prelight = False
                    self.has_focus = True

                if event == curses.BUTTON1_CLICKED:
                    self.has_prelight = False
                    self.has_focus = True

                if event == curses.BUTTON1_DOUBLE_CLICKED:
                    pass

                if event == curses.BUTTON1_TRIPLE_CLICKED:
                    pass

                # Create a Dict with everything
                instance = {
                    'class': self.__class__.__name__,
                    'label': self.get_text(),
                    'id': self.id
                }
                # EVENT EMIT
                # Application().emit(self.curses_mouse_states[event], instance)
                self.emit(self.curses_mouse_states[event], instance)
            else:
                # Nothing for me , the better is to clean the prelight
                # self._set_state_prelight(False)
                # self.set_has_focus(False)
                self._check_selected()
        else:
            if self.debug:
                logging.debug('{0} -> id:{1}, object:{2}, is not sensitive'.format(
                    self.__class__.__name__,
                    self.id,
                    self
                ))

    def _handle_key_event(self, event_signal, *event_args):
        # Check if we have to care about keyboard event
        if self.sensitive and self.has_default:
            # setting
            key = event_args[0]

            # Touch Escape
            if key == GLXCurses.GLXC.KEY_ESC:

                GLXCurses.Application().has_focus = None
                GLXCurses.Application().has_prelight = None
                GLXCurses.Application().has_default = None
                self._check_selected()
                self._update_preferred_sizes()

            if len(self.text) > 0:
                if key == ord(self.text[0].upper()) or key == ord(self.text[0].lower()):
                    instance = {
                        'class': self.__class__.__name__,
                        'label': self.get_text(),
                        'id': self.id
                    }
                    self.emit(self.curses_mouse_states[curses.BUTTON1_CLICKED], instance)

            if key == curses.KEY_ENTER or key == ord("\n"):
                # Create a Dict with everything
                instance = {
                    'class': self.__class__.__name__,
                    'label': self.get_text(),
                    'id': self.id
                }
                self.emit(self.curses_mouse_states[curses.BUTTON1_CLICKED], instance)

    def _check_selected(self):
        if self.can_focus:
            something_change = False
            if GLXCurses.Application().has_default is not None:
                if GLXCurses.Application().has_default.widget.id == self.id:
                    self.has_default = True
                    self.button_border = self.interface_selected
                    something_change = True
                else:
                    self.has_default = False
                    self.button_border = self.interface
                    something_change = True
            if GLXCurses.Application().has_focus is not None:
                if GLXCurses.Application().has_focus.widget.id == self.id:
                    self.has_focus = False
                    self.button_border = self.interface_selected
                    something_change = True
                else:
                    self.has_focus = False
                    self.button_border = self.interface
                    something_change = True
            if GLXCurses.Application().has_prelight is not None:
                if GLXCurses.Application().has_prelight.widget.id == self.id:
                    self.has_prelight = True
                    something_change = True
                else:
                    self.has_prelight = False
                    something_change = True
            if something_change:
                self._update_preferred_sizes()

    def _grab_focus(self):
        """
        Internal method, for Select the contents of the Entry it take focus.

        See: grab_focus_without_selecting ()
        """
        if self.can_focus:
            GLXCurses.Application().has_focus = self
            GLXCurses.Application().has_default = self
        self._check_selected()

    def _check_justify(self):
        """Check the justification of the X axe"""
        width = self.width - 1
        preferred_width = self.preferred_width

        self.x_offset = 0
        if self.get_justify() == GLXCurses.GLXC.JUSTIFY_CENTER:
            # Clamp value and impose the center
            if width is None:
                estimated_width = 0
            elif width <= 0:
                estimated_width = 0
            elif width == 1:
                estimated_width = 0
            else:
                estimated_width = int(width / 2)

            # Clamp value and impose the center
            if preferred_width is None:
                estimated_preferred_width = 0
            elif preferred_width <= 0:
                estimated_preferred_width = 0
            elif preferred_width == 1:
                estimated_preferred_width = 0
            else:
                estimated_preferred_width = int(preferred_width / 2)

            # Make the compute
            final_value = int(estimated_width - estimated_preferred_width)

            # clamp the result
            if final_value <= 0:
                final_value = 0

            # Finally set the value
            self.x_offset = final_value

        elif self.get_justify() == GLXCurses.GLXC.JUSTIFY_LEFT:

            self.x_offset = 0

        elif self.get_justify() == GLXCurses.GLXC.JUSTIFY_RIGHT:

            # Make the compute
            final_value = int(width - preferred_width)

            # clamp the result
            if final_value <= 0:
                final_value = 0

            # Finally set the value
            self.x_offset = final_value

    def _check_position_type(self):
        # PositionType: CENTER, TOP, BOTTOM
        height = 0.5
        preferred_height = self.preferred_height

        if self.get_position_type() == GLXCurses.GLXC.POS_CENTER:
            # Clamp height
            if int(self.height / 2) <= 1:
                self.y_offset = 0
            else:
                self.y_offset = GLXCurses.clamp_to_zero(int(self.height / 2))

        elif self.get_position_type() == GLXCurses.GLXC.POS_TOP:
            self.y_offset = 0

        elif self.get_position_type() == GLXCurses.GLXC.POS_BOTTOM:
            # Clamp height
            if self.height - 1 <= 1:
                self.y_offset = 0
            else:
                self.y_offset = GLXCurses.clamp_to_zero(self.height - 1)

    def _update_preferred_sizes(self):
        self.preferred_width = self._get_estimated_preferred_width()
        self.preferred_height = self._get_estimated_preferred_height()

    def _get_estimated_preferred_width(self):
        """
        Estimate a preferred width, by consider X Location, allowed width

        :return: a estimated preferred width
        :rtype: int
        """
        if self.get_text():
            estimated_preferred_width = 0
            estimated_preferred_width += len(self.get_text())
            estimated_preferred_width += len(self.button_border)
        else:
            estimated_preferred_width = 0
            estimated_preferred_width += len(self.button_border)

        return estimated_preferred_width

    @staticmethod
    def _get_estimated_preferred_height():
        """
        Estimate a preferred height, by consider Y Location

        :return: a estimated preferred height
        :rtype: int
        """
        return 1

    # Unimplemented
    def _enter(self):
        raise NotImplementedError

    def _leave(self):
        raise NotImplementedError

    @staticmethod
    def _key_pressed(char):
        if char > 255:
            return 0  # skip control-characters
        # if chr(char).upper() == self.LabelButton[self.Underline]:
        #     return 1
        else:
            return 0
