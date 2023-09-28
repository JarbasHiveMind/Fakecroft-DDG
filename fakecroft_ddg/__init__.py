from hivemind_bus_client.message import HiveMessage, HiveMessageType
from hivemind_core.protocol import HiveMindListenerProtocol
from ovos_utils.messagebus import Message
from skill_ovos_ddg import DuckDuckGoSolver


class FakeCroftDDGMindProtocol(HiveMindListenerProtocol):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duck = DuckDuckGoSolver()

    def handle_inject_mycroft_msg(self, message: Message, client):
        """
        message (Message): mycroft bus message object
        """
        if message.msg_type == "recognizer_loop:utterance":
            utt = message.data["utterances"][0]
            answer = self.duck.get_spoken_answer(utt)
            payload = HiveMessage(HiveMessageType.BUS,
                                  message.reply("speak", {"utterance": answer}))
            client.send(payload)
