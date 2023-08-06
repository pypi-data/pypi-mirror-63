import asyncio
import inspect
import logging
import os
import shlex
from collections import defaultdict
from concurrent import futures
from contextlib import suppress
from datetime import timedelta
from functools import partial

from docopt import DocoptExit, docopt
from platforms_clients.commissioning.representation.entities import GroupAddress
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.eventloop import use_asyncio_event_loop
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout

from bluetooth_mesh.application import Application, Element
from bluetooth_mesh.apps.mixins import CommandLineMixin
from bluetooth_mesh.messages.config import GATTNamespaceDescriptor
from bluetooth_mesh.models import (
    ConfigClient,
    ConfigServer,
    DebugClient,
    GatewayConfigClient,
    GenericLevelClient,
    GenericOnOffClient,
    HealthClient,
    LightCTLClient,
    LightLightnessClient,
    NetworkDiagnosticClient,
    NetworkDiagnosticSetupClient,
    SceneClient,
)


class MeshCompleter(Completer):
    def __init__(self, application):
        self.application = application
        super().__init__()

    def get_completions(self, document, complete_event):
        if not document.is_cursor_at_the_end:
            return

        command = document.text_before_cursor
        if " " not in command:  # try commands
            for cmd in self.application.commands.values():
                if cmd.CMD.startswith(command):
                    yield Completion(cmd.CMD, start_position=-len(command))

        else:
            words = shlex.split(command)
            if command.endswith(" "):  # wo for difference in split and shlex.split
                words.append("")
            if "-z" in words:  # try zones
                for zone in {
                    zone.zone_name for zone in self.application.network.groups
                }:
                    if zone and zone.startswith(words[-1]):
                        if " " in zone:
                            zone = '"{}"'.format(zone)
                        yield Completion(zone, start_position=-len(words[-1]))

            else:  # try nodes
                for node in {
                    node.uuid.hex[:4] for node in self.application.network.nodes
                }:
                    if node.startswith(words[-1]):
                        yield Completion(node, start_position=-len(words[-1]))


class Command:
    USAGE = """
    Usage:
        %(cmd)s
    """
    CMD = None

    async def __call__(self, application, arguments):
        raise NotImplementedError()

    def get_usage(self, **kwargs):
        return self.USAGE % dict(cmd=self.CMD, **kwargs)

    def __lt__(self, other):
        return self.CMD < other.CMD


class LsCommand(Command):
    USAGE = """
    Usage:
        %(cmd)s
        %(cmd)s [options] <zones>...

    Options:
        -l --long
    """

    CMD = "ls"

    async def __call__(self, application, arguments):
        zones = arguments["<zones>"]

        if zones:
            nodes = defaultdict(list)

            for node in application.network.nodes:
                if not zones or node.zone_name in zones:
                    nodes[node.zone_name].append(node)

            for zone, nodes in sorted(nodes.items(), key=lambda n: n[0]):
                yield "{}:".format(zone)
                for node in sorted(nodes, key=lambda n: n.uuid):
                    if arguments["--long"]:
                        yield "\t{} {:04x} {}".format(
                            node.uuid, node.address, node.name
                        )
                    else:
                        yield "\t{}".format(node.name)
        else:
            for zone in sorted({node.zone_name for node in application.network.nodes}):
                yield "\t{}".format(zone)


class ModelCommandMixin:
    ELEMENT = None
    MODEL = None

    def get_model(self, application):
        return application.elements[self.ELEMENT][self.MODEL]


class AttentionCommand(ModelCommandMixin, Command):
    USAGE = """
    Usage:
        %(cmd)s [options] <uuid>...
        %(cmd)s [options] -z <zones>...

    Options:
        -t --timeout=ATTENTION    Attention timer [default: 5].
        -z --zones
    """

    ELEMENT = 0
    MODEL = HealthClient
    CMD = "attention"

    async def __call__(self, application, arguments):
        model = self.get_model(application)

        attention = int(arguments["--timeout"])

        tasks = []
        if arguments["<uuid>"]:
            tasks = [
                model.attention(node.address, app_index=0, attention=attention)
                for node in application.network.nodes
                if node.uuid.hex[:4] in arguments["<uuid>"]
            ]

        elif arguments["<zones>"]:
            tasks = [
                model.attention_unack(
                    group.get_address(GroupAddress.HEALTH),
                    app_index=0,
                    attention=attention,
                )
                for group in application.network.groups
                if group.zone_name in arguments["<zones>"]
            ]

        return asyncio.gather(*tasks)


