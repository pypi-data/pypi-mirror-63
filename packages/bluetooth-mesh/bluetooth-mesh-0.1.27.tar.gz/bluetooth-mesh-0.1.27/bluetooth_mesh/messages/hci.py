from enum import IntEnum

from construct import (
    Byte,
    Bytes,
    CString,
    GreedyRange,
    Int8ul,
    Int16ul,
    Int24ul,
    Int32ul,
    Padded,
    Rebuild,
    Select,
    Struct,
    Switch,
    len_,
    this,
)

from bluetooth_mesh.messages.util import EnumAdapter

from .util import BitList, MacAddressAdapter, RebuildLength, SwitchLength


class CommandOpcode(IntEnum):
    NONE = 0x0000

    # 7.1 Link Policy Commands, OGF 0x01
    INQUIRY = 0x0401
    INQUIRY_CANCEL = 0x0402
    PERIODIC_INQUIRY_MODE = 0x0403
    EXIT_PERIODIC_INQUIRY_MODE = 0x0404
    CREATE_CONNECTION = 0x0405
    DISCONNECT = 0x0406
    ADD_SCO_CONNECTION = 0x0407
    ACCEPT_CONNECTION_REQUEST = 0x0409
    REJECT_CONNECTION_REQUEST = 0x040A
    LINK_KEY_REQUEST_REPLY = 0x040B
    LINK_KEY_REQUEST_NEGATIVE_REPLY = 0x040C
    PIN_CODE_REQUEST_REPLY = 0x040D
    PIN_CODE_REQUEST_NEGATIVE_REPLY = 0x040E
    CHANGE_CONNECTION_PACKET_TYPE = 0x040F
    AUTHENTICATION_REQUESTED = 0x0411
    SET_CONNECTION_ENCRYPTION = 0x0413
    CHANGE_CONNECTION_LINK_KEY = 0x0415
    MASTER_LINK_KEY = 0x0417
    REMOTE_NAME_REQUEST = 0x0419
    READ_REMOTE_SUPPORTED_FEATURES = 0x041B
    READ_REMOTE_VERSION_INFORMATION = 0x041D
    READ_CLOCK_OFFSET = 0x041F

    # 7.2 Link Policy Commands, OGF 0x02
    HOLD_MODE = 0x0801
    SNIFF_MODE = 0x0803
    EXIT_SNIFF_MODE = 0x0804
    PARK_MODE = 0x0805
    EXIT_PARK_MODE = 0x0806
    QOS_SETUP = 0x0807
    ROLE_DISCOVERY = 0x0809
    SWITCH_ROLE = 0x080B
    READ_LINK_POLICY_SETTINGS = 0x080C
    WRITE_LINK_POLICY_SETTINGS = 0x080D
    READ_DEFAULT_LINK_POLICY_SETTINGS = 0x080E
    WRITE_DEFAULT_LINK_POLICY_SETTINGS = 0x080F
    FLOW_SPECIFICATION = 0x0810
    SNIFF_SUBRATING = 0x0811

    # 7.3 Controller & Baseband Commands, OGF 0x03
    SET_EVENT_MASK = 0x0C01
    RESET = 0x0C03
    SET_EVENT_FILTER = 0x0C05
    FLUSH = 0x0C08
    READ_PIN_TYPE = 0x0C09
    WRITE_PIN_TYPE = 0x0C0A
    CREATE_NEW_UNIT_KEY = 0x0C0B
    READ_STORED_LINK_KEY = 0x0C0D
    WRITE_STORED_LINK_KEY = 0x0C11
    DELETE_STORED_LINK_KEY = 0x0C12
    CHANGE_LOCAL_NAME = 0x0C13
    READ_LOCAL_NAME = 0x0C14
    READ_CONNECTION_ACCEPT_TIMEOUT = 0x0C15
    WRITE_CONNECTION_ACCEPT_TIMEOUT = 0x0C16
    READ_PAGE_TIMEOUT = 0x0C17
    WRITE_PAGE_TIMEOUT = 0x0C18
    READ_SCAN_ENABLE = 0x0C19
    WRITE_SCAN_ENABLE = 0x0C1A
    READ_PAGE_SCAN_ACTIVITY = 0x0C1B
    WRITE_PAGE_SCAN_ACTIVITY = 0x0C1C
    READ_INQUIRY_SCAN_ACTIVITY = 0x0C1D
    WRITE_INQUIRY_SCAN_ACTIVITY = 0x0C1E
    READ_AUTHENTICATION_ENABLE = 0x0C1F
    WRITE_AUTHENTICATION_ENABLE = 0x0C20
    READ_CLASS_OF_DEVICE = 0x0C23
    WRITE_CLASS_OF_DEVICE = 0x0C24
    READ_VOICE_SETTING = 0x0C25
    WRITE_VOICE_SETTING = 0x0C26
    READ_AUTOMATIC_FLUSH_TIMEOUT = 0x0C27
    WRITE_AUTOMATIC_FLUSH_TIMEOUT = 0x0C28
    READ_NUM_BROADCAST_RETRANSMISSIONS = 0x0C29
    WRITE_NUM_BROADCAST_RETRANSMISSIONS = 0x0C2A
    READ_HOLD_MODE_ACTIVITY = 0x0C2B
    WRITE_HOLD_MODE_ACTIVITY = 0x0C2C
    READ_TRANSMIT_POWER_LEVEL = 0x0C2D
    READ_SYNCHRONOUS_FLOW_CONTROL_ENABLE = 0x0C2E
    WRITE_SYNCHRONOUS_FLOW_CONTROL_ENABLE = 0x0C2F
    SET_CONTROLLER_TO_HOST_FLOW_CONTROL = 0x0C31
    HOST_BUFFER_SIZE = 0x0C33
    HOST_NUMBER_OF_COMPLETED_PACKETS = 0x0C35
    READ_LINK_SUPERVISION_TIMEOUT = 0x0C36
    WRITE_LINK_SUPERVISION_TIMEOUT = 0x0C37
    READ_NUMBER_OF_SUPPORTED_IAC = 0x0C38
    READ_CURRENT_IAC_LAP = 0x0C39
    WRITE_CURRENT_IAC_LAP = 0x0C3A
    SET_AFH_HOST_CHANNEL_CLASSIFICATION = 0x0C3F
    READ_INQUIRY_SCAN_TYPE = 0x0C42
    WRITE_INQUIRY_SCAN_TYPE = 0x0C43
    READ_INQUIRY_MODE = 0x0C44
    WRITE_INQUIRY_MODE = 0x0C45
    READ_PAGE_SCAN_TYPE = 0x0C46
    WRITE_PAGE_SCAN_TYPE = 0x0C47
    READ_AFH_CHANNEL_ASSESSMENT_MODE = 0x0C48
    WRITE_AFH_CHANNEL_ASSESSMENT_MODE = 0x0C49
    READ_EXTENDED_INQUIRY_RESPONSE = 0xC51
    WRITE_EXTENDED_INQUIRY_RESPONSE = 0xC52
    REFRESH_ENCRYPTION_KEY = 0x0C53
    READ_SIMPLE_PAIRING_MODE = 0x0C55
    WRITE_IMPLE_PAIRING_MODE = 0x0C56
    READ_LOCAL_OOB_DATA = 0x0C57
    READ_INQUIRY_RESPONSE_TRANSMIT_POWER_LEVEL = 0x0C58
    WRITE_INQUIRY_TRANSMIT_POWER_LEVEL = 0x0C59
    SEND_KEYPRESS_NOTIFICATION = 0x0C60
    READ_DEFAULT_ERRONEOUS_DATA_REPORTING = 0x0C5A
    WRITE_DEFAULT_ERRONEOUS_DATA_REPORTING = 0x0C5B
    ENHANCED_FLUSH = 0x0C5F
    READ_LOGICAL_LINK_ACCEPT_TIMEOUT = 0x0C61
    WRITE_LOGICAL_LINK_ACCEPT_TIMEOUT = 0x0C62
    SET_EVENT_MASK_PAGE_2 = 0x0C63
    # ...

    # Informational Parameters, OGF 0x04
    READ_LOCAL_VERSION_INFORMATION = 0x1001
    READ_LOCAL_SUPPORTED_COMMANDS = 0x1002
    READ_LOCAL_SUPPORTED_FEATURES = 0x1003
    READ_LOCAL_EXTENDED_FEATURES = 0x1004
    READ_BUFFER_SIZE = 0x1005
    READ_BD_ADDR = 0x1009
    READ_DATA_BLOCK_SIZE = 0x100A
    READ_LOCAL_SUPPORTED_CODECS = 0x100B

    # Status Parameters, OGF 0x05
    READ_FAILED_CONTACT_COUNTER = 0x1401
    RESET_FAILED_CONTACT_COUNTER = 0x1402
    READ_LINK_QUALITY = 0x1403
    READ_RSSI = 0x1405
    READ_AFH_CHANNEL_MAP = 0x1406
    READ_CLOCK = 0x1407
    READ_ENCRYPTION_KEY_SIZE = 0x1408
    READ_LOCAL_AMP_INFO = 0x1409
    READ_LOCAL_AMP_ASSOC = 0x140A
    READ_REMOTE_AMP_ASSOC = 0x140B
    GET_MWS_TRANSPORT_LAYER_CONFIGURATION = 0x140C
    SET_TRIGGERED_CLOCK_CAPTURE = 0x140D

    # Testing Commands, OGF 0x06
    READ_LOOPBACK_MODE = 0x1801
    WRITE_LOOPBACK_MODE = 0x1802
    ENABLE_DEVICE_UNDER_TEST_MODE = 0x1803
    WRITE_SIMPLE_PAIRING_DEBUG_MODE = 0x1804
    ENABLE_AMP_RECEIVER_REPORTS = 0x1807
    AMP_TEST_END = 0x1808
    AMP_TEST = 0x1809
    WRITE_SECURE_CONNECTIONS_TEST_MODE = 0x180A

    # LE Controler Commands, OGF 0x08
    LE_SET_EVENT_MASK = 0x2001
    LE_READ_BUFFER_SIZE = 0x2002
    LE_READ_LOCAL_SUPPORTED_FEATURES = 0x2003
    LE_SET_RANDOM_ADDRESS = 0x2005
    LE_SET_ADVERTISING_PARAMETERS = 0x2006
    LE_READ_ADVERTISING_CHANNEL_TX_POWER = 0x2007
    LE_SET_ADVERTISING_DATA = 0x2008
    LE_SET_SCAN_RESPONSE_DATA = 0x2009
    LE_SET_ADVERTISING_ENABLE = 0x200A
    LE_SET_SCAN_PARAMETERS = 0x200B
    LE_SET_SCAN_ENABLE = 0x200C
    LE_CREATE_CONNECTION = 0x200D
    LE_CREATE_CONNECTION_CANCEL = 0x200E
    LE_READ_WHITE_LIST_SIZE = 0x200F
    LE_CLEAR_WHITE_LIST = 0x2010
    LE_ADD_DEVICE_TO_WHITE_LIST = 0x2011
    LE_REMOVE_DEVICE_FROM_WHITE_LIST = 0x2012
    LE_CONNECTION_UPDATE = 0x2013
    LE_SET_HOST_CHANNEL_CLASSIFICATION = 0x2014
    LE_READ_CHANNEL_MAP = 0x2015
    LE_READ_REMOTE_USED_FEATURES = 0x2016
    LE_ENCRYPT = 0x2017
    LE_RAND = 0x2018
    LE_START_ENCRYPTION = 0x2019
    LE_LONG_TERM_KEY_REQUESTED_REPLY = 0x201A
    LE_LONG_TERM_KEY_REQUESTED_NEGATIVE_REPLY = 0x201B
    LE_READ_SUPPORTED_STATES = 0x201C
    LE_RECEIVER_TEST = 0x201D
    LE_TRANSMITTER_TEST = 0x201E
    LE_TEST_END_COMMAND = 0x201F
    LE_REMOTE_CONNECTION_PARAMETER_REQUEST_REPLY = 0x2020
    LE_REMOTE_CONNECTION_PARAMETER_REQUEST_NEGATIVE_REPLY = 0x2021
    LE_SET_DATA_LENGTH = 0x2022
    LE_READ_SUGGESTED_DEFAULT_DATA_LENGTH = 0x2023
    LE_WRITE_SUGGESTED_DEFAULT_DATA_LENGTH = 0x2024
    LE_READ_LOCAL_P256_PUBLIC_KEY_37_0X2025_LE_GENERATE_DHKEY = 0x2026
    LE_ADD_DEVICE_TO_RESOLVING_LIST = 0x2027
    LE_REMOVE_DEVICE_FROM_RESOLVING_LIST = 0x2028
    LE_CLEAR_RESOLVING_LIST = 0x2029
    LE_READ_RESOLVING_LIST_SIZE = 0x202A
    LE_READ_PEER_RESOLVABLE_ADDRESS = 0x202B
    LE_READ_LOCAL_RESOLVABLE_ADDRESS = 0x202C
    LE_SET_ADDRESS_RESOLUTION_ENABLE = 0x202D
    LE_SET_RESOLVABLE_PRIVATE_ADDRESS_TIMEOUT = 0x202E
    LE_READ_MAXIMUM_DATA_LENGTH = 0x202F
    LE_READ_PHY = 0x2030
    LE_SET_DEFAULT_PHY = 0x2031
    LE_ENHANCED_RECEIVER_TEST = 0x2033
    LE_ENHANCED_TRANSMITTER_TEST = 0x2034
    LE_ADVERTISING_SET_RANDOM_ADDRESS = 0x2035
    LE_SET_EXTENDED_ADVERTISING_PARAMETERS = 0x2036
    LE_SET_EXTENDED_ADVERTISING_DATA = 0x2037
    LE_SET_EXTENDED_SCAN_RESPONSE_DATA = 0x2038
    LE_SET_EXTENDED_ADVERTISING_ENABLE = 0x2039
    LE_READ_MAXIMUM_ADVERTISING_DATA_LENGTH = 0x203A
    LE_READ_NUMBER_OF_SUPPORTED_ADVERTISING_SETS = 0x203B
    LE_REMOVE_ADVERTISING_SET = 0x203C
    LE_CLEAR_ADVERTISING_SETS = 0x203D
    LE_SET_PERIODIC_ADVERTISING_PARAMETERS = 0x203E
    LE_SET_PERIODIC_ADVERTISING_DATA = 0x203F
    LE_SET_PERIODIC_ADVERTISING_ENABLE = 0x2040
    LE_SET_EXTENDED_SCAN_PARAMETERS = 0x2041
    LE_SET_EXTENDED_SCAN_ENABLE = 0x2042
    LE_EXTENDED_CREATE_CONNECTION = 0x2043
    LE_PERIODIC_ADVERTISING_CREATE_SYNC = 0x2044
    LE_PERIODIC_ADVERTISING_CREATE_SYNC_CANCEL = 0x2045
    LE_PERIODIC_ADVERTISING_TERMINATE_SYNC = 0x2046
    LE_ADD_DEVICE_TO_PERIODIC_ADVERTISER_LIST = 0x2047
    LE_REMOVE_DEVICE_FROM_PERIODIC_ADVERTISER_LIST = 0x2048
    LE_CLEAR_PERIODIC_ADVERTISER_LIST = 0x2049
    LE_READ_PERIODIC_ADVERTISER_LIST = 0x204A
    LE_READ_TRANSMIT_POWER = 0x204B
    LE_READ_RF_PATH_COMPENSATION = 0x204C
    LE_WRITE_RF_PATH_COMPENSATION = 0x204D
    LE_SET_PRIVACY_MODE = 0x204E


