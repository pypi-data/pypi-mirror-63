import copy
import functools
import inspect
from typing import Union

from .collections import AttrDict
from .utils import load_dict
from .utils import save_dict

_REGISTRY = {}
_KEY_OF_FUNC_OR_CLS = 'name'


class Config(AttrDict):

    def __call__(self, *args, **kwargs):
        return self.instantiate(*args, **kwargs)

    def save(self, f, **kwargs):
        r"""Save configuration file

        Arguments:
            f (str): the configuration file
        """
        save_dict(self.to_dict(), f, **kwargs)

    def instantiate(self, *args, recursive=False, ignore_args=False, **kwargs):
        r"""Create object (or get function output) from config

        Arguments:
            recursive (bool, optional): create object recursively
            ignore_args (bool, optional): ignore arguments not in argument spec

        Returns an object (or function output)
        """
        kwargs = copy.deepcopy(kwargs)

        for k, v in self.items():
            if k not in kwargs and k != _KEY_OF_FUNC_OR_CLS:
                kwargs[k] = v

        if recursive:
            for k, v in kwargs.items():
                if isinstance(v, self.__class__):
                    kwargs[k] = v.instantiate(recursive=recursive, ignore_args=ignore_args)

        func_or_cls = _REGISTRY[self[_KEY_OF_FUNC_OR_CLS]]

        if ignore_args:
            spec = inspect.signature(func_or_cls)
            kwargs = {k: v for k, v in kwargs.items() if k in spec.parameters}

        return func_or_cls(*args, **kwargs)

    def merge(self, other, allow_new_key=False):
        r"""Merge other config

        Arguments:
            allow_new_key (bool, optional): allow new key to merge
        """
        for key, value in other.items():
            if key not in self.keys() and not allow_new_key:
                raise ValueError('{} not found and new key is not allowed'.format(key))

            if isinstance(value, self.__class__):
                self[key].merge(value, allow_new_key)
            else:
                self[key] = value

    def merge_from_file(self, f: str, allow_new_key=False):
        config = load(f)
        self.merge(config, allow_new_key)


def _flatten(data, prefix=None, sep='.'):
    d = {}

    for key, value in data.items():
        if prefix is not None:
            key = prefix + sep + key

        if isinstance(value, dict):
            d.update(_flatten(value, prefix=key))

        d[key] = value

    return d


def _replace(data, prefix='$'):
    m = _flatten(data)

    def replace(d):
        for key, value in d.items():
            if isinstance(value, str) and value.startswith(prefix):
                d[key] = m[value.lstrip(prefix)]

            if isinstance(value, dict):
                replace(value)

    replace(data)

    return data


def load(f_or_dict: Union[str, dict], replace_values=True):
    r"""Load configuration file

    Arguments:
        f_or_dict (str, dict): the configuration file or dict
        replace_values (bool, optional): replace the values with prefix $
    """
    if isinstance(f_or_dict, str):
        data = load_dict(f_or_dict)
    elif isinstance(f_or_dict, dict):
        data = f_or_dict
    else:
        raise TypeError('f_or_dict should be str or dict')

    if replace_values:
        data = _replace(data)

    config = Config(data)
    return config


def register(func_or_cls=None, name: str = None):
    r"""Register function or class

    Arguments:
        func_or_cls: function or class to be registered
        name (str, optional): name of the func_or_cls in registry
    """
    if isinstance(func_or_cls, str) and name is None:
        func_or_cls, name = None, func_or_cls

    def _register(func_or_cls, name=None):
        if name is None:
            name = func_or_cls.__name__

        if name not in _REGISTRY:
            _REGISTRY[name] = func_or_cls
        else:
            raise ValueError('duplicate name {} found'.format(name))

        return func_or_cls

    if func_or_cls is None:
        return functools.partial(_register, name=name)

    return _register(func_or_cls, name=name)


def set_key_of_func_or_cls(key: str):
    global _KEY_OF_FUNC_OR_CLS
    _KEY_OF_FUNC_OR_CLS = key


def instantiate(config, *args, **kwargs):
    r"""Create object (or get function output) from config

    Arguments:
        config (Config): the config to create object

    Returns an object (or function output)
    """
    kwargs = copy.deepcopy(kwargs)

    for k, v in config.items():
        if k not in kwargs and k != _KEY_OF_FUNC_OR_CLS:
            kwargs[k] = v

    func_or_cls = _REGISTRY[config[_KEY_OF_FUNC_OR_CLS]]

    return func_or_cls(*args, **kwargs)