class RecallSceneCommand(ModelCommandMixin, Command):
    USAGE = """
    Usage:
        %(cmd)s [options] <uuid>...
        %(cmd)s [options] -z <zones>...

    Options:
        -c --scene=SCENE    Number of scene to recall.
        -t --transition-time=TRANSITION-TIME    Transition time in seconds [default: 0].
        -z --zones
    """
    ELEMENT = 0
    MODEL = SceneClient
    CMD = "recall_scene"

    async def __call__(self, application, arguments):
        model = application.elements[0][SceneClient]

        scene_number = int(arguments["--scene"])
        transition_time = int(arguments["--transition-time"])

        tasks = []
        if arguments["<uuid>"]:
            tasks = [
                model.recall_scene_unack(
                    node.address,
                    app_index=0,
                    scene_number=scene_number,
                    transition_time=transition_time,
                )
                for node in application.network.nodes
                if node.uuid.hex[:4] in arguments["<uuid>"]
            ]

        elif arguments["<zones>"]:
            tasks = [
                model.recall_scene_unack(
                    group.get_address(GroupAddress.DEFAULT),
                    app_index=0,
                    scene_number=scene_number,
                    transition_time=transition_time,
                )
                for group in application.network.groups
                if group.zone_name in arguments["<zones>"]
            ]

        await asyncio.gather(*tasks)


class NodeSelectionCommandMixin:
    USAGE = """
    Usage:
        %(cmd)s <uuid>...
        %(cmd)s -z <zones>...

    Options:
        -z --zones
    """

    @staticmethod
    def get_addresses(application, arguments):
        uuids = arguments.get("<uuid>", [])
        zones = arguments.get("<zones>", [])
        return [
            node.address
            for node in application.network.nodes
            if node.uuid.hex[:4] in uuids or node.zone_name in zones
        ]


class ModelGetCommandMixin(ModelCommandMixin, NodeSelectionCommandMixin):
    PARAMETER = None

    def format(self, data):
        return str(data[self.PARAMETER])

    async def __call__(self, application, arguments):
        model = self.get_model(application)
        addresses = self.get_addresses(application, arguments)

        get = getattr(model, "get_{}".format(self.PARAMETER))
        results = await get(addresses, 0)

        for address, data in results.items():
            node = application.network.get_node(address=address)
            param = self.format(data) if data is not None else None
            yield "{} | {}: {}".format(node.zone_name, node.name, param)


class DebugCommand(ModelGetCommandMixin, Command):
    ELEMENT = 0
    MODEL = DebugClient


class UptimeCommand(DebugCommand):
    CMD = "uptime"
    PARAMETER = "uptime"

    def format(self, data):
        return str(timedelta(seconds=data["uptime"]))


class FaultCommand(DebugCommand):
    CMD = "fault"
    PARAMETER = "last_sw_fault"

    def format(self, data):
        return "{}, {}".format(data["fault"], timedelta(seconds=data["time"]))


class VersionCommand(DebugCommand):
    CMD = "version"
    PARAMETER = "firmware_version"

    def format(self, data):
        return str(data["version"])


class IvIndexCommand(DebugCommand):
    CMD = "ivindex"
    PARAMETER = "ivindex"


class ArapCommand(DebugCommand):
    CMD = "arap"
    PARAMETER = "arap_content"

    def format(self, data):
        return "\n" + "\n".join(
            "\t{:04x}: {:8d} ivi={:1d}".format(k, v["sequence"], v["ivi"])
            for k, v in data["nodes"].items()
        )


class StatsCommand(DebugCommand):
    CMD = "stats"
    PARAMETER = "system_stats"

    def format(self, data):
        return "\n" + "\n".join(
            "\t{:>10s}: {:5d}".format(k, v) for k, v in data["stats"].items()
        )


class AppVersionCommand(DebugCommand):
    CMD = "app_version"
    PARAMETER = "app_version"

    def format(self, data):
        return str(data["version"])


class ConfigCommand(ModelGetCommandMixin, Command):
    ELEMENT = 0
    MODEL = ConfigClient


class TtlCommand(ConfigCommand):
    CMD = "ttl"
    PARAMETER = "default_ttl"

    def format(self, data):
        return data["TTL"]


