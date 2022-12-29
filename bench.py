import os
import sys
from util import *

from wrapper import joint_shapley

def main(lb, ub):
  algos = [
    'naive',
    'moebius'
  ]

  DEBUG = True

  disable_naive = False
  for n in range(lb, ub + 1):
    print(f'Generate values..')
    vs = get_v_values(n)
    qs = get_q_values(n, n)
    print(f'Finished computing values..')

    if DEBUG:
      phis = []

    tool = ChronoTool(n)
    for algo in algos:
      if algo == 'naive' and disable_naive:
        continue
      print(f'{algo}')
      tool.log(f'{algo}')
      phi = joint_shapley(algo, n, n, qs, vs)
      if DEBUG:
        phis.append(phi)
      curr_time = tool.finish()

      # Timeout of 2 mins.
      if algo == 'naive' and (curr_time / 1000) / 60 > 2.0:
        disable_naive = True

    tool.debug()

    del vs
    del qs

    if DEBUG:
      for i in range(len(phis)):
        for j in range(i + 1, len(phis)):
          if not len(phis[i]) or not len(phis[j]):
            continue
          assert np.allclose(phis[i], phis[j])

if __name__ == '__main__':
  import sys
  if len(sys.argv) != 3:
    print(f'Usage: python3 {sys.argv[0]} <lb:int> <ub:int>')
    sys.exit(-1)

  lb, ub = [int(x) for x in sys.argv[1:]]
  assert lb <= ub
  main(lb, ub)