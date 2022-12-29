import ctypes
import pathlib

class WrappedOutput(ctypes.Structure):
  _fields_ = [
    ("size", ctypes.c_int),
    ("result", ctypes.POINTER(ctypes.c_double))
  ]

def _make_array(arr):
  c_arr = (ctypes.c_double * len(arr))()
  for i in range(len(arr)):
    c_arr[i] = arr[i]
  return c_arr

def _transform(n, k, qs, vs):
  # Convert to C.
  return n, k, _make_array(qs), _make_array(vs)

libname = pathlib.Path().absolute() / "build/libjoint-shapley.so"
framework = ctypes.CDLL(libname)
framework.naive.restype = WrappedOutput
framework.moebius.restype = WrappedOutput

def _unwrap_result(wrapped):
  ret = [0] * (wrapped.size)
  for i in range(wrapped.size):
    ret[i] = wrapped.result[i]
  return ret

fn = {
  'naive' : framework.naive,
  'moebius' : framework.moebius,
}

def joint_shapley(algo, n, k, qs, vs):
  input = _transform(n, k, qs, vs)
  output = fn[algo](*input)
  return _unwrap_result(output)