class EventType(IntEnum):
    INQUIRY_COMPLETE = 0x01
    INQUIRY_RESULT = 0x02
    CONNECTION_COMPLETE = 0x03
    CONNECTION_REQUEST = 0x04
    DISCONNECTION_COMPLETE = 0x05
    AUTHENTICATION_COMPLETE = 0x06
    REMOTE_NAME_REQUEST_COMPLETE = 0x07
    ENCRYPTION_CHANGE = 0x08
    CHANGE_CONNECTION_LINK_KEY_COMPLETE = 0x09
    MASTER_LINK_KEY_COMPLETE = 0x0A
    READ_REMOTE_SUPPORTED_FEATURES_COMPLETE = 0x0B
    READ_REMOTE_VERSION_INFORMATION_COMPLETE = 0x0C
    QOS_SETUP_COMPLETE = 0x0D
    COMMAND_COMPLETE = 0x0E
    COMMAND_STATUS = 0x0F
    HARDWARE_ERROR = 0x10
    FLUSH_OCCURED = 0x11
    ROLE_CHANGE = 0x12
    NUMBER_OF_COMPLETED_PACKETS = 0x13
    MODE_CHANGE = 0x14
    RETURN_LINK_KEYS = 0x15
    PIN_CODE_REQUEST = 0x16
    LINK_KEY_REQUEST = 0x17
    LINK_KEY_NOTIFICATION = 0x18
    LOOPBACK_COMMAND = 0x19
    DATA_BUFFER_OVERFLOW = 0x1A
    MAX_SLOTS_CHANGE = 0x1B
    READ_CLOCK_OFFSET_COMPLETE = 0x1C
    CONNECTION_PACKET_TYPE_CHANGED = 0x1D
    QOS_VIOLATION = 0x1E
    PAGE_SCAN_REPETITION_MODE_CHANGE = 0x20
    FLOW_SPECIFICATION_COMPLETE = 0x21
    INQUIRY_RESULT_WITH_RSSI = 0x22
    READ_REMOTE_EXTENDED_FEATURES_COMPLETE = 0x23
    SYNCHRONOUS_CONNECTION_COMPLETE = 0x2C
    SYNCHRONOUS_CONNECTION_CHANGED = 0x2D
    SNIFF_SUBRATING = 0x2E
    EXTENDED_INQUIRY_RESULT = 0x2F
    ENCRYPTION_KEY_REFRESH_COMPLETE = 0x30
    IO_CAPABILITY_REQUEST = 0x31
    IO_CAPABILITY_RESPONSE = 0x32
    USER_CONFIRMATION_REQUEST = 0x33
    USER_PASSKEY_REQUEST = 0x34
    REMOTE_OOB_DATA_REQUEST = 0x35
    SIMPLE_PAIRING_COMPLETE = 0x36
    LINK_SUPERVISION_TIMEOUT_CHANGED = 0x38
    ENHANCED_FLUSH_COMPLETE = 0x39
    USER_PASSKEY_NOTIFICATION = 0x3B
    KEYPRESS_NOTIFICATION = 0x3C
    REMOTE_HOST_SUPPORTED_FEATURES_NOTIFICATION = 0x3D
    PHYSICAL_LINK_COMPLETE = 0x40
    CHANNEL_SELECTED = 0x41
    DISCONNECTION_PHYSICAL_LINK_COMPLETE = 0x42
    PHYSICAL_LINK_LOSS_EARLY_WARNING = 0x43
    PHYSICAL_LINK_RECOVERY = 0x44
    LOGICAL_LINK_COMPLETE = 0x45
    DISCONNECTION_LOGICAL_LINK_COMPLETE = 0x46
    FLOW_SPEC_MODIFY_COMPLETE = 0x47
    NUMBER_OF_COMPLETED_DATA_BLOCKS = 0x48
    SHORT_RANGE_MODE_CHANGE_COMPLETE = 0x4C
    AMP_STATUS_CHANGE = 0x4D
    AMP_START_TEST = 0x49
    AMP_TEST_END = 0x4A
    AMP_RECEIVER_REPORT = 0x4B
    LE_META_EVENT = 0x3E
    TRIGGERED_CLOCK_CAPTURE = 0x4E
    SYNCHRONIZATION_TRAIN_COMPLETE = 0x4F
    SYNCHRONIZATION_TRAIN_RECEIVED = 0x50
    CONNECTIONLESS_SLAVE_BROADCAST_RECEIVE = 0x51
    CONNECTIONLESS_SLAVE_BROADCAST_TIMEOUT = 0x52
    TRUNCATED_PAGE_COMPLETE = 0x53
    SLAVE_PAGE_RESPONSE_TIMEOUT = 0x54
    CONNECTIONLESS_SLAVE_BROADCAST_CHANNEL_MAP_CHANGE = 0x55
    INQUIRY_RESPONSE_NOTIFICATION = 0x56
    AUTHENTICATED_PAYLOAD_TIMEOUT_EXPIRED = 0x57
    SAM_STATUS_CHANGE = 0x58


