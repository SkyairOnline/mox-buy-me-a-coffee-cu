from eth_utils import to_wei
import boa
from tests.conftest import SEND_VALUE

RANDOM_USER = boa.env.generate_address("non-owner")

def test_price_feed_is_coffee(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address, "Price feed address does not match the expected ETH/USD feed address."

def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address, "Owner address does not match the expected account address."

def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts("You must spend more ETH!"):
        coffee.fund()

def test_fun_with_money(coffee, account):
    # Arrange
    boa.env.set_balance(account.address, SEND_VALUE * 10)
    # Act
    coffee.fund(value=SEND_VALUE)
    # Assert
    funder = coffee.funders(0)
    assert funder == account.address, "Funder address does not match the expected account address"
    assert coffee.funder_to_amount_funded(funder) == SEND_VALUE, "Funder amount does not match the expected send value"

def test_non_owner_cannot_withdraw(coffee_funded, account):
    # Act & Assert
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            coffee_funded.withdraw()

def test_owner_cannot_withdraw(coffee_funded, account):
    # Arrange
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()
    assert boa.env.get_balance(coffee_funded.address) == 0, "Owner balance after withdrawal does not match expected value."

def test_withdraw_from_multiple_funders(coffee_funded):
    number_of_funders = 10
    for i in range(number_of_funders):
        user = boa.env.generate_address(i)
        boa.env.set_balance(user, SEND_VALUE * 2)
        with boa.env.prank(user):
            coffee_funded.fund(value=SEND_VALUE)
    starting_fund_me_balance = boa.env.get_balance(coffee_funded.address)
    starting_owner_balance = boa.env.get_balance(coffee_funded.OWNER())

    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()

    assert boa.env.get_balance(coffee_funded.address) == 0
    assert starting_fund_me_balance + starting_owner_balance == boa.env.get_balance(
        coffee_funded.OWNER()
    )

def test_get_rate(coffee):
    assert coffee.get_eth_to_usd_rate(SEND_VALUE) > 0, "ETH to USD rate should be greater than zero."