class RelayCommand(ConfigCommand):
    CMD = "relay"
    PARAMETER = "relay"

    def format(self, data):
        return "%s <interval: %sms, count: %s>" % (
            data["relay"],
            data["retransmit"]["interval"],
            data["retransmit"]["count"],
        )


class GatewayConfigurationCommand(
    ModelCommandMixin, NodeSelectionCommandMixin, Command
):
    USAGE = (
        """
    Usage:
        %(cmd)s ("""
        "--mtu=MTU | --mac=MAC | --server=HOST:PORT | --reconnect=INTERVAL | "
        "--dns=IP | --ip=IP | --gateway=IP | --netmask=NETMASK | [--get] | "
        "--mtu=MTU --mac=MAC --server=HOST:PORT --reconnect=INTERVAL | "
        "--mtu=MTU --mac=MAC --server=HOST:PORT --reconnect=INTERVAL --dns=IP |"
        "--mtu=MTU --mac=MAC --server=HOST:PORT --reconnect=INTERVAL --dns=IP --ip=IP --netmask=NETMASK --gateway=IP"
        """) <uuid>

        %(cmd)s --mtu=MTU --mac=MAC --server=HOST:PORT --reconnect=INTERVAL <uuid>
        %(cmd)s --mtu=MTU --mac=MAC --server=HOST:PORT --reconnect=INTERVAL --dns=IP <uuid>
        %(cmd)s --mtu=MTU --mac=MAC --server=HOST:PORT --reconnect=INTERVAL --dns=IP --ip=IP --netmask=NETMASK --gateway=IP <uuid>
        %(cmd)s [--get=TYPE] <uuid>
    Options:
        --mtu=MTU               Set MTU size
        --mac=MAC               Set MAC address
        --server=SERVER:PORT    Set server's name nad port
        --reconnect=INTERVAL    Set reconnect interval
        --dns=IP                Set DNS IP address
        --ip=IP                 Set IP address
        --gateway=IP            Set gateway UP address
        --netmask=NETMASK       Set netmask
        --get                   Get current configuration
    """
    )

    CMD = "gateway"
    ELEMENT = 0
    MODEL = GatewayConfigClient

    async def __call__(self, application, arguments):
        model = self.get_model(application)

        # strip'--' prefixes from options and drop Nones
        kwargs = {
            k.lstrip("-"): v
            for k, v in arguments.items()
            if k.startswith("--") and v is not None
        }

        kwargs.pop("get", None)

        if len(kwargs) > 1:
            method = partial(model.configuration_set, **self.parse_args(kwargs))
        elif len(kwargs) > 0:
            ((name, value),) = kwargs.items()
            method = partial(getattr(model, f"{name}_set"), **self.parse_args(kwargs))
        else:
            method = getattr(model, f"configuration_get")

        tasks = [
            method(destination=node.address, net_index=0)
            for node in application.network.nodes
            if node.uuid.hex[:4] in arguments["<uuid>"]
        ]

        results = await asyncio.gather(*tasks)
        self.parse_status_payload(results[0]["params"]["payload"])

    @staticmethod
    def parse_args(args):
        parsed = {}
        for key in args:
            if key in ("mtu", "reconnect", "netmask"):
                parsed[key] = int(args[key])
            if key in ("mac", "dns", "ip", "gateway"):
                parsed[key] = args[key]
            if key in "server":
                # convert HOST:PORT into a Tuple
                host, port = args[key].split(":")
                parsed[key] = (host, int(port))

        return parsed

    @staticmethod
    def parse_status_payload(payload):
        server_addr = payload["server_address"]

        if server_addr == "":
            server_addr = "NONE"

        parsed = (
            "revision: {}\n"
            "mac: {}\n"
            "mtu: {}\n"
            "ip: {}/{}\n"
            "gateway: {}\n"
            "dns: {}\n"
            "server: {}:{}\n"
            "reconnect_interval: {}\n"
            "dhcp: {}".format(
                payload["chip_revision_id"],
                payload["mac_address"],
                payload["mtu_size"],
                payload["ip_address"],
                payload["netmask"],
                payload["gateway_ip_address"],
                payload["dns_ip_address"],
                server_addr,
                payload["server_port_number"],
                payload["reconnect_interval"],
                str(payload["flags"]),
            )
        )
        print(parsed)