class ErrorCode(IntEnum):
    SUCCESS = 0x00
    UNKNOWN_HCI_COMMAND = 0x01
    UNKNOWN_CONNECTION_IDENTIFIER = 0x02
    HARDWARE_FAILURE = 0x03
    PAGE_TIMEOUT = 0x04
    AUTHENTICATION_FAILURE = 0x05
    PIN_OR_KEY_MISSING = 0x06
    MEMORY_CAPACITY_EXCEEDED = 0x07
    CONNECTION_TIMEOUT = 0x08
    CONNECTION_LIMIT_EXCEEDED = 0x09
    SYNCHRONOUS_CONNECTION_LIMIT_TO_A_DEVICE_EXCEEDED = 0x0A
    CONNECTION_ALREADY_EXISTS = 0x0B
    COMMAND_DISALLOWED = 0x0C
    CONNECTION_REJECTED_DUE_TO_LIMITED_RESOURCES = 0x0D
    CONNECTION_REJECTED_DUE_TO_SECURITY_REASONS = 0x0E
    CONNECTION_REJECTED_DUE_TO_UNACCEPTABLE_BD_ADDR = 0x0F
    CONNECTION_ACCEPT_TIMEOUT_EXCEEDED = 0x10
    UNSUPPORTED_FEATURE_OR_PARAMETER_VALUE = 0x11
    INVALID_HCI_COMMAND_PARAMETERS = 0x12
    REMOTE_USER_TERMINATED_CONNECTION = 0x13
    REMOTE_DEVICE_TERMINATED_CONNECTION_DUE_TO_LOW_RESOURCES = 0x14
    REMOTE_DEVICE_TERMINATED_CONNECTION_DUE_TO_POWER_OFF = 0x15
    CONNECTION_TERMINATED_BY_LOCAL_HOST = 0x16
    REPEATED_ATTEMPTS = 0x17
    PAIRING_NOT_ALLOWED = 0x18
    UNKNOWN_LMP_PDU = 0x19
    UNSUPPORTED_REMOTE_OR_LMP_FEATURE = 0x1A
    SCO_OFFSET_REJECTED = 0x1B
    SCO_INTERVAL_REJECTED = 0x1C
    SCO_AIR_MODE_REJECTED = 0x1D
    INVALID_LMP_OR_LL_PARAMETERS = 0x1E
    UNSPECIFIED_ERROR = 0x1F
    UNSUPPORTED_LMP_OR_LL_PARAMETER_VALUE = 0x20
    ROLE_CHANGE_NOT_ALLOWED = 0x21
    LMP_OR_LL_RESPONSE_TIMEOUT = 0x22
    LMP_ERROR_TRANSACTION_COLLISION_OR_LL_PROCEDURE_COLLISION = 0x23
    LMP_PDU_NOT_ALLOWED = 0x24
    ENCRYPTION_MODE_NOT_ACCEPTABLE = 0x25
    LINK_KEY_CANNOT_BE_CHANGED = 0x26
    REQUESTED_QOS_NOT_SUPPORTED = 0x27
    INSTANT_PASSED = 0x28
    PAIRING_WITH_UNIT_KEY_NOT_SUPPORTED = 0x29
    DIFFERENT_TRANSACTION_COLLISION = 0x2A
    RESERVED_FOR_FUTURE_USE = 0x2B
    QOS_UNACCEPTABLE_PARAMETER = 0x2C
    QOS_REJECTED = 0x2D
    CHANNEL_CLASSIFICATION_NOT_SUPPORTED = 0x2E
    INSUFFICIENT_SECURITY = 0x2F
    PARAMETER_OUT_OF_MANDATORY_RANGE = 0x30
    ROLE_SWITCH_PENDING = 0x32
    RESERVED_SLOT_VIOLATION = 0x34
    ROLE_SWITCH_FAILED = 0x35
    EXTENDED_INQUIRY_RESPONSE_TOO_LARGE = 0x36
    SECURE_SIMPLE_PAIRING_NOT_SUPPORTED_BY_HOST = 0x37
    HOST_BUSY_PAIRING = 0x38
    CONNECTION_REJECTED_DUE_TO_NO_SUITABLE_CHANNEL_FOUND = 0x39
    CONTROLLER_BUSY = 0x3A
    UNACCEPTABLE_CONNECTION_PARAMETERS = 0x3B
    ADVERTISING_TIMEOUT = 0x3C
    CONNECTION_TERMINATED_DUE_TO_MIC_FAILURE = 0x3D
    CONNECTION_FAILED_TO_BE_ESTABLISHED = 0x3E
    MAC_CONNECTION_FAILED = 0x3F
    COARSE_CLOCK_ADJUSTMENT_REJECTED_BUT_WILL_TRY_TO_ADJUST_USING_CLOCK_DRAGGING = (
        0x40  # pylint: disable=C0103
    )
    TYPE0_SUBMAP_NOT_DEFINED = 0x41
    UNKNOWN_ADVERTISING_IDENTIFIER = 0x42
    LIMIT_REACHED = 0x43
    OPERATION_CANCELLED_BY_HOST = 0x44


