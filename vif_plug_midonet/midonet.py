#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from os_vif import plugin
from os_vif import objects

from vif_plug_ovs import processutils
from vif_plug_ovs import linux_net

PLUGIN_NAME = 'midonet'


class MidonetPlugin(base.PluginBase):
    """A VIF type that plugs into a MidoNet network port."""

    def __init__(self, **config):
        processutils.configure(**config)

    def get_supported_vifs(self):
        return set([objects.PluginVIFSupport(PLUGIN_NAME, '1.0', '1.0')])

    def plug(self, instance, vif):
        """Plug into MidoNet's network port

        Bind the vif to a MidoNet virtual port.
        """
        dev = vif.devname
        port_id = vif.id
        linux_net.create_tap_dev(dev)
        processutils.execute('mm-ctl', '--bind-port', port_id, dev,
                             run_as_root=True)

    def unplug(self, vif):
        """Unplug from MidoNet network port

        Unbind the vif from a MidoNet virtual port.
        """
        dev = vif.devname
        port_id = vif.id
        processutils.execute('mm-ctl', '--unbind-port', port_id,
                             run_as_root=True)
        linux_net.delete_net_dev(dev)