class GatewayPacketsCommand(ModelCommandMixin, NodeSelectionCommandMixin, Command):
    USAGE = """
    Usage:
        %(cmd)s [options] <uuid>

    Options:
        --clear     Clear packet's error counters
    """

    CMD = "packets"
    ELEMENT = 0
    MODEL = GatewayConfigClient

    async def __call__(self, application, arguments):
        model = self.get_model(application)

        if arguments["--clear"]:
            method = partial(model.packets_clear)
        else:
            method = partial(model.packets_get)

        tasks = [
            method(node.address, net_index=0)
            for node in application.network.nodes
            if node.uuid.hex[:4] in arguments["<uuid>"]
        ]

        results = await asyncio.gather(*tasks)
        self.parse_status_packets(results[0]["params"]["payload"])

    @staticmethod
    def parse_status_packets(payload):
        parsed = (
            "rx_errors: {}\n"
            "tx_errors: {}\n"
            "bandwidth: {}\n"
            "connection_state: {}\n"
            "link_status: {}\n"
            "last_error: {}".format(
                payload["total_eth_rx_errors"],
                payload["total_eth_tx_errors"],
                payload["bandwidth"],
                str(payload["connection_state"]["conn_state"]),
                str(payload["connection_state"]["link_status"]),
                str(payload["connection_state"]["last_error"]),
            )
        )
        print(parsed)


class LightCommand(ModelCommandMixin, NodeSelectionCommandMixin, Command):
    USAGE = """
            Usage:
                %(cmd)s <uuid>... [--lightness <light>] [--temperature <temp>]
                %(cmd)s -z <zones>... [--lightness <light>] [--temperature <temp>]

            Options:
                -z --zones
                -l --lightness <light>
                -t --temperature <temp>
            """
    ELEMENT = 0
    CMD = "light"
    PARAMETER = "light_status"
    CTL_ELEMENT = 2

    def format(self, data_light, data_ctl):
        return "lightness {present_lightness}, temperature {present_ctl_temperature}".format(
            present_lightness=data_light.get("present_lightness")
            if data_light
            else None,
            present_ctl_temperature=data_ctl.get("present_ctl_temperature")
            if data_ctl
            else None,
        )

    async def __call__(self, application, arguments):
        addresses = self.get_addresses(application, arguments)

        self.MODEL = LightLightnessClient
        model = self.get_model(application)
        if arguments["--lightness"]:
            results_light = await model.set_lightness(
                nodes=addresses, app_index=0, lightness=int(arguments["--lightness"])
            )
        else:
            results_light = await model.get_lightness(nodes=addresses, app_index=0)

        self.MODEL = LightCTLClient
        model = self.get_model(application)
        if arguments["--temperature"]:
            results_ctl = await model.set_ctl(
                nodes=[addr + self.CTL_ELEMENT for addr in addresses],
                app_index=0,
                ctl_temperature=int(arguments["--temperature"]),
            )
        else:
            results_ctl = await model.get_ctl(
                nodes=[addr + self.CTL_ELEMENT for addr in addresses], app_index=0
            )

        for address in addresses:
            node = application.network.get_node(address=address)
            param = self.format(
                results_light[address], results_ctl[address + self.CTL_ELEMENT]
            )
            print("{}: {}".format(node.name, param))


class NetworkTransmissionCommand(ModelCommandMixin, NodeSelectionCommandMixin, Command):
    USAGE = """
        Usage:
            %(cmd)s <uuid>... [--interval <millis>] [--count <count>]
            %(cmd)s -z <zones>... [--interval <millis>] [--count <count>]

        Options:
            -z --zones
            -s --interval <millis>
            -c --count <count>
        """
    ELEMENT = 0
    MODEL = ConfigClient
    CMD = "net_transmission"
    PARAMETER = "net_transmission"

    def format(self, data):
        return "interval={}ms, count={}".format(*data)

    async def __call__(self, application, arguments):
        model = self.get_model(application)
        addresses = self.get_addresses(application, arguments)

        for address in addresses:
            if arguments["--interval"] and arguments["--count"]:
                results = await model.set_network_transmission(
                    address,
                    net_index=0,
                    interval=int(arguments["--interval"]),
                    count=int(arguments["--count"]),
                )
            else:
                results = await model.get_network_transmission(address, net_index=0)

            node = application.network.get_node(address=address)
            param = self.format(results) if results is not None else None
            print("{}: {}".format(node.name, param))


