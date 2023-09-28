from hivemind_core.service import HiveMindService
from ovos_utils.messagebus import FakeBus

from fakecroft_ddg import FakeCroftDDGMindProtocol


def run():
    service = HiveMindService(protocol=FakeCroftDDGMindProtocol,
                              bus=FakeBus())
    service.run()


if __name__ == "__main__":
    run()
