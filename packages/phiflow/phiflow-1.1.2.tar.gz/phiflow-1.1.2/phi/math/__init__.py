from .base_backend import DYNAMIC_BACKEND
from .scipy_backend import SciPyBackend
from .struct_backend import StructBroadcastBackend
from .math_util import types, is_static_shape, zeros, ones, randn, randfreq
from .nd import (spatial_rank, spatial_dimensions, axes, all_dimensions,
                 is_scalar,
                 indices_tensor,
                 normalize_to,
                 batch_align, batch_align_scalar,
                 blur,
                 l1_loss, l2_loss, l_n_loss,
                 divergence, gradient, axis_gradient, laplace, fourier_laplace,
                 fftfreq,
                 downsample2x, upsample2x, interpolate_linear,
                 spatial_sum,)


# Setup Backend
DYNAMIC_BACKEND.add_backend(SciPyBackend())
DYNAMIC_BACKEND.add_backend(StructBroadcastBackend(DYNAMIC_BACKEND))

# Enable importing methods directly from math
choose_backend = DYNAMIC_BACKEND.choose_backend

abs = DYNAMIC_BACKEND.abs
add = DYNAMIC_BACKEND.add
all = DYNAMIC_BACKEND.all
any = DYNAMIC_BACKEND.any
as_tensor = DYNAMIC_BACKEND.as_tensor
batch_gather = DYNAMIC_BACKEND.batch_gather
boolean_mask = DYNAMIC_BACKEND.boolean_mask
cast = DYNAMIC_BACKEND.cast
ceil = DYNAMIC_BACKEND.ceil
cos = DYNAMIC_BACKEND.cos
dtype = DYNAMIC_BACKEND.dtype
equal = DYNAMIC_BACKEND.equal
floor = DYNAMIC_BACKEND.floor
concat = DYNAMIC_BACKEND.concat
conv = DYNAMIC_BACKEND.conv
dimrange = DYNAMIC_BACKEND.dimrange
divide_no_nan = DYNAMIC_BACKEND.divide_no_nan
dot = DYNAMIC_BACKEND.dot
exp = DYNAMIC_BACKEND.exp
expand_dims = DYNAMIC_BACKEND.expand_dims
fft = DYNAMIC_BACKEND.fft
flatten = DYNAMIC_BACKEND.flatten
gather = DYNAMIC_BACKEND.gather
ifft = DYNAMIC_BACKEND.ifft
imag = DYNAMIC_BACKEND.imag
isfinite = DYNAMIC_BACKEND.isfinite
is_tensor = DYNAMIC_BACKEND.is_tensor
matmul = DYNAMIC_BACKEND.matmul
max = DYNAMIC_BACKEND.max
maximum = DYNAMIC_BACKEND.maximum
mean = DYNAMIC_BACKEND.mean
min = DYNAMIC_BACKEND.min
minimum = DYNAMIC_BACKEND.minimum
name = DYNAMIC_BACKEND.name
ndims = DYNAMIC_BACKEND.ndims
ones_like = DYNAMIC_BACKEND.ones_like
pad = DYNAMIC_BACKEND.pad
py_func = DYNAMIC_BACKEND.py_func
random_uniform = DYNAMIC_BACKEND.random_uniform
range = DYNAMIC_BACKEND.range
real = DYNAMIC_BACKEND.real
resample = DYNAMIC_BACKEND.resample
reshape = DYNAMIC_BACKEND.reshape
round = DYNAMIC_BACKEND.round
sign = DYNAMIC_BACKEND.sign
size = DYNAMIC_BACKEND.size
scatter = DYNAMIC_BACKEND.scatter
shape = DYNAMIC_BACKEND.shape
sin = DYNAMIC_BACKEND.sin
sqrt = DYNAMIC_BACKEND.sqrt
stack = DYNAMIC_BACKEND.stack
staticshape = DYNAMIC_BACKEND.staticshape
std = DYNAMIC_BACKEND.std
sum = DYNAMIC_BACKEND.sum
prod = DYNAMIC_BACKEND.prod
tile = DYNAMIC_BACKEND.tile
to_complex = DYNAMIC_BACKEND.to_complex
to_float = DYNAMIC_BACKEND.to_float
to_int = DYNAMIC_BACKEND.to_int
unstack = DYNAMIC_BACKEND.unstack
where = DYNAMIC_BACKEND.where
while_loop = DYNAMIC_BACKEND.while_loop
with_custom_gradient = DYNAMIC_BACKEND.with_custom_gradient
zeros_like = DYNAMIC_BACKEND.zeros_like
