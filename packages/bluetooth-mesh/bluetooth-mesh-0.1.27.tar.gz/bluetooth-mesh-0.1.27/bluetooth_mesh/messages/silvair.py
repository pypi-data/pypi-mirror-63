import enum

import construct
from construct import (
    BitsInteger,
    BitStruct,
    Bytes,
    Const,
    Flag,
    Int8ul,
    Int16ul,
    Int32ul,
    PaddedString,
    Padding,
    Rebuild,
    Struct,
    Switch,
    len_,
    this,
)

from bluetooth_mesh.messages.util import EnumAdapter
from pymeshd.messages.hci import LEAdvertisingData
from pymeshd.messages.util import MacAddressAdapter


class AdvType(enum.IntEnum):
    ADV_IND = 0x00
    ADV_DIRECT_IND = 0x01
    ADV_NONCONN_IND = 0x02


class Phy(enum.IntEnum):
    _1MBIT = 0x03
    _2MBIT = 0x04
    NONE = 0xFF


class Pwr(enum.IntEnum):
    PLUS_8_DBM = 0x08
    PLUS_7_DBM = 0x07
    PLUS_6_DBM = 0x06
    PLUS_5_DBM = 0x05
    PLUS_4_DBM = 0x04
    PLUS_3_DBM = 0x03
    PLUS_2_DBM = 0x02
    ZERO_DBM = 0x00
    MINUS_4_DB = 0xFC
    MINUS_8_DBM = 0xF8
    MINUS_12_DBM = 0xF4
    MINUS_16_DBM = 0xF0
    MINUS_20_DBM = 0xEC
    MINUS_30_DBM = 0xFF
    MINUS_40_DBM = 0xD8


class PacketType(enum.IntEnum):
    EVT_RX = 0x06
    CMD_TX = 0x18
    CMD_RX = 0x19
    CMD_BOOTLOADER = 0x1A
    CMD_FILTER = 0x1B
    EVT_RESET = 0x1C
    CMD_KEEP_ALIVE = 0x1D


def rebuild_adv_hdr_size(obj):
    adv_addr = MacAddressAdapter(Bytes(6)).build(obj._.address)
    adv_data = LEAdvertisingData.build(obj._.adv_data)

    return len(adv_addr) + len(adv_data)


# fmt:off
AdvHdr = BitStruct(
    "rx_add" / Flag,
    "tx_add" / Flag,
    Padding(2),
    "type" / EnumAdapter(BitsInteger(4), AdvType),
    "size" / Rebuild(BitsInteger(8), rebuild_adv_hdr_size),
)

RxEvtHdr = Struct(
    "hdr_len" / Const(10, Int8ul),
    "crc" / Rebuild(Int8ul, lambda obj: 0),
    "channel" / Int8ul,
    "rssi" / Int8ul,
    "counter" / Rebuild(Int16ul, lambda obj: 0),
    "timestamp" / Int32ul,
)

RxEvtPld = Struct(
    "access_address" / Const(bytes.fromhex('8e89bed6'), Bytes(4)),
    "header" / AdvHdr,
    Padding(1),
    "address" / MacAddressAdapter(Bytes(6)),
    "adv_data" / LEAdvertisingData,
)

TxCmdHdr = Struct(
    "hdr_len" / Const(13, Int8ul),
    "channels" / Bytes(8),
    "phy" / EnumAdapter(Int8ul, Phy),
    "pwr" / EnumAdapter(Int8ul, Pwr),
    "counter" / Rebuild(Int16ul, lambda obj: 0),
)

TxCmdPld = Struct(
    "access_address" / Const(bytes.fromhex('8e89bed6'), Bytes(4)),
    "header" / AdvHdr,
    Padding(1),
    "address" / MacAddressAdapter(Bytes(6)),
    "adv_data" / LEAdvertisingData,
)

KeepAliveCmdPld = Struct(
    "silvair_version_len" / Rebuild(Int8ul, len_(this.silvair_version)),
    "silvair_version" / PaddedString(23, 'ascii'),
    "reset_reason" / Int32ul,
    "uptime" / Int32ul,
    "last_fault_len" / Rebuild(Int8ul, len_(this.last_fault)),
    "last_fault" / PaddedString(128, 'ascii'),
)

Hdr = Switch(
    this.pkt_hdr.type,
    {
        PacketType.EVT_RX: RxEvtHdr,
        PacketType.CMD_TX: TxCmdHdr,
    },
    default=Struct(),
)

Pld = Switch(
    this.pkt_hdr.type,
    {
        PacketType.EVT_RX: RxEvtPld,
        PacketType.CMD_TX: TxCmdPld,
        PacketType.CMD_KEEP_ALIVE: KeepAliveCmdPld,
    },
    default=Struct(),
)


def rebuild_pld_len(obj):
    hdr = Hdr.cases.get(obj.type)
    pld = Pld.cases.get(obj.type)
    return (hdr.sizeof() if hdr else 0) + (len(pld.build(obj._.pld)) if pld else 0)


PktHdr = Struct(
    "hdr_len" / Const(6, Int8ul),
    "pld_len" / Rebuild(Int8ul, rebuild_pld_len),
    "version" / Const(1, Int8ul),
    "counter" / Rebuild(Int16ul, lambda obj: 0),
    "type" / EnumAdapter(Int8ul, PacketType),
)


Packet = Struct(
    "pkt_hdr" / PktHdr,
    "hdr" / Hdr,
    "pld" / Pld,
)
# fmt: on
