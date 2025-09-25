from __future__ import annotations

import contextlib
from functools import wraps
from typing import Any, Dict, Iterable, Sequence


class ParametrizedTestCase:
    pass


def _parse_names(names: str) -> Sequence[str]:
    return [n.strip() for n in names.split(",") if n.strip()]


def _to_kwargs(names: Sequence[str], row: Any) -> Dict[str, Any]:
    if isinstance(row, dict):
        return row
    if not isinstance(row, (list, tuple)):
        row = (row,)
    return dict(zip(names, row, strict=False))


def parametrize(names: str, rows: Iterable[Any]):
    name_list = _parse_names(names)

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for row in rows:
                call_kwargs = _to_kwargs(name_list, row)
                subtest = getattr(self, "subTest", None)
                cm = (
                    subtest(**call_kwargs)
                    if subtest
                    else contextlib.nullcontext()
                )
                with cm:
                    func(self, **call_kwargs)

        return wrapper

    return decorator
