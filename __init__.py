# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Pro/__init__.py
# Compiled at: 2018-04-23 20:27:04
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, SYNC, REMOTE, controller_id, inport, outport
from .Launchpad_Pro import Launchpad_Pro_Custom

def create_instance(c_instance):
    return Launchpad_Pro_Custom(c_instance)


def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[
                         81], model_name='Launchpad Pro Custom'), 
       PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 inport(props=[]),
                 outport(props=[NOTES_CC, SYNC, SCRIPT, REMOTE]),
                 outport(props=[])]}
