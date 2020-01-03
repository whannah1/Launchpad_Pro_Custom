from __future__ import absolute_import, print_function, unicode_literals
import Live
from itertools import izip_longest
from _Framework.Util import find_if, in_range
from _Framework.Dependency import depends
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.Control import ButtonControl
from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from .ArrangementComponent import ArrangementComponent

class SpecialArrangementComponent(ArrangementComponent):
    # scene_component_type = SpecialSceneComponent
    delete_button = ButtonControl(color='DefaultButton.Off', pressed_color='DefaultButton.On')
    quantize_button = ButtonControl(color='DefaultButton.Off', pressed_color='DefaultButton.On')
    # double_button = ButtonControl(color='DefaultButton.Off', pressed_color='DefaultButton.On')
    # duplicate_button = ButtonControl(color='DefaultButton.Off', pressed_color='DefaultButton.On')

    def __init__(self, *a, **k):
        super(SpecialArrangementComponent, self).__init__(*a, **k)
        return

    # def __getattr__(self, name):
    #     if len(name) > 4 and name[:4] == 'set_':
    #         return _disable_control
    #     raise AttributeError(name)

    def on_enabled_changed(self):
        super(SpecialArrangementComponent, self).on_enabled_changed()
        return

    def update_navigation_buttons(self):
        self._vertical_banking.update()
        # self._horizontal_banking.update()


    def set_transport_buttons(self, buttons):
        if buttons:
            buttons.reset_state()
        # super(SpecialSessionComponent, self).set_scene_launch_buttons(buttons)

    def set_track_buttons(self, buttons):
        if buttons:
            buttons.reset_state()

class TrackMixerComponent(MixerComponent):
    @depends(layout_setup=None)
    def __init__(self, num_tracks=0, num_returns=0, auto_name=False, invert_mute_feedback=False, layout_setup=None, *a, **k):
        self._layout_setup = layout_setup
        super(TrackMixerComponent, self).__init__(num_tracks, num_returns, auto_name, invert_mute_feedback, *a, **k)

    def _create_track_strip(self):
        return SpecialTrackStripComponent()

    def set_arm_buttons(self, buttons):
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            if button:
                button.reset_state()
                button.set_on_off_values('Mixer.ArmOn', 'Mixer.ArmOff')
            strip.set_arm_button(button)

    def set_solo_buttons(self, buttons):
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            if button:
                button.reset_state()
                button.set_on_off_values('Mixer.SoloOn', 'Mixer.SoloOff')
            strip.set_solo_button(button)

    def set_mute_buttons(self, buttons):
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            if button:
                button.reset_state()
                button.set_on_off_values('Mixer.MuteOff', 'Mixer.MuteOn')
            strip.set_mute_button(button)

    def set_track_select_buttons(self, buttons):
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            if button:
                button.reset_state()
                button.set_on_off_values('Mixer.Selected', 'Mixer.Unselected')
            strip.set_select_button(button)

class SpecialTrackStripComponent(ChannelStripComponent):

    def __init__(self, *a, **k):
        super(SpecialTrackStripComponent, self).__init__(*a, **k)
        self.empty_color = 'DefaultButton.Disabled'

    def _arm_value(self, value):
        super(SpecialTrackStripComponent, self)._arm_value(value)
        if self.is_enabled() and value and self._track and self._track.can_be_armed and self.song().view.selected_track != self._track:
            self.song().view.selected_track = self._track

    def _select_value(self, value):
        super(SpecialTrackStripComponent, self)._select_value(value)
        if self.is_enabled() and value and self._track:
            view = self.application().view
            if view.is_view_visible('Detail') and not view.is_view_visible('Detail/DeviceChain'):
                view.show_view('Detail/DeviceChain')