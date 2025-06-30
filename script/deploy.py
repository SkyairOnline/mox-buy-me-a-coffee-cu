from moccasin.config import get_active_network
from src import buy_me_a_coffee
from moccasin.boa_tools import VyperContract

def deploy_coffee(price_feed: VyperContract) -> VyperContract:
    coffee: VyperContract = buy_me_a_coffee.deploy(price_feed)

    # active_network = get_active_network()
    # if active_network.has_explorer() and active_network.is_local_or_forked_network() is False:
    #     result = active_network.moccasin_verify(coffee)
    #     result.wait_for_verification()
    return coffee

def moccasin_main() -> VyperContract:
    active_network = get_active_network()
    price_feed: VyperContract = active_network.manifest_named("price_feed")

    print(f"Deploying Buy Me A Coffee on {active_network.name} with price feed at {price_feed.address}")
    return deploy_coffee(price_feed)