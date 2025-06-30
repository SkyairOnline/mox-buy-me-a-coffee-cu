from src import buy_me_a_coffee
from moccasin.config import get_active_network

def withdraw():
    active_network = get_active_network()
    coffee = active_network.manifest_named("buy_me_a_coffee")
    print(f"Withdrawing from Buy Me A Coffee on {active_network.name} at {coffee.address}")
    coffee.withdraw()

def moccasin_main():
    return withdraw()