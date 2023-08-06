"""
Vector and application class for the 1D heat equation
"""

import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import spsolve
from scipy.sparse import identity

from pymgrit.core.application import Application
from pymgrit.core.vector import Vector


class VectorHeat1D(Vector):
    """
    Vector class for the 1D heat equation
    """

    def __init__(self, size):
        super(VectorHeat1D, self).__init__()
        self.size = size
        self.values = np.zeros(size)

    def __add__(self, other):
        tmp = VectorHeat1D(self.size)
        tmp.set_values(self.get_values() + other.get_values())
        return tmp

    def __sub__(self, other):
        tmp = VectorHeat1D(self.size)
        tmp.set_values(self.get_values() - other.get_values())
        return tmp

    def norm(self):
        return np.linalg.norm(self.values)

    def clone_zero(self):
        return VectorHeat1D(self.size)

    def clone_rand(self):
        tmp = VectorHeat1D(self.size)
        tmp.set_values(np.random.rand(self.size))
        return tmp

    def set_values(self, values):
        self.values = values

    def get_values(self):
        return self.values


class Heat1D(Application):
    """
    Application class for the heat equation in 1D space,
        u_t - a*u_xx = b(x,t),  a > 0, x in [x_start,x_end], t in [0,T],
    """

    def __init__(self, x_start, x_end, nx, a, init_con_fnc=lambda x: x * 0, rhs=lambda x, t: x * 0, *args, **kwargs):
        super(Heat1D, self).__init__(*args, **kwargs)
        self.x_start = x_start  # lower interval bound of spatial domain
        self.x_end = x_end  # upper interval bound of spatial domain
        self.x = np.linspace(self.x_start, self.x_end, nx)  # spatial domain
        self.x = self.x[1:-1]  # homogeneous Dirichlet BCs
        self.nx = nx - 2  # update number of spatial unknowns due to BCs
        self.a = a  # diffusion coefficient
        self.dx = self.x[1] - self.x[0]  # spatial grid spacing
        self.identity = identity(self.nx, dtype='float', format='csr')  # Identity matrix
        self.init_con_fnc = init_con_fnc
        self.rhs = rhs

        # set spatial discretization matrix
        self.space_disc = self.compute_matrix()

        self.vector_template = VectorHeat1D(self.nx)
        self.vector_t_start = VectorHeat1D(self.nx)  # Create initial value solution
        self.vector_t_start.set_values(self.init_con_fnc(self.x))  # Set initial value

    def compute_matrix(self):
        """
        Define spatial discretization matrix for 1D heat equation

        Second-order central finite differences in space.
        """

        fac = self.a / self.dx ** 2

        diagonal = np.ones(self.nx) * 2 * fac
        lower = np.ones(self.nx - 1) * -fac
        upper = np.ones(self.nx - 1) * -fac

        matrix = sp.diags(
            diagonals=[diagonal, lower, upper],
            offsets=[0, -1, 1], shape=(self.nx, self.nx),
            format='csr')

        return matrix

    def step(self, u_start: VectorHeat1D, t_start: float, t_stop: float) -> VectorHeat1D:
        """
        Time integration routine for 1D heat equation example problem:
            Backward Euler in time

        At each time step i = 1, ..., nt+1, we obtain the linear system
        | 1+2ar   -ar                     | |  u_{1,i}   |   |  u_{1,i-1}   |   |  dt*b_{1,i}   |
        |  -ar   1+2ar  -ar               | |  u_{2,i}   |   |  u_{2,i-1}   |   |  dt*b_{2,i}   |
        |         ...   ...    ...        | |    ...     | = |     ...      | + |     ...       |
        |               -ar   1+2ar  -ar  | | u_{nx-1,i} |   | u_{nx-1,i-1} |   | dt*b_{nx-1,i} |
        |                      -ar  1+2ar | |  u_{nx,i}  |   |  u_{nx,i-1}  |   |  dt*b_{nx,i}  |

        with r = (dt/dx^2), which we denote by
            Mu_i = u_{i-1} + dt*b_i.
        This leads to the time-stepping problem u_i = M^{-1}(u_{i-1} + dt*b_i)
        which is implemented as time integrator function Phi u_i = Phi(u_{i-1}, t_{i}, t_{i-1}, app)

        :param u_start: approximate solution for the input time t_start
        :param t_start: time associated with the input approximate solution u_start
        :param t_stop: time to evolve the input approximate solution to
        :return: approximate solution at input time t_stop
        """
        tmp = u_start.get_values()
        tmp = spsolve((t_stop - t_start) * self.space_disc + self.identity,
                      tmp + self.rhs(self.x, t_stop) * (t_stop - t_start))
        ret = VectorHeat1D(len(tmp))
        ret.set_values(tmp)
        return ret
