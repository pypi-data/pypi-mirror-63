from enum import IntEnum

from construct import (
    Bytes,
    Const,
    Default,
    Embedded,
    Flag,
    GreedyString,
    Int8ul,
    Int16ul,
    PaddedString,
    Select,
    Struct,
    Switch,
    this,
)

from bluetooth_mesh.messages.util import BitList, EnumAdapter, Opcode
from pymeshd.messages.util import IpAddressAdapter, MacAddressAdapter


class GatewayConfigServerOpcode(IntEnum):
    OPCODE = 0xF03601


class GatewayConfigServerSubOpcode(IntEnum):
    GATEWAY_CONFIGURATION_GET = 0x00
    GATEWAY_CONFIGURATION_SET = 0x01
    GATEWAY_CONFIGURATION_DHCP_GET = 0x02
    GATEWAY_CONFIGURATION_DHCP_SET = 0x03
    GATEWAY_PACKETS_GET = 0x04
    GATEWAY_PACKETS_CLEAR = 0x05
    MTU_SIZE_SET = 0x06
    ETHERNET_MAC_ADDRESS_SET = 0x07
    IP_ADDRESS_SET = 0x08
    GATEWAY_IP_ADDRESS_SET = 0x09
    NETMASK_SET = 0x0A
    DNS_IP_ADDRESS_SET = 0x0B
    SERVER_ADDRESS_AND_PORT_NUMBER_SET = 0x0C
    RECONNECT_INTERVAL_SET = 0x0D
    GATEWAY_CONFIGURATION_STATUS = 0x0E
    GATEWAY_PACKETS_STATUS = 0x0F
    GATEWAY_CONFIGURATION_DHCP_STATUS = 0x10


# fmt: off
# GATEWAY CONFIGURATION MSG
ConfigurationSetMtu = Struct(
    "mtu_size" / Int16ul,
)

ConfigurationSetMacAddr = Struct(
    "mac_address" / MacAddressAdapter(Bytes(6)),
)

ConfigurationSetDnsIpAddr = Struct(
    "dns_ip_address" / IpAddressAdapter(Bytes(4)),
)

ConfigurationSetServerAddrAndPortNr = Struct(
    "server_port_number" / Int16ul,
    "server_address_length" / Int8ul,
    "server_address" / PaddedString(this.server_address_length, "utf8"),
)

ConfigurationSetReconnectInterval = Struct(
    "reconnect_interval" / Int16ul,
)

ConfigurationSetIpAddr = Struct(
    "ip_address" / IpAddressAdapter(Bytes(4)),
)

ConfigurationSetGatewayIpAddr = Struct(
    "gateway_ip_address" / IpAddressAdapter(Bytes(4)),
)

ConfigurationSetNetmask = Struct(
    "netmask" / Int8ul,
)

ConfigurationSetWithoutOptional = Struct(
    "mtu_size" / Int16ul,
    "mac_address" / MacAddressAdapter(Bytes(6)),
    "dns_ip_address" / IpAddressAdapter(Bytes(4)),
    "server_port_number" / Int16ul,
    "reconnect_interval" / Int16ul,
    "server_address_length" / Int8ul,
    "server_address" / PaddedString(this.server_address_length, "utf8"),
)

ConfigurationSetWithOptional = Struct(
    Embedded(ConfigurationSetWithoutOptional),
    "ip_address" / IpAddressAdapter(Bytes(4)),
    "gateway_ip_address" / IpAddressAdapter(Bytes(4)),
    "netmask" / Int8ul,
)

ConfigurationSet = Select(
    ConfigurationSetWithOptional,
    ConfigurationSetWithoutOptional
)

ConfigurationStatus = Struct(
    "chip_revision_id" / Int8ul,
    Embedded(ConfigurationSetWithOptional),
)

# GATEWAY CONFIGURATION DHCP MSG
ConfigurationDhcpSet = Struct(
    "dhcp_enable" / Flag,
)

ConfigurationDhcpStatus = ConfigurationDhcpSet

# GATEWAY PACKETS MSG
PacketsStatus = Struct(
    "total_eth_rx_errors" / Int16ul,
    "total_eth_tx_errors" / Int16ul,
    "bandwidth" / Int16ul,
    "connection_state" / BitList(1)
)

GatewayConfigPayload = Struct(
    "subopcode" / EnumAdapter(Int8ul, GatewayConfigServerSubOpcode),
    "payload" / Default(Switch(
        this.subopcode,
        {
            GatewayConfigServerSubOpcode.GATEWAY_CONFIGURATION_SET: ConfigurationSet,
            GatewayConfigServerSubOpcode.GATEWAY_CONFIGURATION_DHCP_SET: ConfigurationDhcpSet,
            GatewayConfigServerSubOpcode.MTU_SIZE_SET: ConfigurationSetMtu,
            GatewayConfigServerSubOpcode.ETHERNET_MAC_ADDRESS_SET: ConfigurationSetMacAddr,
            GatewayConfigServerSubOpcode.IP_ADDRESS_SET: ConfigurationSetIpAddr,
            GatewayConfigServerSubOpcode.GATEWAY_IP_ADDRESS_SET: ConfigurationSetGatewayIpAddr,
            GatewayConfigServerSubOpcode.NETMASK_SET: ConfigurationSetNetmask,
            GatewayConfigServerSubOpcode.DNS_IP_ADDRESS_SET: ConfigurationSetDnsIpAddr,
            GatewayConfigServerSubOpcode.SERVER_ADDRESS_AND_PORT_NUMBER_SET: ConfigurationSetServerAddrAndPortNr,
            GatewayConfigServerSubOpcode.RECONNECT_INTERVAL_SET: ConfigurationSetReconnectInterval,
            GatewayConfigServerSubOpcode.GATEWAY_CONFIGURATION_STATUS: ConfigurationStatus,
            GatewayConfigServerSubOpcode.GATEWAY_PACKETS_STATUS: PacketsStatus,
            GatewayConfigServerSubOpcode.GATEWAY_CONFIGURATION_DHCP_STATUS: ConfigurationDhcpStatus
        },
    ), None)
)

GatewayConfigMessage = Struct(
    "opcode" / Const(GatewayConfigServerOpcode.OPCODE, Opcode),
    "params" / GatewayConfigPayload
)
# fmt: on
