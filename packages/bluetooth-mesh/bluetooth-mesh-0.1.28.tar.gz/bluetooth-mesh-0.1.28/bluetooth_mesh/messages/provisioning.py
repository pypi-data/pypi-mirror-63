from enum import IntEnum

from construct import (
    BitsInteger,
    Bytes,
    Const,
    GreedyBytes,
    Int8ul,
    Int16ub,
    Int32ub,
    Padding,
    Select,
    Struct,
    Switch,
    this,
)

from bluetooth_mesh.messages.util import EnumAdapter
from pymeshd.messages.util import EmbeddedBitStruct


class GenericControlFormat(IntEnum):
    TRANSACTION_START = 0b00
    TRANSACTION_ACK = 0b01
    TRANSACTION_CONT = 0b10
    BEARER_CONTROL = 0b11


# fmt: off
GPCF = EnumAdapter(BitsInteger(2), GenericControlFormat)


TransactionStart = Struct(
    *EmbeddedBitStruct(
        "_",
        "segn" / BitsInteger(6),
        "gpcf" / Const(GenericControlFormat.TRANSACTION_START, GPCF),
    ),
    "total_length" / Int16ub,  # TODO: compute / rebuild
    "fcs" / Int8ul,  # TODO: validate / rebuild
    "segment" / GreedyBytes,
)


TransactionAck = Struct(
    *EmbeddedBitStruct(
        "_",
        "padding" / Padding(6),
        "gpcf" / Const(GenericControlFormat.TRANSACTION_ACK, GPCF),
    ),
)


TransactionCont = Struct(
    *EmbeddedBitStruct(
        "_",
        "segment_index" / BitsInteger(6),
        "gpcf" / Const(GenericControlFormat.TRANSACTION_CONT, GPCF),
    ),
    "segment" / GreedyBytes,
)


class BearerOpcode(IntEnum):
    LINK_OPEN = 0x00
    LINK_ACK = 0x01
    LINK_CLOSE = 0x02


LinkOpen = Struct(
    "device_uuid" / Bytes(16),
)


class LinkCloseReason(IntEnum):
    SUCCESS = 0x00
    TIMEOUT = 0x01
    FAIL = 0x02


LinkClose = Struct(
    "reason" / EnumAdapter(Int8ul, LinkCloseReason),
)


BearerControl = Struct(
    *EmbeddedBitStruct(
        "_",
        "bearer_opcode" / EnumAdapter(BitsInteger(6), BearerOpcode),
        "gpcf" / Const(GenericControlFormat.BEARER_CONTROL, GPCF),
    ),
    "parameters" / Switch(
        this.bearer_opcode,
        {
            BearerOpcode.LINK_OPEN: LinkOpen,
            BearerOpcode.LINK_CLOSE: LinkClose,
        },
    )
)


GenericPDU = Select(
    TransactionStart,
    TransactionAck,
    TransactionCont,
    BearerControl,
)


Adv = Struct(
    "link_id" / Int32ub,
    "transaction" / Int8ul,
    "pdu" / GenericPDU,
)
# fmt: on
