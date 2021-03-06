# generated by 'xml2py'
# flags '-c -d -k defst -l blackbox.dll -o blackbox.py -m ctypes.wintypes BlackBox.xml'
from ctypes import *

from ctypes.wintypes import DWORD
from ctypes.wintypes import BOOL
from ctypes.wintypes import BYTE
from ctypes.wintypes import WORD
_libraries = {}
_libraries['blackbox.dll'] = CDLL('blackbox.dll')
STRING = c_char_p


GPIO_PUSH_PULL = 2
GPIO_OPEN_DRAIN = 3
GPIO_INPUT = 1
GPIO_BIDI = 0
BB_HANDLE = c_ushort
# C:\Python27\BlackBox.h 39
class I2C_OPTIONS(Structure):
    pass
I2C_OPTIONS._fields_ = [
    # C:\Python27\BlackBox.h 39
    ('readTimeout', DWORD),
    ('writeTimeout', DWORD),
    ('repeatedStart', BOOL),
    ('isBigEndian', BOOL),
    ('regAddr16', BOOL),
    ('noIncAddr', BOOL),
    ('i2cBusMode', c_int),
    ('i2cTimeout', c_int),
    ('busGrantEnabled', BOOL),
]

# values for unnamed enumeration
# C:\Python27\BlackBox.h 66
class GPIO_OPTIONS(Structure):
    pass
