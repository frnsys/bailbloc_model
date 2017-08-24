import params
import numpy as np
from tqdm import tqdm
from mining import Mining
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor


# assuming sample is evenly distributed throughout the year
# though people accumulate over time
N_DAYS = 365
SIZE_PER_DAY = round(params.POP_SIZE/365)
BAIL_RANGES, BAIL_PROBS = zip(*params.BAIL_DIST)
DETENTION_RANGES, DETENTION_PROBS = zip(*params.PRETRIAL_DETENTION_DIST)


class Case:
    def __init__(self, amount, duration):
        self.amount = amount
        self.duration = duration


def generate_bail_sample():
    """generates an annual population
    we sample from"""
    # generate sample of bail ranges
    sample = np.random.choice(
        range(len(BAIL_RANGES)),
        size=params.POP_SIZE,
        replace=True,
        p=BAIL_PROBS)

    # count n people at each bail range
    unique, counts = np.unique(sample, return_counts=True)

    # for each bail range,
    # roll how many make/don't make bail
    not_made = {}
    for idx, n in zip(unique, counts):
        p = params.BAIL_MADE[idx][1]
        n_made = np.random.binomial(n, p)
        n_not_made = n - n_made
        not_made[idx] = n_not_made

    # sample bail amounts
    sample = []
    for idx, n in not_made.items():
        l, u = BAIL_RANGES[idx]
        amounts = np.random.uniform(l, u, size=n)
        sample.extend(amounts)

    # sample pretrial detention durations
    # assuming that these durations are independent
    # from bail amount, though I assume that they are actually
    # dependent. need to find data to use here.
    duration_idxs = np.random.choice(
        range(len(DETENTION_RANGES)),
        size=len(sample),
        replace=True,
        p=DETENTION_PROBS)
    durations = []
    for idx in duration_idxs:
        l, u = DETENTION_RANGES[idx]
        duration = np.random.uniform(l, u)
        durations.append(round(duration))
    sample = [Case(s, d) for s, d in zip(sample, durations)]
    return sample


def run_trial(seed):
    np.random.seed(seed)
    bail_fund = 0
    raised = 0
    released = 0

    mining = Mining()
    population = []
    awaiting_trial = []
    sample = generate_bail_sample()
    for day in range(N_DAYS):
        # monthly
        if day % 30 == 0:
            mined = mining.mine()
            bail_fund += mined
            raised += mined
        mining.update_miners()
        mining.update_price()

        population.extend(np.random.choice(sample, size=SIZE_PER_DAY, replace=False))
        _population = []
        for case in population:
            case.duration -= 1
            if case.duration > 0:
                _population.append(case)
        population = _population

        # assuming we want to maximize the amount
        # of people we get out on bail
        # so we sort by lowest amounts
        # we could also optimize for reducing overall pretrial duration by the most
        population = sorted(population, key=lambda c: c.amount)

        # gather reclaimed bail
        _awaiting_trial = []
        for case in awaiting_trial:
            case.duration -= 1
            if case.duration <= 0:
                # appeared at course
                if np.random.random() > params.ADJUSTED_FTA:
                    bail_fund += case.amount
            else:
                _awaiting_trial.append(case)
        awaiting_trial = _awaiting_trial

        # print('DAY', day)
        # print('  FUND: ${:.2f}'.format(bail_fund))
        # print('  RELEASED:', released)
        # print('  MINERS:', mining.n_miners)
        # print('  XMR>USD: ${:.2f}'.format(mining.price))

        # spend as much as we can
        while bail_fund > 0 and population:
            # sorted according to selection criteria
            case = population[0]
            if case.amount <= bail_fund:
                released += 1
                bail_fund -= case.amount
                population.pop(0)
                awaiting_trial.append(case)
            else:
                break

    print('TOTALS')
    print('  RAISED: ${:.2f}'.format(raised))
    print('  RELEASED:', released)

    return raised, released


def parallel(fn, n, n_jobs=None):
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        kwargs = {
            'total': n,
            'unit': 'i',
            'unit_scale': True,
            'leave': True
        }

        futures = executor.map(fn, [datetime.utcnow().timestamp() + i for i in range(n)])
        for f in tqdm(futures, **kwargs):
            yield f


if __name__ == '__main__':
    N_TRIALS = 100
    raiseds, releaseds = [], []
    for raised, released in parallel(run_trial, N_TRIALS):
        raiseds.append(raised)
        releaseds.append(released)

    print('MEANS')
    print('  RAISED: ${:.2f}'.format(sum(raiseds)/len(raiseds)))
    print('  RELEASED: ${:.2f}'.format(sum(releaseds)/len(releaseds)))