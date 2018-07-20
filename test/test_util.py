from kubernaut.util import require

import pytest


def test_require_raise_if_none():
    with pytest.raises(ValueError) as e:
        require(None)


def test_require_returns_value_if_not_none():
    assert "IAmTheWalrus" == require("IAmTheWalrus")