class LEMetaEventType(IntEnum):
    LE_CONNECTION_COMPLETE = 0x01
    LE_ADVERTISING_REPORT = 0x02
    LE_CONNECTION_UPDATE_COMPLETE = 0x03
    LE_READ_REMOTE_FEATURES_COMPLETE = 0x04
    LE_LONG_TERM_KEY_REQUEST = 0x05
    LE_REMOTE_CONNECTION_PARAMETER_REQUEST = 0x06
    LE_DATA_LENGTH_CHANGE = 0x07
    LE_READ_LOCAL_P256_PUBLIC_KEY_COMPLETE = 0x08
    LE_GENERATE_DHKEY_COMPLETE = 0x09
    LE_ENHANCED_CONNECTION_COMPLETE = 0x0A
    LE_DIRECTED_ADVERTISING_REPORT = 0x0B
    LE_PHY_UPDATE_COMPLETE = 0x0C
    LE_EXTENDED_ADVERTISING_REPORT = 0x0D
    LE_PERIODIC_ADVERTISING_SYNC_ESTABLISHED = 0x0E
    LE_PERIODIC_ADVERTISING_REPORT = 0x0F
    LE_PERIODIC_ADVERTISING_SYNC_LOST = 0x10
    LE_SCAN_TIMEOUT = 0x11
    LE_ADVERTISIG_SET_TERMINATED = 0x12
    LE_SCAN_REQUEST_RECEIVED = 0x13
    LE_CHANNEL_SELECTION_ALGORITHM = 0x14


