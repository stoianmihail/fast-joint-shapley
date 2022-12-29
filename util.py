import os
import math
import time
import random
import numpy as np
import scipy.special

random.seed(0)

def choose(n, k):
  return scipy.special.comb(n, k)

def get_v_values(n):
  print(f'Compute v values..')
  v = [0] * (2**n)
  for i in range(1, 2**n):
    max_val = 0
    j = i
    if False:
      while j:
        least_power = j & -j
        max_val = max(max_val, v[i ^ least_power])
        j = j & (j - 1)
    max_val += random.randint(1, 10)
    v[i] = max_val
  return v

# Source: https://github.com/harris-chris/joint-shapley-values
def get_q_values(n, k):
  print(f'Compute q values..')
  q_values = np.zeros(n+1)
  q0_den = sum([choose(n, s) for s in range(1, k + 1)])
  
  q_values[0] = 1 / q0_den
  
  for r in range(1, n):
    lim_d = min(k, n - r)
    lim_n = max(r - k, 0)
    q_den = 0
    q_num = 0
    for s in range(1, lim_d + 1):
      q_den = q_den + choose(n - r, s)
        
    for s in range(lim_n, r):
      q_num = q_num + choose(r, s) * q_values[s]
          
    q_values[r] = q_num / q_den
  
  return q_values

class ChronoTool:
  def __init__(self, n):
    self.n = n
    self.active = None
    self.start = None
    self.all = {}

  def time(self):
    return time.time_ns() // 1_000_000

  def log(self, fn=''):
    assert fn
    assert self.active is None
    self.start = self.time()
    self.active = fn

  def finish(self):
    assert self.active is not None
    stop = self.time()
    self.all[self.active] = stop - self.start
    curr_time = self.all[self.active]
    self.active = None
    return curr_time

  def format(self, should_clean=False):
    def cleanse(s):
      if should_clean:
        pos = 0
        while pos != len(key) and key[pos] != ']':
          pos += 1
        return key[pos + 1:].strip()
      return s

    ret = f'Benchmark: n={self.n}\n'
    for key, val in dict(sorted(self.all.items(), key=lambda item: -item[1])).items():
      ret += f'{cleanse(key)}: {"{:.2f}".format(val)} ms\n'
    return f'{ret}\n'

  def debug(self):
    print(self.format(should_clean=False), end='')

  def flush(self):
    # Create the directory if it doesn't exist.
    os.system(f'mkdir -p results')

    # Write.
    with open(f'results/{self.n}.out', 'w') as f:
      f.write(self.format(True))
    pass
