import numpy as np

XMR_USD_START = 85

# bittrex commission fee
COMMISSION_FEE = 0.0025


class Mining:
    def __init__(self):
        self.price = XMR_USD_START
        self.n_miners = 0
        self.params = {
            'XMR_PER_MONTH_PER_PERSON_MEAN': np.random.beta(a=2, b=2),
            'XMR_PER_MONTH_PER_PERSON_STD': np.random.beta(a=2, b=2),
            'DAILY_MINER_GROWTH_MEAN': np.random.normal(loc=1, scale=5),
            'DAILY_MINER_GROWTH_STD': np.random.beta(a=2, b=2),
            'XMR_DAILY_PRICE_CHANGE_MEAN': np.random.normal(loc=0.01, scale=0.1),
            'XMR_DAILY_PRICE_CHANGE_STD': np.random.beta(a=2, b=2)/2,
        }

    def mine(self):
        xmr = np.random.normal(
            loc=self.params['XMR_PER_MONTH_PER_PERSON_MEAN'],
            scale=self.params['XMR_DAILY_PRICE_CHANGE_STD'],
            size=self.n_miners)
        total = self.price * xmr.sum()
        return total * (1 - COMMISSION_FEE)

    def update_price(self):
        """using a random walk model"""
        self.price += np.random.normal(
            loc=self.params['XMR_DAILY_PRICE_CHANGE_MEAN'],
            scale=self.params['XMR_DAILY_PRICE_CHANGE_STD']
        )
        self.price = max(0, self.price)

    def update_miners(self):
        """using a random walk model"""
        self.n_miners += np.random.normal(
            loc=self.params['DAILY_MINER_GROWTH_MEAN'],
            scale=self.params['DAILY_MINER_GROWTH_STD'])
        self.n_miners = max(0, self.n_miners)
        self.n_miners = round(self.n_miners)