class LEAdvertisingDataTag(IntEnum):
    FLAGS = 0x01
    INCOMPLETE_LIST_OF_16BIT_SERVICE_CLASS_UUIDS = 0x02
    COMPLETE_LIST_OF_16BIT_SERVICE_CLASS_UUIDS = 0x03
    INCOMPLETE_LIST_OF_32BIT_SERVICE_CLASS_UUIDS = 0x04
    COMPLETE_LIST_OF_32BIT_SERVICE_CLASS_UUIDS = 0x05
    INCOMPLETE_LIST_OF_128BIT_SERVICE_CLASS_UUIDS = 0x06
    COMPLETE_LIST_OF_128BIT_SERVICE_CLASS_UUIDS = 0x07
    SHORTENED_LOCAL_NAME = 0x08
    COMPLETE_LOCAL_NAME = 0x09
    TX_POWER_LEVEL = 0x0A
    CLASS_OF_DEVICE = 0x0D
    SIMPLE_PAIRING_HASH_C192 = 0x0E
    SIMPLE_PAIRING_RANDOMIZER_R192 = 0x0F
    DEVICE_ID = 0x10
    SECURITY_MANAGER_OUT_OF_BAND_FLAGS = 0x11
    SLAVE_CONNECTION_INTERVAL_RANGE = 0x12
    LIST_OF_16BIT_SERVICE_SOLICITATION_UUIDS = 0x14
    LIST_OF_128BIT_SERVICE_SOLICITATION_UUIDS = 0x15
    SERVICE_DATA = 0x16
    PUBLIC_TARGET_ADDRESS = 0x17
    RANDOM_TARGET_ADDRESS = 0x18
    APPEARANCE = 0x19
    ADVERTISING_INTERVAL = 0x1A
    LE_BLUETOOTH_DEVICE_ADDRESS = 0x1B
    LE_ROLE = 0x1C
    SIMPLE_PAIRING_HASH_C256 = 0x1D
    SIMPLE_PAIRING_RANDOMIZER_R256 = 0x1E
    LIST_OF_32BIT_SERVICE_SOLICITATION_UUIDS = 0x1F
    SERVICE_DATA_32BIT_UUID = 0x20
    SERVICE_DATA_128BIT_UUID = 0x21
    LE_SECURE_CONNECTIONS_CONFIRMATION_VALUE = 0x22
    LE_SECURE_CONNECTIONS_RANDOM_VALUE = 0x23
    URI = 0x24
    INDOOR_POSITIONING = 0x25
    TRANSPORT_DISCOVERY_DATA = 0x26
    LE_SUPPORTED_FEATURES = 0x27
    CHANNEL_MAP_UPDATE_INDICATION = 0x28
    _3D_INFORMATION_DATA = 0x3D

    MESH_PROVISIONING_PDU = 0x29
    MESH_NETWORK_PDU = 0x2A
    MESH_BEACON = 0x2B
    MANUFACTURER_SPECIFIC_DATA = 0xFF


