# Bail Bloc Simulation

When developing Bail Bloc, it became important for us to communicate its potential impact,

Given a number of participants ("miners") and period of months, this simulation estimates Bail Bloc's impact in terms of the accumulated bail fund and how many people this can release from pre-trial detention.

## Data

The data for this simulation were collected in part from the Bronx Freedom Fund's own statistics and [1], but primarily from [2].

In detail, the data used are (unless otherwise noted, these are all NYC-specific):

- A distribution of bail amounts less than or equal to $10,000(Figure 9, p47 of [1]).
    - In the paper these data are pre-bucketed; in lieu of individual information we assume that bails are uniformly distributed within these buckets.
    - The paper includes bail amounts above $10,000. This accounts for less than 1% of the population which we omitted, assuming our funds will be used for smaller amounts of bail.
- A distribution of what percentage within a bail bucket successfully makes bail (Table 7, p51 of [1]).
    - Bail amounts in the bucket [1, 25] are not included; we assume that 100% of bail in that bucket is made.
- A distribution of pretrial detention durations, in days (Figure 45,.p121 of [1]). There is no upper-bound described, so it is arbitrarily set as 200.
- Adjusted "failure to appear" (FTA) rate (Figure 35, p96 of [1]).

## Simulation Design

The simulation time interval is measured in months.

Each month, we sample a bail population based on the data above. This includes: bail amount, whether or not they pay it on their own, how long they will be detained for, and whether or not they will plead guilty (which could but doesn't necessarily indicate a plea deal).

We also compute a new XMR-to-USD price, modeled as a random walk (a monthly change is uniformly random on the interval `[-5%, 5%]`). For each miner, we also sample the XMR mined (directly as its estimated USD value) uniformly randomly from the interval `[$1, $4]`. This mined USD is added to the bail fund.

There needs to be some decision mechanism for determining who the bail fund is applied towards. The model optimizes for releasing the most people, so it releases as many people as possible, starting from the smallest bail amounts. The real-world decision process is obviously not this neat and is much more nuanced.

When a person's pre-trial detention time is up and they are out on bail we see if they appear for trial, according to the FTA rate (see above). If they appear, we recoup the bail amount back into the fund.

This process repeats for the number of months specified by the user.

We run the simulation 50 times and return the means of people released and amount raised across all runs.


## References

1. Phillips, M. T. (2012). A decade of bail research in New York City. CJA, New York City Criminal Justice Agency, Incorporated.
2. [The Price of Freedom: Bail and Pretrial Detention of Low Income Nonfelony Defendants in New York City](https://www.hrw.org/report/2010/12/02/price-freedom/bail-and-pretrial-detention-low-income-nonfelony-defendants-new-york). December 2, 2010. Humans Right Watch.