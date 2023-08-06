""" this module interops with the c dll"""
from ctypes import (c_char_p, c_int, c_longlong, c_void_p, cdll, Structure, POINTER,
                    c_bool, CFUNCTYPE)
from typing import NewType
from enum import Enum
import platform
import os
import sys

FREECB = CFUNCTYPE(None, c_void_p)


class SdConfig(Structure):  # pylint: disable=too-few-public-methods
    """ service discovery configuration class """
    _fields_ = [
        ("endpoints", c_char_p),
        ("etcd_prefix", c_char_p),
        ("server_type_filters", c_char_p),
        ("heartbeat_ttl_sec", c_int),
        ("log_heartbeat", c_int),
        ("log_server_sync", c_int),
        ("log_server_details", c_int),
        ("sync_servers_interval_sec", c_int),
        ("max_number_of_retries", c_int)]


class NatsConfig(Structure):  # pylint: disable=too-few-public-methods
    """ nats configuration class """
    _fields_ = [
        ("endpoint", c_char_p),
        ("connection_timeout_ms", c_longlong),
        ("request_timeout_ms", c_int),
        ("max_reconnection_attempts", c_int),
        ("max_pending_msgs", c_int)]


class Server(Structure):  # pylint: disable=too-few-public-methods
    """ server class """
    _fields_ = [
        ("id", c_char_p),
        ("type", c_char_p),
        ("metadata", c_char_p),
        ("hostname", c_char_p),
        ("frontend", c_int)]


class PitayaError(Structure):  # pylint: disable=too-few-public-methods
    """ pitaya error class """
    _fields_ = [
        ("code", c_char_p),
        ("msg", c_char_p)]


class MemoryBuffer(Structure):  # pylint: disable=too-few-public-methods
    """ memory buffer class, this is used to send pointer to data to and from c """
    _fields_ = [
        ("data", c_void_p),
        ("size", c_int)]


class RPCReq(Structure):  # pylint: disable=too-few-public-methods
    """ rpc req class used in sendrpc and rpc cbs """
    _fields_ = [
        ("buffer", POINTER(MemoryBuffer)),
        ("tag", c_void_p)]


RPCCB = CFUNCTYPE(c_void_p, POINTER(RPCReq))

LevelType = NewType('Level', int)
class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    CRITICAL = 4

class Native(object):
    __instance = None

    class __impl:
        def __init__(self):
            lib_dir = os.environ.get('PITAYA_LIB_DIR')
            if lib_dir == None:
                system = platform.system()

                if system == "Linux":
                    lib_dir = "libpitaya_cpp.so"
                elif system == "Darwin":
                    lib_dir = "libpitaya_cpp.dylib"
                elif system == "Windows":
                    lib_dir = "libpitaya_cpp.dll"

                print (
                    "PITAYA_LIB_DIR env var not set, defaulting lib to %s, make sure it's in the current dir" % lib_dir)

            """ Implementation of the singleton interface """

            self.LIB = cdll.LoadLibrary(lib_dir)

            self.LIB.tfg_pitc_InitializeWithNats.restype = c_bool
            self.LIB.tfg_pitc_InitializeWithNats.argtypes = [POINTER(NatsConfig), POINTER(SdConfig), POINTER(Server),
                                                    c_int, c_char_p]

            self.LIB.tfg_pitc_GetServerById.restype = c_bool
            self.LIB.tfg_pitc_GetServerById.argtypes = [
                c_char_p, POINTER(Server)]

            self.LIB.tfg_pitc_FreeServer.argtypes = [POINTER(Server)]

            self.LIB.tfg_pitc_Terminate.restype = None

            self.LIB.tfg_pitc_FreeMemoryBuffer.argtypes = [
                POINTER(MemoryBuffer)]

            self.LIB.tfg_pitc_FreePitayaError.argtypes = [POINTER(PitayaError)]

            self.LIB.tfg_pitc_RPC.restype = c_bool
            self.LIB.tfg_pitc_RPC.argtypes = [c_char_p, c_char_p, c_void_p, c_int,
                                              POINTER(POINTER(MemoryBuffer)), POINTER(PitayaError)]

            self.LIB.tfg_pitc_FreeMem.argtypes = [c_void_p]

            self.LIB.tfg_pitc_AllocMem.restype = c_void_p
            self.LIB.tfg_pitc_AllocMem.argtypes = [c_int]

            self.LIB.tfg_pitc_WaitForRpc.restype = POINTER(RPCReq)

            self.LIB.tfg_pitc_FinishRpcCall.argtypes = [c_void_p,POINTER(RPCReq)]

    def __init__(self):
        if Native.__instance is None:
            Native.__instance = Native.__impl()
        self.__dict__['_Native__instance'] = Native.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