class LEAdvertisingType(IntEnum):
    ADV_IND = 0
    ADV_DIRECT_IND_HIGH_DUTY = 1
    ADV_SCAN_IND = 2
    ADV_NOCONN_IND = 3
    ADV_DIRECT_IND_LOW_DUTY = 4


class LEAddressType(IntEnum):
    PUBLIC = 0
    RANDOM = 1
    RESOLVABLE_PUBLIC = 2
    RESOLVABLE_RANDOM = 3


class LEAdvertisingFilterPolicy(IntEnum):
    CONN_ALL_SCAN_ALL = 0
    CONN_ALL_SCAN_WL = 1
    CONN_WL_SCAN_ALL = 2
    CONN_WL_SCAN_WL = 3


class PacketType(IntEnum):
    COMMAND = 0x01
    ACL_DATA = 0x02
    SYNCHRONOUS_DATA = 0x03
    EVENT = 0x04
    EXTENDED_COMMAND = 0x09
    VENDOR = 0xFF


# fmt: off
CommandOpcodeAdapter = EnumAdapter(Int16ul, CommandOpcode)

EventTypeAdapter = EnumAdapter(Int8ul, EventType)

ErrorCodeAdapter = EnumAdapter(Int8ul, ErrorCode)

LEMetaEventTypeAdapter = EnumAdapter(Int8ul, LEMetaEventType)

LEAdvertisingDataTagAdapter = EnumAdapter(Int8ul, LEAdvertisingDataTag)

PacketTypeAdapter = EnumAdapter(Int8ul, PacketType)

MacAddress = MacAddressAdapter(Byte[6])

DeleteStoredLinkKeyComplete = Struct(
    "num_keys_deleted" / Int16ul,
)

ReadLocalVersionInformation = Struct(
    "hci_revision" / Int16ul,
    "lmp_pal_version" / Int8ul,
    "manufacturer_name" / Int16ul,
    "lmp_pal_subversion" / Int16ul,
)

ReadLocalSupportedCommandsComplete = Struct(
    "supported_commands" / BitList(64)
)

ReadLocalSupportedFeaturesComplete = Struct(
    "features" / BitList(8)
)

ReadLocalExtendedFeaturesComplete = Struct(
    "page_number" / Int8ul,
    "maximum_page_number" / Int8ul,
    "extended_lmp_features" / BitList(8),
)

ReadBufferSizeComplete = Struct(
    "hc_acl_data_packet_length" / Int16ul,
    "hc_syncronous_packet_length" / Int8ul,
    "hc_total_num_acl_data_packets" / Int16ul,
    "hc_total_num_synchronous_data_packets" / Int16ul,
)

ReadBDAddrComplete = Struct(
    "bd_addr" / MacAddress
)

ReadDataBlockSizeComplete = Struct(
    "max_acl_data_packet_length" / Int16ul,
    "data_block_length" / Int16ul,
)

ReadLocalSupportedCodecsComplete = Struct(
    "number_of_supported_codecs" / Int8ul,
    "supported_codecs" / Int8ul[this.number_of_supported_codecs],
    "number_of_supported_vendor_specific_codecs" / Int8ul,
    "vendor_specific_codecs" / Int32ul[this.number_of_supported_vendor_specific_codecs],
)

ReadStoredLocalLinkKeyComplete = Struct(
    "max_num_keys" / Int16ul,
    "num_keys_read" / Int16ul,
)

ReadLocalNameComplete = Struct(
    "local_name" / CString("utf8")
)

ReadPageScanActivityComplete = Struct(
    # TODO: calculate time in seconds (* 0.625 ms)
    "page_scan_interval" / Int16ul,
    "page_scan_window" / Int16ul,
)

ReadClassOfDeviceComplete = Struct(
    "class_of_device" / Int24ul
)

ReadVoiceSettingComplete = Struct(
    "voice_setting" / Int16ul
)

ReadNumberOfSupprtedIACComplete = Struct(
    "num_support_iac" / Int8ul
)

ReadCurrentIACLAPComplete = Struct(
    "num_current_iac" / Int8ul,
    "iac_lap" / Int24ul[this.num_current_iac],
)

ReadPageScanTypeComplete = Struct(
    "page_scan_type" / Int8ul,
)

LEReadBufferSizeComplete = Struct(
    "hc_le_data_packet_length" / Int16ul,
    "hc_total_num_le_data_packets" / Int8ul,
)

LEReadLocalSupportedFeaturesComplete = Struct(
    "le_features" / BitList(8)
)

LEReadAdvertisingChannelTxPowerComplete = Struct(
    "transmit_power_level" / Int8ul
)

