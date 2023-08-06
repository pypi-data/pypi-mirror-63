#**
# * Copyright (c) 2020 Weitian Leung
# *
# * This file is part of pywpsrpc.
# *
# * This file is distributed under the MIT License.
# * See the LICENSE file for details.
# *
#*


from .common import (S_OK, IUnknown)
from types import BuiltinFunctionType


class RpcException(Exception):

    def __init__(self, text, hr=None):
        self._text = text
        self._hr = hr

    def __str__(self):
        text = "RpcException: {}".format(self._text)
        if not self._hr is None:
            text += " ({})".format(hex(self._hr & 0xffffffff))

        return text


class RpcMethod(object):
    __slots__ = ["_method", "_proxy"]

    def __init__(self, method, proxy):
        self._proxy = None
        if not isinstance(method, BuiltinFunctionType):
            raise RpcException("RpcMethod required builtin function or method")

        self._method = method
        self._proxy = proxy

        # AddRef to avoid Releasing before the method be called
        # such as app.Documents.Add()
        self._proxy.rpc_object.AddRef()

    def __del__(self):
        if self._proxy:
            self._proxy.rpc_object.Release()

    def __call__(self, *args, **kwargs):
        ret = self._method(*args, **kwargs)
        if isinstance(ret, tuple):
            self._proxy.last_error = ret[0]
            if ret[0] != S_OK:
                if self._proxy.use_exception:
                    raise RpcException("Call '{}' failed.".format(
                        self._method), ret[0])
                return None

            if len(ret) == 2:
                if isinstance(ret[1], IUnknown):
                    return RpcProxy(ret[1], self._proxy.use_exception)
                else:
                    return ret[1]

            result = ()
            for i in range(1, len(ret)):
                if isinstance(ret[i], IUnknown):
                    result += (RpcProxy(ret[i], self._proxy.use_exception), )
                else:
                    result += (ret[i], )
            return result

        self._proxy.last_error = ret
        return ret == S_OK

    @property
    def __doc__(self):
        return self._method.__doc__


class RpcProxy(object):
    __slots__ = ["_object", "_use_exception", "_last_hr"]

    def __init__(self, obj, use_exception=False):
        """ The obj can be (hr, IUnknown) or IUnknown.
        If use_exception set to True then any call failed will raise an exception.
        """

        def _check_iunknown(obj):
            if not isinstance(obj, IUnknown):
                raise RpcException("RpcProxy required an IUnknown instance")

        self._object = None
        self._last_hr = S_OK
        if isinstance(obj, tuple):
            self._last_hr = obj[0]
            if obj[0] == S_OK:
                _check_iunknown(obj[1])
                self._object = obj[1]
            elif use_exception:
                raise RpcException("Can't create proxy due to the previous call failed.", obj[0])
        else:
            _check_iunknown(obj)
            self._object = obj

        self._use_exception = use_exception

    def __del__(self):
        if self._object:
            self._object.Release()

    def __getattr__(self, name):
        if name.startswith("_"):
            return getattr(self._object, name)

        if hasattr(self._object, name):
            return RpcMethod(getattr(self._object, name), self)

        hr, value = getattr(self._object, "get_" + name)()
        if hr != S_OK:
            if self._use_exception:
                raise RpcException("Call '{}.get_{}()' failed.".format(
                    self._object.__class__.__name__, name), hr)
            value = None
        elif isinstance(value, IUnknown):
            value = RpcProxy(value, self._use_exception)

        self._last_hr = hr

        return value

    def __setattr__(self, name, value):
        if name in self.__slots__ or name in ("use_exception", "last_error", "rpc_object"):
            super().__setattr__(name, value)
        else:
            hr = getattr(self._object, "put_" + name)(value)
            if hr != S_OK and self._use_exception:
                raise RpcException("Call '{}.put_{}({})' failed.".format(
                    self._object.__class__.__name__, name, value), hr)
            self._last_hr = hr

    def __bool__(self):
        return not self._object is None

    @property
    def rpc_object(self):
        return self._object

    @property
    def use_exception(self):
        return self._use_exception

    @use_exception.setter
    def use_exception(self, value):
        self._use_exception = value

    @property
    def last_error(self):
        return self._last_hr

    @last_error.setter
    def last_error(self, hr):
        self._last_hr = hr
