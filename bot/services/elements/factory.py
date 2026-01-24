from bot.services.elements.strategy import PriceProvider

PROVIDERS = {
    "gold": PriceProvider("gold"),
    "silver": PriceProvider("silver"),
    "platinum": PriceProvider("platinum"),
    "palladium": PriceProvider("palladium"),
}

def get_provider(metal):
    return PROVIDERS.get(metal.lower())

def list_provider():
    return sorted(PROVIDERS.keys())