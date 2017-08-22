import numpy as np

XMR_USD_START = 85
XMR_PER_MONTH_PER_PERSON_MEAN = 0.05
XMR_PER_MONTH_PER_PERSON_STD = 0.02 # guessing

# also guesses
DAILY_MINER_GROWTH_MEAN = 1
DAILY_MINER_GROWTH_STD = 2
XMR_DAILY_PRICE_CHANGE_MEAN = 0.01
XMR_DAILY_PRICE_CHANGE_STD = 0.1 # volatility

# bittrex commission fee
COMMISSION_FEE = 0.0025


class Mining:
    def __init__(self):
        self.price = XMR_USD_START
        self.n_miners = 0

    def mine(self):
        xmr = np.random.normal(
            loc=XMR_PER_MONTH_PER_PERSON_MEAN,
            scale=XMR_PER_MONTH_PER_PERSON_STD,
            size=self.n_miners)
        total = self.price * xmr.sum()
        return total * (1 - COMMISSION_FEE)

    def update_price(self):
        """using a random walk model"""
        self.price += np.random.normal(
            loc=XMR_DAILY_PRICE_CHANGE_MEAN,
            scale=XMR_DAILY_PRICE_CHANGE_STD
        )
        self.price = max(0, self.price)

    def update_miners(self):
        """using a random walk model"""
        self.n_miners += np.random.normal(
            loc=DAILY_MINER_GROWTH_MEAN,
            scale=DAILY_MINER_GROWTH_STD)
        self.n_miners = max(0, self.n_miners)
        self.n_miners = round(self.n_miners)