class CompositionDataCommand(ModelCommandMixin, NodeSelectionCommandMixin, Command):
    ELEMENT = 0
    MODEL = ConfigClient
    CMD = "composition"
    PARAMETER = "composition_data"

    async def __call__(self, application, arguments):
        model = self.get_model(application)
        addresses = self.get_addresses(application, arguments)

        for address in addresses:
            data = await model.get_composition_data([address], net_index=0)
            node = application.network.get_node(address=address)

            composition = data[address]["data"]

            yield "{}: CID {}, PID {}, VID {}, CRPL {}, Features {:016b}".format(
                node.name,
                composition["CID"],
                composition["PID"],
                composition["VID"],
                composition["CRPL"],
                composition["features"],
            )

            for i, ele in enumerate(composition["elements"]):
                yield "\tElement {}, location: {}".format(i, ele["location"])
                yield "\t\t   SIG Models: " + ", ".join(
                    "{:04x}".format(mod["model_id"]) for mod in ele["SIG_models"]
                )
                yield "\t\tVendor Models: " + ", ".join(
                    "{:04x}:{:04x}".format(mod["vendor_id"], mod["model_id"])
                    for mod in ele["vendor_models"]
                )


class GenericOnOffCommand(ModelCommandMixin, Command):
    USAGE = """
    Usage:
        %(cmd)s <uuid>...
        %(cmd)s -z <zones>...

    Options:
        -z --zones
    """
    TARGET = None
    MODEL = GenericOnOffClient
    ELEMENT = 0
    PARAMETER = "set_onoff"

    async def __call__(self, application, arguments):
        model = self.get_model(application)

        tasks = []
        if arguments["<uuid>"]:
            command = getattr(model, self.PARAMETER)
            tasks = [
                command(node.address, app_index=0, onoff=self.TARGET)
                for node in application.network.nodes
                if node.uuid.hex[:4] in arguments["<uuid>"]
            ]

        elif arguments["<zones>"]:
            command = getattr(model, "{}_unack".format(self.PARAMETER))
            tasks = [
                command(
                    group.get_address(GroupAddress.LIGHTNESS),
                    app_index=0,
                    onoff=self.TARGET,
                )
                for group in application.network.groups
                if group.zone_name in arguments["<zones>"]
            ]

        await asyncio.gather(*tasks)


class GenericOnCommand(GenericOnOffCommand):
    CMD = "on"
    TARGET = True


class GenericOffCommand(GenericOnOffCommand):
    CMD = "off"
    TARGET = False


class MorseCommand(ModelCommandMixin, Command):
    USAGE = """
    Usage:
        %(cmd)s -z <zone> <text>

    Options:
        -z --zone
    """
    CMD = "morse"
    MODEL = GenericLevelClient
    ELEMENT = 0
    PARAMETER = "set_onoff_unack"

    CODE = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        "0": "-----",
        ".": ".-.-.-",
        ",": "--..--",
        ":": "---...",
        "?": "..--..",
        "'": ".----.",
        "-": "-....-",
        "/": "-..-.",
        "@": ".--.-.",
        "=": "-...-",
    }

    async def __call__(self, application, arguments):
        model = self.get_model(application)

        group = next(
            group
            for group in application.network.groups
            if group.zone_name and group.zone_name in arguments["<zone>"]
        )

        send_interval = 0.01
        retransmissions = 6

        set_unack = partial(
            model.set_level_unack,
            destination=group.get_address(GroupAddress.LIGHTNESS),
            app_index=0,
            retransmissions=retransmissions,
            send_interval=send_interval,
        )

        on = partial(set_unack, level=32767)
        off = partial(set_unack, level=-24576)

        try:
            # warm up time
            await off()
            await asyncio.sleep(0.5)

            for letter in arguments["<text>"].upper():
                code = self.CODE[letter]
                logging.getLogger("morse").info("%s = %s", letter, code)

                for blink in code:
                    await on(delay=retransmissions * send_interval)

                    delay = (
                        retransmissions * send_interval + 0.1 if blink == "." else 0.5
                    )
                    await off(delay=delay)
                    await asyncio.sleep(delay + 0.1)

                await asyncio.sleep(0.3)
        finally:
            await set_unack(level=-32768)


class HelpCommand(Command):
    CMD = "help"

    async def __call__(self, application, arguments):
        for cmd in sorted(application.commands.values()):
            yield "\t{}".format(cmd.CMD)


