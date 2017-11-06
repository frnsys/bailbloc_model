"""
For nonfelony cases.

Many assumptions are being made here,
in lieu of more detailed data.

Assuming these RVs are independent.
"""

POP_SIZE = 52465

# Assuming uniformly distributed within buckets
# For NYC, Figure 9, p47. [1]
# See also Appendix B
BAIL_DIST = [
    ((1, 25),        0.09),
    ((25, 499),      0.02),
    ((500, 500),     0.27),
    ((501, 999),     0.09),
    ((1000, 1000),   0.29),
    ((1001, 2499),   0.14),
    ((2500, 2500),   0.06),
    ((2501, 4999),   0.02),
    ((5000, 10000),  0.02),
]
# NOTE: <1% is above $10,000

# Table 7, p51, ibid
# Note that this does not distinguish nonfelony from felony
BAIL_MADE = [
    ((1, 25),       1.0), # not in the table, assume all made
    ((25, 499),     0.26),
    ((500, 500),    0.21),
    ((501, 999),    0.16),
    ((1000, 1000),  0.16),
    ((1001, 2499),  0.14),
    ((2500, 2500),  0.11),
    ((2501, 4999),  0.09),
    ((5000, 5000),  0.07),
    ((5001, 10000), 0.04),
]

# Assuming uniformally distributed within buckets
# For NYC, Figure 45
# p121, ibid
# In days
N = 5138
PRETRIAL_DETENTION_DIST = [
    ((0, 1),    1479/N),
    ((1, 7),    1853/N),
    ((8, 60),   1491/N),
    ((60, 200), 315/N)
]
# NOTE: 200 chosen as an arbitrary upper bound

# Figure 35, p96, ibid
ADJUSTED_FTA = 0.07

# p116, ibid
CONVICTION_RATE = 0.58

# https://www.theguardian.com/commentisfree/2013/feb/14/america-bail-system-law-rich-poor
CONVICTION_RATE_FROM_PLEA_DEAL = 0.996