LEReadWhiteListSizeComplete = Struct(
    "white_list_size" / Int8ul,
)

LEReadSupportedStatesComplete = Struct(
    "le_states" / BitList(8)
)

LEReadSuggestedDefaultDataLength = Struct(
    "suggested_max_tx_octets" / Int16ul,
    "suggested_max_tx_time" / Int16ul,
)

LEReadMaximumDataLengthComplete = Struct(
    "supported_max_tx_octets" / Int16ul,
    "supported_max_tx_time" / Int16ul,
    "supported_max_rx_octets" / Int16ul,
    "supported_max_rx_time" / Int16ul,
)

ReadInquiryResponseTransmitPowerLevelComplete = Struct(
    "tx_power" / Int8ul,
)

CommandComplete = Struct(
    "ncmd" / Int8ul,
    "opcode" / CommandOpcodeAdapter,
    # TODO: this should be moved to payload, since not all commands require
    # "status" return parameter (e.g. HOLD_MODE)
    "status" / ErrorCodeAdapter,
    "payload" / Switch(
        this.opcode,
        {
            CommandOpcode.DELETE_STORED_LINK_KEY: DeleteStoredLinkKeyComplete,

            CommandOpcode.READ_LOCAL_VERSION_INFORMATION: ReadLocalVersionInformation,
            CommandOpcode.READ_LOCAL_SUPPORTED_COMMANDS: ReadLocalSupportedCommandsComplete,
            CommandOpcode.READ_LOCAL_SUPPORTED_FEATURES: ReadLocalSupportedFeaturesComplete,
            CommandOpcode.READ_LOCAL_EXTENDED_FEATURES: ReadLocalExtendedFeaturesComplete,
            CommandOpcode.READ_BUFFER_SIZE: ReadBufferSizeComplete,
            CommandOpcode.READ_BD_ADDR: ReadBDAddrComplete,
            CommandOpcode.READ_DATA_BLOCK_SIZE: ReadDataBlockSizeComplete,
            CommandOpcode.READ_LOCAL_SUPPORTED_CODECS: ReadLocalSupportedCodecsComplete,

            CommandOpcode.READ_STORED_LINK_KEY: ReadStoredLocalLinkKeyComplete,
            CommandOpcode.READ_LOCAL_NAME: ReadLocalNameComplete,
            CommandOpcode.READ_PAGE_SCAN_ACTIVITY: ReadPageScanActivityComplete,
            CommandOpcode.READ_CLASS_OF_DEVICE: ReadClassOfDeviceComplete,
            CommandOpcode.READ_VOICE_SETTING: ReadVoiceSettingComplete,
            CommandOpcode.READ_NUMBER_OF_SUPPORTED_IAC: ReadNumberOfSupprtedIACComplete,
            CommandOpcode.READ_CURRENT_IAC_LAP: ReadCurrentIACLAPComplete,
            CommandOpcode.READ_PAGE_SCAN_TYPE: ReadPageScanTypeComplete,
            CommandOpcode.READ_INQUIRY_RESPONSE_TRANSMIT_POWER_LEVEL: ReadInquiryResponseTransmitPowerLevelComplete,

            CommandOpcode.LE_READ_BUFFER_SIZE: LEReadBufferSizeComplete,
            CommandOpcode.LE_READ_LOCAL_SUPPORTED_FEATURES: LEReadLocalSupportedFeaturesComplete,
            CommandOpcode.LE_READ_ADVERTISING_CHANNEL_TX_POWER: LEReadAdvertisingChannelTxPowerComplete,
            CommandOpcode.LE_READ_WHITE_LIST_SIZE: LEReadWhiteListSizeComplete,
            CommandOpcode.LE_READ_SUPPORTED_STATES: LEReadSupportedStatesComplete,
            CommandOpcode.LE_READ_SUGGESTED_DEFAULT_DATA_LENGTH: LEReadSuggestedDefaultDataLength,
            CommandOpcode.LE_READ_MAXIMUM_DATA_LENGTH: LEReadMaximumDataLengthComplete,
        },
        default=Bytes(0)
    )
)

CommandStatus = Struct(
    "status" / ErrorCodeAdapter,
    "num_hci_command_packets" / Int8ul,
    "command_opcode" / CommandOpcodeAdapter,
)

LEAdvertisingData = GreedyRange(Struct(
    "length" / Rebuild(Int8ul, len_(this.data) + 1),
    "tag" / Select(LEAdvertisingDataTagAdapter, Int8ul),
    "data" / Bytes(this.length - 1),
))

LEAdvertisingReport = Struct(
    "num_reports" / Rebuild(Int8ul, len_(this.reports)),
    "reports" / Struct(
        "event_type" / Int8ul,
        "address_type" / Int8ul,
        "address" / MacAddress,
        "length_data" / RebuildLength(Int8ul, LEAdvertisingData, this.data),
        "data" / LEAdvertisingData,
        "rssi" / Int8ul,
    )[this.num_reports],
)

LEMetaEvent = Struct(
    "subevent" / LEMetaEventTypeAdapter,
    "payload" / Switch(
        this.subevent,
        {
            LEMetaEventType.LE_ADVERTISING_REPORT: LEAdvertisingReport,
        },
        default=Bytes(this._.length - 1),
    )
)

WriteDefaultLinkPolicySettings = Struct(
    "default_link_policy_settings" / Int16ul,
)

SetEventMask = Struct(
    "event_mask" / BitList(8)
)

ReadStoredLocalLinkKey = Struct(
    "bd_addr" / MacAddress,
    "read_all_flag" / Int8ul,
)

DeleteStoredLinkKey = Struct(
    "bd_addr" / MacAddress,
    "delete_all_flag" / Int8ul,
)

WriteAuthenticationEnable = Struct(
    "authentication_enable" / Int8ul,
)