class PrimaryElement(Element):
    LOCATION = GATTNamespaceDescriptor.FORTY_SECOND

    MODELS = [
        GenericLevelClient,
        LightLightnessClient,
        LightCTLClient,
        # GatewayConfigClient,
        ConfigServer,
        ConfigClient,
        HealthClient,
        DebugClient,
        GenericOnOffClient,
        SceneClient,
        NetworkDiagnosticClient,
        NetworkDiagnosticSetupClient,
    ]


class MeshCommandLine(Application, CommandLineMixin):
    PATH = "/com/silvair/meshcli/v5"

    COMMANDS = [
        HelpCommand,
        LsCommand,
        AttentionCommand,
        RecallSceneCommand,
        UptimeCommand,
        FaultCommand,
        VersionCommand,
        IvIndexCommand,
        ArapCommand,
        StatsCommand,
        AppVersionCommand,
        LightCommand,
        GenericOnCommand,
        GenericOffCommand,
        CompositionDataCommand,
        MorseCommand,
        NetworkTransmissionCommand,
        TtlCommand,
        RelayCommand,
        GatewayConfigurationCommand,
        GatewayPacketsCommand,
    ]

    COMPANY_ID = 0xFEE5
    PRODUCT_ID = 0x42
    VERSION_ID = 1
    CRPL = 0xF00

    ELEMENTS = {0: PrimaryElement}

    def __init__(self, loop: asyncio.AbstractEventLoop, arguments):
        super().__init__(loop, arguments)
        self.history = FileHistory(os.path.expanduser("~/.meshcli_history"))
        self.completer = MeshCompleter(self)
        self.session = PromptSession(
            history=self.history, completer=self.completer, complete_while_typing=False,
        )
        self.commands = {cmd.CMD: cmd() for cmd in self.COMMANDS}
        self._tid = 0

    async def configure_node(self):
        await super().configure_node()

        debug_client = self.get_model_instance(element=0, model=DebugClient)
        health_client = self.get_model_instance(element=0, model=HealthClient)

        for index, *_ in self.app_keys:
            await debug_client.bind(index)
            await health_client.bind(index)

    async def run(self, command):
        addr, self.network = await self.platform_login()

        async with self:
            await self._run(addr, command)

    async def _run(self, addr, command):
        await self.connect(addr)
        await self.import_nodes()
        await self.configure_node()
        self.logger.info(
            "Loaded network %s, %d nodes", self.network, len(self.network.nodes)
        )

        while True:
            if command is not None:
                self.logger.info("Running command: %s", command)
                line = command
            else:
                line = await self.session.prompt("{}> ".format(self.uuid), async_=True)

                if not line.strip():
                    continue

            cmd, *argv = shlex.split(line)

            handler = self.commands.get(cmd, None)

            if not handler:
                print("Command not found: {}".format(cmd))
                continue

            usage = handler.get_usage()
            try:
                arguments = docopt(usage, argv, help=False)

                lines = []
                result = handler(self, arguments)

                if inspect.isasyncgen(result):
                    async for line in result:
                        lines.append(line)
                elif inspect.isawaitable(result):
                    result = await result

                    if result is not None:
                        lines.append(str())

                if lines:
                    print("\n".join(lines))
            except futures.TimeoutError:
                print("Command timed out: {}".format(cmd))
            except KeyboardInterrupt:
                pass
            except DocoptExit:
                print(usage.strip("\n").rstrip())

            if command:
                break


def main():
    doc = """
        Mesh CLI

        Usage:
            meshcli [options] [<command>]
            meshcli -h | --help | --version

        Options:
            -l --login <login>             User login to platform service (email)
            -p --password <password>       User password to platform service (!unsecured!)
            -n --project <project>         Project name to be loaded from platform

            -d --debug
            -h --help                      Show this help message and exit
            --version                      Show version and exit
    """
    use_asyncio_event_loop()
    arguments = docopt(doc, version="stat_checker 0.5")

    logging.basicConfig(
        format="%(asctime)s %(name)-40s %(levelname)-8s %(filename)15s:%(lineno)3s  %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    loop = asyncio.get_event_loop()
    mesh_cli = MeshCommandLine(loop, arguments)

    with suppress(EOFError, KeyboardInterrupt), patch_stdout():
        loop.run_until_complete(mesh_cli.run(arguments.get("<command>")))
