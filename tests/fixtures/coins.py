import pytest
from brownie import ETH_ADDRESS
from brownie_tokens import ERC20


@pytest.fixture(scope="session")
def _plain_coins(alice, decimals):
    return_true_revert = [ERC20(decimals=precision, deployer=alice) for precision in decimals]
    return_true_false = [
        ERC20(fail=False, decimals=precision, deployer=alice) for precision in decimals
    ]
    return_none_revert = [
        ERC20(success=None, decimals=precision, deployer=alice) for precision in decimals
    ]
    return [return_true_revert, return_true_false, return_none_revert]


@pytest.fixture(scope="session")
def plain_coins(_plain_coins, return_type):
    return _plain_coins[return_type]


@pytest.fixture(scope="session")
def rebase_coins(alice, ATokenMock, decimals, lending_pool, plain_coins):
    return [
        ATokenMock.deploy(
            "Test Rebase Token", "TRT", precision, token, lending_pool, {"from": alice}
        )
        for precision, token in zip(decimals, plain_coins)
    ]


@pytest.fixture(scope="session")
def coins(plain_coins, rebase_coins, is_eth_pool, is_rebase_pool):
    if is_eth_pool:
        return [ETH_ADDRESS] + plain_coins[1:]
    elif is_rebase_pool:
        return rebase_coins
    else:
        return plain_coins


@pytest.fixture(scope="session")
def underlying_coins(plain_coins, is_rebase_pool):
    return plain_coins if is_rebase_pool else []


@pytest.fixture(scope="session")
def underlying_decimals(decimals):
    return decimals