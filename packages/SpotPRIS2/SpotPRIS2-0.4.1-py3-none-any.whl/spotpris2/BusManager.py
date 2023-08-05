from pydbus import SessionBus

from .util import new_session_bus, create_playback_state
from . import MediaPlayer2
from abc import ABCMeta, abstractmethod


class BusManager(metaclass=ABCMeta):
    def __init__(self, spotify, app_name):
        self.spotify = spotify
        self.app_name = app_name

    def _publish(self, bus, player, bus_postfix=None):
        bus_name = f"org.mpris.MediaPlayer2.{self.app_name}"
        if bus_postfix is not None:
            bus_name = f"{bus_name}.{bus_postfix}"
        return bus.publish(bus_name, ("/org/mpris/MediaPlayer2", player))

    @abstractmethod
    def main_loop(self):
        pass


class SingleBusManager(BusManager):
    def __init__(self, spotify, app_name="spotpris"):
        super().__init__(spotify, app_name)
        self.publication = None
        self.bus = SessionBus()  # Use built in method to get bus singleton
        self.player = None

    def main_loop(self):
        current_playback = self.spotify.current_playback()
        if current_playback is None:
            if self.publication is not None:
                self.publication.unpublish()
                self.publication = None
        else:
            if self.publication is None:
                if self.player is None:
                    self.player = MediaPlayer2(self.spotify, current_playback)
                self.publication = self._publish(self.bus, self.player)
            self.player.event_loop(current_playback)


class MultiBusManager(BusManager):
    def __init__(self, spotify, allowed_devices=None, ignored_devices=None, app_name="spotpris"):
        super().__init__(spotify, app_name)
        self.allowed_devices = allowed_devices
        self.ignored_devices = ignored_devices
        self.current_devices = {}

    def main_loop(self):
        devices = self.spotify.devices()["devices"]
        devices = {d["id"]: d for d in devices}
        current_playback = self.spotify.current_playback()
        for device_id in devices:
            if device_id not in self.current_devices and self._is_device_allowed(devices[device_id]):
                self._create_device(device_id, create_playback_state(current_playback, devices[device_id]))

        for device_id in list(self.current_devices.keys()):
            if device_id not in devices:
                self._remove_device(device_id)
            else:
                self.current_devices[device_id].player.event_loop(
                    create_playback_state(current_playback, device=devices[device_id]))

    def _create_device(self, device_id, current_playback):
        bus = new_session_bus()
        player = MediaPlayer2(self.spotify, current_playback, device_id=device_id)
        publication = self._publish(bus, player, bus_postfix=f"device{device_id}")
        self.current_devices[device_id] = self.PlayerInfo(player, publication)

    def _remove_device(self, device_id):
        player_info = self.current_devices[device_id]
        player_info.publication.unpublish()
        del self.current_devices[device_id]

    def _is_device_allowed(self, device):
        if self.allowed_devices is not None:
            return device["name"] in self.allowed_devices or device["id"] in self.allowed_devices
        elif self.ignored_devices is not None:
            return device["name"] not in self.ignored_devices and device["id"] not in self.ignored_devices
        else:
            return True

    class PlayerInfo:
        def __init__(self, player, publication):
            self.player = player
            self.publication = publication
