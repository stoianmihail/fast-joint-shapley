#include <cassert>
#include <cstdint>
#include <vector>
#include <cmath>

struct WrappedOutput {
  int size;
  double *result;
};

static constexpr bool isClose(double x, double y) { return std::fabs(x - y) < 1e-6; }
static constexpr std::size_t cardinality(uint64_t mask) { return __builtin_popcountll(mask); }

double* compute_naive(int n, int k, double* qs, double* vs)
// The naive algorithm.
{
  assert(isClose(vs[0], 0));
  double* phi = new double[1ull << n]();

  uint64_t full_mask = (1ull << n) - 1;
  for (uint64_t T = 1; T < (1ull << n); ++T) {
    // Allow only subsets of size <= `k`.
    if (cardinality(T) > k) continue;

    // Compute `N / T` in the equation.
    auto mask = T ^ full_mask;

    // Iterate all subsets of `N / T`.
    uint64_t current = 0;
    do {
      phi[T] += qs[cardinality(current)] * (vs[current | T] - vs[current]);
      current = (current - mask) & mask;
    } while (current);
  }
  return phi;
}

double* compute_moebius(int n, int k, double* qs, double* vs)
// The proposed algorithm.
{
  assert(isClose(vs[0], 0));
  double* phi = new double[1ull << n]();
  uint64_t full_mask = (1ull << n) - 1;

  // Fetch next mask with <= `q` bits. The mask will then be complemented.
  // This is partially function `subsets` from paper.
  auto next_compl_mask = [&](const unsigned q, const uint64_t mask, const unsigned compl_size) {
    // Enough bits? Then simply increment.
    if (compl_size < q)
      return mask + 1;

    // Level up the lower bits if we reached `q`. Then increment.
    return (mask | (mask - 1)) + 1;
  };

  // Compute the first term.
  // Compute `phi` for subsets of size `i`, in ascending order.
  for (unsigned i = 1; i <= k; ++i) {
    // Handle the case `k = n` separately.
    if (i == n) {
      phi[full_mask] = qs[0] * vs[full_mask];
      break;
    } else {
      // Initialize cf. Eq. (4)
      unsigned compl_size = 0;
      for (uint64_t compl_mask = 0; compl_mask <= full_mask; compl_mask = next_compl_mask(n - i, compl_mask, compl_size), compl_size = cardinality(compl_mask)) {
        auto mask = compl_mask ^ full_mask;
        phi[mask] = qs[(n - compl_size) - i] * vs[mask];
      }
    }

    // Perform computation cf. Eq. (5)
    for (unsigned j = 0; j != n; ++j) {
      unsigned compl_size = 0;
      for (uint64_t compl_mask = 0; compl_mask <= full_mask; compl_mask = next_compl_mask(n - i, compl_mask, compl_size), compl_size = cardinality(compl_mask)) {
        auto mask = compl_mask ^ full_mask;
        if (!(mask & (1ull << j)))
          phi[mask] += phi[mask ^ (1ull << j)];    
      }
    }
  }

  // Compute the second term.
  double *tmp = new double[1ull << n]();
  for (uint64_t T = 1; T <= full_mask; ++T)
    tmp[T] = qs[cardinality(T)] * vs[T];
  for (unsigned i = 0; i != n; ++i)
    for (uint64_t T = 1; T <= full_mask; ++T)
      if (T & (1ull << i))
        tmp[T] += tmp[T ^ (1ull << i)];

  // Update `phi`.
  for (uint64_t T = 1; T <= full_mask; ++T)
    // As discussed in the paper, the second term actually represents `\hat v_0(N \setminus T)`.
    if (cardinality(T) <= k)
      phi[T] -= tmp[T ^ full_mask];
    else
      phi[T] = 0;
  return phi;
}

extern "C" {
  WrappedOutput naive(int n, int k, double* qs, double* vs) {
    auto ret = compute_naive(n, k, qs, vs);
    return {1 << n, ret};
  }

  WrappedOutput moebius(int n, int k, double* qs, double* vs) {
    auto ret = compute_moebius(n, k, qs, vs);
    return {1 << n, ret};
  }
}