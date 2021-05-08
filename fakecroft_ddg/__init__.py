from jarbas_hive_mind.nodes.fakecroft import FakeCroftMind, FakeCroftMindProtocol
from jarbas_hive_mind import HiveMindListener
from jarbas_hive_mind.message import HiveMessage, HiveMessageType
from ovos_utils.log import LOG
from ask_the_duck import DDG


platform = "FakeCroftDDGMindV0.1"


class FakeCroftDDGMindProtocol(FakeCroftMindProtocol):
    """"""


class FakeCroftDDGMind(FakeCroftMind):
    protocol = FakeCroftDDGMindProtocol
    ddg = DDG()

    def handle_incoming_mycroft(self, message, client):
        """
        message (Message): mycroft bus message object
        """
        LOG.debug(f"Mycroft bus message received: {message.msg_type}")
        LOG.debug(f"data: {message.data}")
        LOG.debug(f"context: {message.context}")

        answer = "quack!"
        if message.msg_type == "recognizer_loop:utterance":
            utt = message.data["utterances"][0]
            answer = self.ddg.ask_the_duck(utt) or answer

        payload = HiveMessage(HiveMessageType.BUS,
                              message.reply("speak", {"utterance": answer}))
        self.interface.send(payload, client)


class FakeCroftDDGListener(HiveMindListener):
    def __init__(self, *args, **kwargs):
        super(FakeCroftDDGListener, self).__init__(*args, **kwargs)
        self.announce = False

    def secure_listen(self, key=None, cert=None, factory=None, protocol=None):
        factory = factory or FakeCroftDDGMind(announce=self.announce)
        protocol = protocol or FakeCroftDDGMindProtocol
        return super().secure_listen(key=key, cert=cert,
                                     factory=factory, protocol=protocol)

    def unsafe_listen(self, factory=None, protocol=None):
        factory = factory or FakeCroftDDGMind(announce=self.announce)
        protocol = protocol or FakeCroftDDGMindProtocol
        return super().unsafe_listen(factory=factory, protocol=protocol)

    def listen(self, factory=None, protocol=None):
        factory = factory or FakeCroftDDGMind(announce=self.announce)
        protocol = protocol or FakeCroftDDGMindProtocol
        return super().listen(factory=factory, protocol=protocol)


def get_listener(port=6789, max_connections=-1, bus=None, announce=False):
    ddg = FakeCroftDDGListener(port, max_connections, bus)
    ddg.announce = announce
    return ddg