GPIO_OPTIONS._fields_ = [
    # C:\Python27\BlackBox.h 66
    ('readTimeout', DWORD),
    ('writeTimeout', DWORD),
    ('gpioCfg0', BYTE),
    ('gpioCfg1', BYTE),
    ('gpioCfg2', BYTE),
    ('gpioCfg3', BYTE),
    ('gpioCfg4', BYTE),
    ('gpioCfg5', BYTE),
    ('gpioCfg6', BYTE),
    ('gpioCfg7', BYTE),
    ('gpioRequest', BYTE),
    ('gpioGrant', BYTE),
    ('gpioRequestActiveLow', BOOL),
    ('gpioGrantActiveLow', BOOL),
]
# C:\Python27\BlackBox.h 68
BlackBox_GetVersion = _libraries['blackbox.dll'].BlackBox_GetVersion
BlackBox_GetVersion.restype = BYTE
# BlackBox_GetVersion(pVersion)
BlackBox_GetVersion.argtypes = [POINTER(DWORD)]
BlackBox_GetVersion.__doc__ = \
"""BYTE BlackBox_GetVersion(DWORD * pVersion)
C:\Python27\BlackBox.h:68"""
# C:\Python27\BlackBox.h 69
BlackBox_Number = _libraries['blackbox.dll'].BlackBox_Number
BlackBox_Number.restype = BYTE
# BlackBox_Number(number)
BlackBox_Number.argtypes = [POINTER(BYTE)]
BlackBox_Number.__doc__ = \
"""BYTE BlackBox_Number(BYTE * number)
C:\Python27\BlackBox.h:69"""
# C:\Python27\BlackBox.h 70
BlackBox_Open = _libraries['blackbox.dll'].BlackBox_Open
BlackBox_Open.restype = BYTE
# BlackBox_Open(number, bbHandle)
BlackBox_Open.argtypes = [BYTE, POINTER(BB_HANDLE)]
BlackBox_Open.__doc__ = \
"""BYTE BlackBox_Open(BYTE number, BYTE * bbHandle)
C:\Python27\BlackBox.h:70"""
# C:\Python27\BlackBox.h 71
BlackBox_Close = _libraries['blackbox.dll'].BlackBox_Close
BlackBox_Close.restype = BYTE
# BlackBox_Close(bbHandle)
BlackBox_Close.argtypes = [BB_HANDLE]
BlackBox_Close.__doc__ = \
"""BYTE BlackBox_Close(BB_HANDLE bbHandle)
C:\Python27\BlackBox.h:71"""
# C:\Python27\BlackBox.h 72
BlackBox_Serial = _libraries['blackbox.dll'].BlackBox_Serial
BlackBox_Serial.restype = BYTE
# BlackBox_Serial(bbHandle, serial)
BlackBox_Serial.argtypes = [BB_HANDLE, POINTER(STRING)]
BlackBox_Serial.__doc__ = \
"""BYTE BlackBox_Serial(BB_HANDLE bbHandle, char * * serial)
C:\Python27\BlackBox.h:72"""
# C:\Python27\BlackBox.h 73
BlackBox_Description = _libraries['blackbox.dll'].BlackBox_Description
BlackBox_Description.restype = BYTE
# BlackBox_Description(bbHandle, description)
BlackBox_Description.argtypes = [BB_HANDLE, POINTER(STRING)]
BlackBox_Description.__doc__ = \
"""BYTE BlackBox_Description(BB_HANDLE bbHandle, char * * description)
C:\Python27\BlackBox.h:73"""
# C:\Python27\BlackBox.h 74
BlackBox_GetLastStatus = _libraries['blackbox.dll'].BlackBox_GetLastStatus
BlackBox_GetLastStatus.restype = BYTE
# BlackBox_GetLastStatus(bbHandle, pStatus)
BlackBox_GetLastStatus.argtypes = [BYTE, POINTER(STRING)]
BlackBox_GetLastStatus.__doc__ = \
"""BYTE BlackBox_GetLastStatus(BYTE bbHandle, char * * pStatus)
C:\Python27\BlackBox.h:74"""
# C:\Python27\BlackBox.h 76
I2C_ReadByte = _libraries['blackbox.dll'].I2C_ReadByte
I2C_ReadByte.restype = BYTE
# I2C_ReadByte(bbHandle, deviceID, regAddr)
I2C_ReadByte.argtypes = [BB_HANDLE, BYTE, WORD]
I2C_ReadByte.__doc__ = \
"""BYTE I2C_ReadByte(BB_HANDLE bbHandle, BYTE deviceID, WORD regAddr)
C:\Python27\BlackBox.h:76"""
# C:\Python27\BlackBox.h 77
I2C_ReadWord = _libraries['blackbox.dll'].I2C_ReadWord
I2C_ReadWord.restype = WORD
# I2C_ReadWord(bbHandle, deviceID, regAddr)
I2C_ReadWord.argtypes = [BB_HANDLE, BYTE, WORD]
I2C_ReadWord.__doc__ = \
"""WORD I2C_ReadWord(BB_HANDLE bbHandle, BYTE deviceID, WORD regAddr)
C:\Python27\BlackBox.h:77"""
# C:\Python27\BlackBox.h 78
I2C_ReadBlock = _libraries['blackbox.dll'].I2C_ReadBlock
I2C_ReadBlock.restype = BYTE
# I2C_ReadBlock(bbHandle, deviceID, regAddr, pData, length)
I2C_ReadBlock.argtypes = [BB_HANDLE, BYTE, WORD, POINTER(BYTE), WORD]
I2C_ReadBlock.__doc__ = \
"""BYTE I2C_ReadBlock(BB_HANDLE bbHandle, BYTE deviceID, WORD regAddr, BYTE * pData, WORD length)
C:\Python27\BlackBox.h:78"""
# C:\Python27\BlackBox.h 81
I2C_WriteByte = _libraries['blackbox.dll'].I2C_WriteByte
I2C_WriteByte.restype = None
# I2C_WriteByte(bbHandle, deviceID, regAddr, value)
I2C_WriteByte.argtypes = [BB_HANDLE, BYTE, WORD, BYTE]
I2C_WriteByte.__doc__ = \
"""void I2C_WriteByte(BB_HANDLE bbHandle, BYTE deviceID, WORD regAddr, BYTE value)
C:\Python27\BlackBox.h:81"""
# C:\Python27\BlackBox.h 82
I2C_WriteWord = _libraries['blackbox.dll'].I2C_WriteWord
I2C_WriteWord.restype = None
# I2C_WriteWord(bbHandle, deviceID, regAddr, value)
I2C_WriteWord.argtypes = [BB_HANDLE, BYTE, WORD, WORD]
I2C_WriteWord.__doc__ = \
"""void I2C_WriteWord(BB_HANDLE bbHandle, BYTE deviceID, WORD regAddr, WORD value)
C:\Python27\BlackBox.h:82"""
# C:\Python27\BlackBox.h 83
I2C_WriteBlock = _libraries['blackbox.dll'].I2C_WriteBlock
I2C_WriteBlock.restype = BYTE
# I2C_WriteBlock(bbHandle, deviceID, regAddr, Data, length)
I2C_WriteBlock.argtypes = [BB_HANDLE, BYTE, WORD, POINTER(BYTE), WORD]
I2C_WriteBlock.__doc__ = \
"""BYTE I2C_WriteBlock(BB_HANDLE bbHandle, BYTE deviceID, WORD regAddr, unknown * Data, WORD length)
C:\Python27\BlackBox.h:83"""
# C:\Python27\BlackBox.h 85
GetI2CRepeatedStartMode = _libraries['blackbox.dll'].GetI2CRepeatedStartMode
GetI2CRepeatedStartMode.restype = BYTE
# GetI2CRepeatedStartMode(bbHandle, startMode)
GetI2CRepeatedStartMode.argtypes = [BB_HANDLE, POINTER(BYTE)]
GetI2CRepeatedStartMode.__doc__ = \
"""BYTE GetI2CRepeatedStartMode(BB_HANDLE bbHandle, BYTE * startMode)
C:\Python27\BlackBox.h:85"""
# C:\Python27\BlackBox.h 86
SetI2CRepeatedStartMode = _libraries['blackbox.dll'].SetI2CRepeatedStartMode
SetI2CRepeatedStartMode.restype = BYTE
# SetI2CRepeatedStartMode(bbHandle, startMode)
SetI2CRepeatedStartMode.argtypes = [BB_HANDLE, BYTE]
SetI2CRepeatedStartMode.__doc__ = \
"""BYTE SetI2CRepeatedStartMode(BB_HANDLE bbHandle, BYTE startMode)
C:\Python27\BlackBox.h:86"""
# C:\Python27\BlackBox.h 87
GetI2CBigEndianMode = _libraries['blackbox.dll'].GetI2CBigEndianMode
GetI2CBigEndianMode.restype = BYTE
# GetI2CBigEndianMode(bbHandle, endianMode)
GetI2CBigEndianMode.argtypes = [BB_HANDLE, POINTER(BYTE)]
GetI2CBigEndianMode.__doc__ = \
"""BYTE GetI2CBigEndianMode(BB_HANDLE bbHandle, BYTE * endianMode)
C:\Python27\BlackBox.h:87"""
# C:\Python27\BlackBox.h 88
SetI2CBigEndianMode = _libraries['blackbox.dll'].SetI2CBigEndianMode
SetI2CBigEndianMode.restype = BYTE
# SetI2CBigEndianMode(bbHandle, endianMode)
SetI2CBigEndianMode.argtypes = [BB_HANDLE, BYTE]
SetI2CBigEndianMode.__doc__ = \
"""BYTE SetI2CBigEndianMode(BB_HANDLE bbHandle, BYTE endianMode)
C:\Python27\BlackBox.h:88"""
# C:\Python27\BlackBox.h 89
GetI2C16bitAddress = _libraries['blackbox.dll'].GetI2C16bitAddress
GetI2C16bitAddress.restype = BYTE
# GetI2C16bitAddress(bbHandle, is16bitMode)
GetI2C16bitAddress.argtypes = [BB_HANDLE, POINTER(BYTE)]
GetI2C16bitAddress.__doc__ = \
"""BYTE GetI2C16bitAddress(BB_HANDLE bbHandle, BYTE * is16bitMode)
C:\Python27\BlackBox.h:89"""
# C:\Python27\BlackBox.h 90
SetI2C16bitAddress = _libraries['blackbox.dll'].SetI2C16bitAddress
SetI2C16bitAddress.restype = BYTE
# SetI2C16bitAddress(bbHandle, is16bitMode)
SetI2C16bitAddress.argtypes = [BB_HANDLE, BYTE]
SetI2C16bitAddress.__doc__ = \
"""BYTE SetI2C16bitAddress(BB_HANDLE bbHandle, BYTE is16bitMode)
C:\Python27\BlackBox.h:90"""
# C:\Python27\BlackBox.h 91
GetI2CIncAddress = _libraries['blackbox.dll'].GetI2CIncAddress
GetI2CIncAddress.restype = BYTE
# GetI2CIncAddress(bbHandle, incAddrMode)
GetI2CIncAddress.argtypes = [BB_HANDLE, POINTER(BYTE)]
GetI2CIncAddress.__doc__ = \
"""BYTE GetI2CIncAddress(BB_HANDLE bbHandle, BYTE * incAddrMode)
C:\Python27\BlackBox.h:91"""
# C:\Python27\BlackBox.h 92
SetI2CIncAddress = _libraries['blackbox.dll'].SetI2CIncAddress
SetI2CIncAddress.restype = BYTE
# SetI2CIncAddress(bbHandle, incAddrMode)
SetI2CIncAddress.argtypes = [BB_HANDLE, BYTE]
SetI2CIncAddress.__doc__ = \
"""BYTE SetI2CIncAddress(BB_HANDLE bbHandle, BYTE incAddrMode)
C:\Python27\BlackBox.h:92"""
# C:\Python27\BlackBox.h 93
GetI2CBusGrantMode = _libraries['blackbox.dll'].GetI2CBusGrantMode
GetI2CBusGrantMode.restype = BYTE
# GetI2CBusGrantMode(bbHandle, busGrant)
GetI2CBusGrantMode.argtypes = [BB_HANDLE, POINTER(BOOL)]
GetI2CBusGrantMode.__doc__ = \
"""BYTE GetI2CBusGrantMode(BB_HANDLE bbHandle, BOOL * busGrant)
C:\Python27\BlackBox.h:93"""
# C:\Python27\BlackBox.h 94
SetI2CBusGrantMode = _libraries['blackbox.dll'].SetI2CBusGrantMode
SetI2CBusGrantMode.restype = BYTE
# SetI2CBusGrantMode(bbHandle, busGrant)
SetI2CBusGrantMode.argtypes = [BB_HANDLE, BOOL]
SetI2CBusGrantMode.__doc__ = \
"""BYTE SetI2CBusGrantMode(BB_HANDLE bbHandle, BOOL busGrant)
C:\Python27\BlackBox.h:94"""
# C:\Python27\BlackBox.h 96
I2C_GetOptions = _libraries['blackbox.dll'].I2C_GetOptions
I2C_GetOptions.restype = BYTE
# I2C_GetOptions(bbHandle, pOptions)
I2C_GetOptions.argtypes = [BB_HANDLE, POINTER(I2C_OPTIONS)]
I2C_GetOptions.__doc__ = \
"""BYTE I2C_GetOptions(BB_HANDLE bbHandle, I2C_OPTIONS * pOptions)
C:\Python27\BlackBox.h:96"""
# C:\Python27\BlackBox.h 97
I2C_SetOptions = _libraries['blackbox.dll'].I2C_SetOptions
I2C_SetOptions.restype = BYTE
# I2C_SetOptions(bbHandle, pOptions)
I2C_SetOptions.argtypes = [BB_HANDLE, I2C_OPTIONS]
I2C_SetOptions.__doc__ = \
"""BYTE I2C_SetOptions(BB_HANDLE bbHandle, I2C_OPTIONS pOptions)
C:\Python27\BlackBox.h:97"""
# C:\Python27\BlackBox.h 99
GPIO_GetPins = _libraries['blackbox.dll'].GPIO_GetPins
GPIO_GetPins.restype = BYTE
# GPIO_GetPins(bbHandle, pinMask)
GPIO_GetPins.argtypes = [BB_HANDLE, BYTE]
GPIO_GetPins.__doc__ = \
"""BYTE GPIO_GetPins(BB_HANDLE bbHandle, BYTE pinMask)
C:\Python27\BlackBox.h:99"""
# C:\Python27\BlackBox.h 100
GPIO_SetPins = _libraries['blackbox.dll'].GPIO_SetPins
GPIO_SetPins.restype = BYTE
# GPIO_SetPins(bbHandle, pinMask)
GPIO_SetPins.argtypes = [BB_HANDLE, GPIO_OPTIONS]
GPIO_SetPins.__doc__ = \
"""BYTE GPIO_SetPins(BB_HANDLE bbHandle, BYTE pinMask)
C:\Python27\BlackBox.h:100"""
# C:\Python27\BlackBox.h 101
GPIO_ClearPins = _libraries['blackbox.dll'].GPIO_ClearPins
GPIO_ClearPins.restype = BYTE
# GPIO_ClearPins(bbHandle, pinMask)
GPIO_ClearPins.argtypes = [BB_HANDLE, BYTE]
GPIO_ClearPins.__doc__ = \
"""BYTE GPIO_ClearPins(BB_HANDLE bbHandle, BYTE pinMask)
C:\Python27\BlackBox.h:101"""
# C:\Python27\BlackBox.h 102
GPIO_ModifyPins = _libraries['blackbox.dll'].GPIO_ModifyPins
GPIO_ModifyPins.restype = BYTE
# GPIO_ModifyPins(bbHandle, PinMask, PinState)
GPIO_ModifyPins.argtypes = [BB_HANDLE, BYTE, BYTE]
GPIO_ModifyPins.__doc__ = \
"""BYTE GPIO_ModifyPins(BB_HANDLE bbHandle, BYTE PinMask, BYTE PinState)
C:\Python27\BlackBox.h:102"""
# C:\Python27\BlackBox.h 104
GetGPIOBusRequestPin = _libraries['blackbox.dll'].GetGPIOBusRequestPin
GetGPIOBusRequestPin.restype = BYTE
# GetGPIOBusRequestPin(bbHandle, requestPin)
GetGPIOBusRequestPin.argtypes = [BB_HANDLE, POINTER(BYTE)]
GetGPIOBusRequestPin.__doc__ = \
"""BYTE GetGPIOBusRequestPin(BB_HANDLE bbHandle, BYTE * requestPin)
C:\Python27\BlackBox.h:104"""
# C:\Python27\BlackBox.h 105
SetGPIOBusRequestPin = _libraries['blackbox.dll'].SetGPIOBusRequestPin
SetGPIOBusRequestPin.restype = BYTE
# SetGPIOBusRequestPin(bbHandle, requestPin)
SetGPIOBusRequestPin.argtypes = [BB_HANDLE, BYTE]
SetGPIOBusRequestPin.__doc__ = \
"""BYTE SetGPIOBusRequestPin(BB_HANDLE bbHandle, BYTE requestPin)
C:\Python27\BlackBox.h:105"""
# C:\Python27\BlackBox.h 106
GetGPIOBusGrantPin = _libraries['blackbox.dll'].GetGPIOBusGrantPin
GetGPIOBusGrantPin.restype = BYTE
# GetGPIOBusGrantPin(bbHandle, grantPin)
GetGPIOBusGrantPin.argtypes = [BB_HANDLE, POINTER(BYTE)]
GetGPIOBusGrantPin.__doc__ = \
"""BYTE GetGPIOBusGrantPin(BB_HANDLE bbHandle, BYTE * grantPin)
C:\Python27\BlackBox.h:106"""
# C:\Python27\BlackBox.h 107
SetGPIOBusGrantPin = _libraries['blackbox.dll'].SetGPIOBusGrantPin
SetGPIOBusGrantPin.restype = BYTE
# SetGPIOBusGrantPin(bbHandle, grantPin)
SetGPIOBusGrantPin.argtypes = [BB_HANDLE, BYTE]
SetGPIOBusGrantPin.__doc__ = \
"""BYTE SetGPIOBusGrantPin(BB_HANDLE bbHandle, BYTE grantPin)
C:\Python27\BlackBox.h:107"""
# C:\Python27\BlackBox.h 108
GetGPIOBusRequestActiveLow = _libraries['blackbox.dll'].GetGPIOBusRequestActiveLow
GetGPIOBusRequestActiveLow.restype = BYTE
# GetGPIOBusRequestActiveLow(bbHandle, busRequestLow)
GetGPIOBusRequestActiveLow.argtypes = [BB_HANDLE, POINTER(BOOL)]
GetGPIOBusRequestActiveLow.__doc__ = \
"""BYTE GetGPIOBusRequestActiveLow(BB_HANDLE bbHandle, BOOL * busRequestLow)
C:\Python27\BlackBox.h:108"""
# C:\Python27\BlackBox.h 109
SetGPIOBusRequestActiveLow = _libraries['blackbox.dll'].SetGPIOBusRequestActiveLow
SetGPIOBusRequestActiveLow.restype = BYTE
# SetGPIOBusRequestActiveLow(bbHandle, busRequestLow)
SetGPIOBusRequestActiveLow.argtypes = [BB_HANDLE, BOOL]
SetGPIOBusRequestActiveLow.__doc__ = \
"""BYTE SetGPIOBusRequestActiveLow(BB_HANDLE bbHandle, BOOL busRequestLow)
C:\Python27\BlackBox.h:109"""
# C:\Python27\BlackBox.h 110
GetGPIOBusGrantActiveLow = _libraries['blackbox.dll'].GetGPIOBusGrantActiveLow
GetGPIOBusGrantActiveLow.restype = BYTE
# GetGPIOBusGrantActiveLow(bbHandle, busGrantLow)
GetGPIOBusGrantActiveLow.argtypes = [BB_HANDLE, POINTER(BOOL)]
GetGPIOBusGrantActiveLow.__doc__ = \
"""BYTE GetGPIOBusGrantActiveLow(BB_HANDLE bbHandle, BOOL * busGrantLow)
C:\Python27\BlackBox.h:110"""
# C:\Python27\BlackBox.h 111
SetGPIOBusGrantActiveLow = _libraries['blackbox.dll'].SetGPIOBusGrantActiveLow
SetGPIOBusGrantActiveLow.restype = BYTE
# SetGPIOBusGrantActiveLow(bbHandle, busGrantLow)
SetGPIOBusGrantActiveLow.argtypes = [BB_HANDLE, BOOL]
SetGPIOBusGrantActiveLow.__doc__ = \
"""BYTE SetGPIOBusGrantActiveLow(BB_HANDLE bbHandle, BOOL busGrantLow)
C:\Python27\BlackBox.h:111"""
# C:\Python27\BlackBox.h 113
GPIO_GetOptions = _libraries['blackbox.dll'].GPIO_GetOptions
GPIO_GetOptions.restype = BYTE
# GPIO_GetOptions(bbHandle, pOptions)
GPIO_GetOptions.argtypes = [BB_HANDLE, POINTER(GPIO_OPTIONS)]
GPIO_GetOptions.__doc__ = \
"""BYTE GPIO_GetOptions(BB_HANDLE bbHandle, GPIO_OPTIONS * pOptions)
C:\Python27\BlackBox.h:113"""
# C:\Python27\BlackBox.h 114
GPIO_SetOptions = _libraries['blackbox.dll'].GPIO_SetOptions
GPIO_SetOptions.restype = BYTE
# GPIO_SetOptions(bbHandle, pOptions)
GPIO_SetOptions.argtypes = [BB_HANDLE, GPIO_OPTIONS]
GPIO_SetOptions.__doc__ = \
"""BYTE GPIO_SetOptions(BB_HANDLE bbHandle, GPIO_OPTIONS pOptions)
C:\Python27\BlackBox.h:114"""
I2C_ADDRMODE_16 = 1 # Variable c_int '1'
I2C_TIMEOUT_MIN = 1 # Variable c_int '1'
I2C_ADDRMODE_8 = 0 # Variable c_int '0'
I2C_MODE_FAST = 0 # Variable c_int '0'
SUCCESS = 0 # Variable c_int '0'
I2C_MODE_SLOW = 2 # Variable c_int '2'
I2C_TIMEOUT_MAX = 127 # Variable c_int '127'
I2C_MODE_STD = 1 # Variable c_int '1'
FAILURE = 1 # Variable c_int '1'
I2C_TIMEOUT_DISABLE = 0 # Variable c_int '0'
__all__ = ['I2C_WriteWord', 'SetGPIOBusGrantActiveLow',
           'GetGPIOBusGrantPin', 'BlackBox_Number',
           'BlackBox_GetVersion', 'GPIO_SetOptions', 'BlackBox_Open',
           'SetI2CIncAddress', 'SetGPIOBusRequestPin',
           'GetI2CBusGrantMode', 'SetI2CBusGrantMode', 'I2C_MODE_STD',
           'GPIO_PUSH_PULL', 'GPIO_ModifyPins', 'GPIO_OPEN_DRAIN',
           'SUCCESS', 'I2C_MODE_FAST', 'GPIO_GetOptions',
           'I2C_MODE_SLOW', 'SetI2C16bitAddress',
           'GetGPIOBusRequestPin', 'SetGPIOBusGrantPin',
           'BlackBox_GetLastStatus', 'I2C_TIMEOUT_DISABLE',
           'GPIO_BIDI', 'I2C_ReadBlock', 'GPIO_GetPins', 'FAILURE',
           'GetI2C16bitAddress', 'BlackBox_Description',
           'GetGPIOBusRequestActiveLow', 'SetI2CRepeatedStartMode',
           'I2C_WriteBlock', 'GetI2CRepeatedStartMode',
           'I2C_ADDRMODE_16', 'I2C_SetOptions', 'BB_HANDLE',
           'BlackBox_Serial', 'GPIO_ClearPins', 'I2C_OPTIONS',
           'GetI2CBigEndianMode', 'I2C_WriteByte', 'I2C_TIMEOUT_MIN',
           'GetGPIOBusGrantActiveLow', 'I2C_ADDRMODE_8',
           'I2C_ReadByte', 'I2C_TIMEOUT_MAX',
           'SetGPIOBusRequestActiveLow', 'I2C_GetOptions',
           'GetI2CIncAddress', 'SetI2CBigEndianMode', 'GPIO_INPUT',
           'GPIO_SetPins', 'I2C_ReadWord', 'BlackBox_Close',
           'GPIO_OPTIONS']
