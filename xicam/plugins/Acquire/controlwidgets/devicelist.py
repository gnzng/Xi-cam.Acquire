from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

from alsdac import ophyd as alsophyd
import ophyd
from ophyd.utils.epics_pvs import BadPVName
from xicam.core import msg
from xicam.gui import threads
from xicam.plugins import manager as pluginmanager
from ..devices import Device

class DeviceList(QListView):
    sigShowControl = Signal(QWidget)

    def __init__(self):
        super(DeviceList, self).__init__()

        self._model = pluginmanager.getPluginByName('Devices', 'SettingsPlugin').plugin_object.devicesmodel
        self.setModel(self._model)

    # FIXME: device discovery is not officially an element of EPICS's design; early work will add devices explicitly
    # @threads.method
    # def refresh(self):
    #     self._model.clear()
    #
    #
    #
    #     # Find devices
    #     motors = ophyd.EpicsSignalRO('beamline:motors:devices', name='motors').value
    #     ais = ophyd.EpicsSignalRO('beamline:ais:devices', name='ais').value
    #     dios = ophyd.EpicsSignalRO('beamline:dios:devices', name='dios').value
    #     instruments = ophyd.EpicsSignalRO('beamline:instruments:devices', name='instruments').value
    #
    #     for pvname in motors:
    #         try:
    #             self._model.appendRow(DeviceItem(pvname, alsophyd.Motor('beamline:motors:' + pvname, name=pvname)))
    #         except BadPVName:
    #             msg.logMessage(f'PV named "{pvname}" is invalid.', msg.WARNING)

    def selectionChanged(self, *args, **kwargs):
        indexes = self.selectedIndexes()
        if indexes and indexes[0].isValid():
            item = self._model.itemFromIndex(indexes[0])
            self.sigShowControl.emit(item.widget)
