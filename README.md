Fast Joint Shapley Values
====

The newly introduced [Joint Shapley](https://arxiv.org/abs/2107.11357) value provides a measure for the average contribution of a set of players to a coalition game. However, the current algorithm lies in $O(3^n \wedge 2^n n^k)$, where $k$ is the explanatory order.

We improve it to $O(2^n nk)$ for arbitrary $k$. This leads directly to more tractable insights for Explainable AI.

## Build

```
mkdir -p build
cd build
cmake ..
```

## Reproducibility

```
python3 bench.py 21 26
```

## Results

We compare both algorithms for different values of $n$ and $k = n$.

$n$ | $O(3^n)$ | $O(2^n n^2)$
--- | --- | --- |
21 | 23.25 s | 1.52 s
22 | 74.10 s | 3.39 s
23 | N/A | 7.21 s
24 | N/A | 15.32 s
25 | N/A | 31.86 s
26 | N/A | 67.15 s