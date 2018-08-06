import re

from click import Option, UsageError, Context
from typing import Any, Dict, Optional, TypeVar
from kubernaut.backend import Backend

import json
import random
import pkg_resources
import string


T = TypeVar('T')


def get_current_backend(ctx: Context, fail_if_not_found: bool = True) -> Optional[Backend]:
    config = ctx.obj

    from pprint import pprint
    pprint(config)

    if config.current_backend is not None:
        return config.current_backend
    else:
        if fail_if_not_found:
            ctx.fail("No activated backend was found. Please activate a backend")
        else:
            return None


def require(value: T) -> T:
    if value is None:
        return None
    else:
        return value


def load_resource(name) -> str:
    res = pkg_resources.resource_string(__name__, "/".join(("resources", name)))
    return res.decode("utf-8")


def random_alphanum(length: int) -> str:
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def random_name(suffix_len: int = 8) -> str:
    data = json.loads(load_resource("names.json"))
    part1 = random.choice(data["adjectives"])
    part2 = random.choice(data["fruits"])

    if suffix_len > 0:
        return "{}-{}-{}".format(part1, part2, random_alphanum(suffix_len))
    else:
        return "{}-{}"


def strip_margin(text: str) -> str:
    return re.sub('\n[ \t]*\|', '\n', text)


class MutexOption(Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        kwargs['help'] = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = kwargs['help'] + (
                    ' NOTE: This argument is mutually exclusive with '
                    ' arguments: [' + ex_str + '].'
            )
        super(MutexOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(
                    self.name,
                    ', '.join(self.mutually_exclusive)
                )
            )

        return super(MutexOption, self).handle_parse_result(ctx, opts, args)