WriteInquiryMode = Struct(
    "inquiry_mode" / Int8ul,
)

WriteExtendedInquiryResponse = Struct(
    "fec_required" / Int8ul,
    "extended_inquiry_response" / Bytes(240),
)

SetEventMaskPage2 = Struct(
    "event_mask_page_2" / BitList(8),
)

ReadLocalExtendedFeatures = Struct(
    "page_number" / Int8ul,
)

LESetEventMask = Struct(
    "le_event_mask" / BitList(8)
)

LESetRandomAddress = Struct(
    "random_address" / MacAddress,
)

LESetAdvertisingParameters = Struct(
    "advertising_interval_min" / Int16ul,
    "advertising_interval_max" / Int16ul,
    "advertising_type" / EnumAdapter(Int8ul, LEAdvertisingType),
    "own_address_type" / EnumAdapter(Int8ul, LEAddressType),
    "peer_address_type" / EnumAdapter(Int8ul, LEAddressType),
    "peer_address" / MacAddress,
    "advertising_channel_map" / Int8ul,
    "advertising_filter_policy" / Int8ul,
)

LESetAdvertisingData = Struct(
    "advertising_data_length" / RebuildLength(Int8ul, LEAdvertisingData, this.advertising_data),
    "advertising_data" / Padded(31, LEAdvertisingData),
)

LESetScanResponseData = Struct(
    "scan_response_data_length" / Int8ul,
    "scan_response_data" / Padded(31, LEAdvertisingData),
)

LESetAdvertisingEnable = Struct(
    "advertising_enable" / Int8ul,
)

LESetScanParameters = Struct(
    "le_scan_type" / Int8ul,
    "le_scan_interval" / Int16ul,
    "le_scan_window" / Int16ul,
    "own_address_type" / Int8ul,
    "scan_filter_policy" / Int8ul,
)

LESetScanEnable = Struct(
    "le_scan_enable" / Int8ul,
    "filter_duplicates" / Int8ul,
)

LEWriteSuggestedDefaultDataLength = Struct(
    "suggested_max_tx_octets" / Int16ul,
    "suggested_max_tx_time" / Int16ul,
)

CommandMap = {
    CommandOpcode.WRITE_DEFAULT_LINK_POLICY_SETTINGS: WriteDefaultLinkPolicySettings,

    CommandOpcode.SET_EVENT_MASK: SetEventMask,
    CommandOpcode.READ_STORED_LINK_KEY: ReadStoredLocalLinkKey,
    CommandOpcode.DELETE_STORED_LINK_KEY: DeleteStoredLinkKey,
    CommandOpcode.WRITE_AUTHENTICATION_ENABLE: WriteAuthenticationEnable,

    CommandOpcode.WRITE_INQUIRY_MODE: WriteInquiryMode,
    CommandOpcode.WRITE_EXTENDED_INQUIRY_RESPONSE: WriteExtendedInquiryResponse,
    CommandOpcode.SET_EVENT_MASK_PAGE_2: SetEventMaskPage2,

    CommandOpcode.READ_LOCAL_EXTENDED_FEATURES: ReadLocalExtendedFeatures,

    CommandOpcode.LE_SET_EVENT_MASK: LESetEventMask,
    CommandOpcode.LE_SET_RANDOM_ADDRESS: LESetRandomAddress,
    CommandOpcode.LE_SET_ADVERTISING_PARAMETERS: LESetAdvertisingParameters,
    CommandOpcode.LE_SET_ADVERTISING_DATA: LESetAdvertisingData,
    CommandOpcode.LE_SET_SCAN_RESPONSE_DATA: LESetScanResponseData,
    CommandOpcode.LE_SET_ADVERTISING_ENABLE: LESetAdvertisingEnable,
    CommandOpcode.LE_SET_SCAN_PARAMETERS: LESetScanParameters,
    CommandOpcode.LE_SET_SCAN_ENABLE: LESetScanEnable,
    CommandOpcode.LE_WRITE_SUGGESTED_DEFAULT_DATA_LENGTH: LEWriteSuggestedDefaultDataLength,
}

CommandPayload = Switch(
    this.opcode,
    CommandMap,
    default=Bytes(0),
)

Command = Struct(
    "opcode" / CommandOpcodeAdapter,
    "length" / SwitchLength(Int8ul, this.opcode, CommandMap, this.payload),
    "payload" / CommandPayload,
)

AclData = Struct(
    "handle" / Int16ul,
    "data_total_length" / Rebuild(Int8ul, len_(this.data)),
    "data" / Bytes(this.data_total_length)
)

SynchronousData = Struct(
    "handle" / Int16ul,
    "data_total_length" / Rebuild(Int8ul, len_(this.data)),
    "data" / Bytes(this.data_total_length),
)

EventMap = {
    EventType.COMMAND_COMPLETE: CommandComplete,
    EventType.COMMAND_STATUS: CommandStatus,
    EventType.LE_META_EVENT: LEMetaEvent,
}

Event = Struct(
    "event" / EventTypeAdapter,
    "length" / SwitchLength(Int8ul, this.event, EventMap, this.payload),
    "payload" / Switch(
        this.event,
        EventMap
    ),
)

ExtendedCommand = Struct(
    "opcode" / CommandOpcodeAdapter,
    "length" / SwitchLength(Int16ul, this.opcode, CommandMap, this.payload),
    "payload" / CommandPayload,
)

Vendor = Bytes(this._.vendor_length)

Packet = Struct(
    "type" / PacketTypeAdapter,
    "payload" / Switch(
        this.type,
        {
            PacketType.COMMAND: Command,
            PacketType.ACL_DATA: AclData,
            PacketType.SYNCHRONOUS_DATA: SynchronousData,
            PacketType.EVENT: Event,
            PacketType.VENDOR: Vendor,
        },
    )
)
# fmt: on
