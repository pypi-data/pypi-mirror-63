import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import spsolve
from scipy.sparse import identity

from pymgrit.core.application import Application
from pymgrit.heat.vector_heat_1d_2pts import VectorHeat1D2Pts


class Heat1DBDF2(Application):
    """
    Heat equation 1-d example
    u_t - a*u_xx = b(x,t),  a > 0, x in [0,1], t in [0,T]
         u(0,t)  = u(1,t) = 0,   t in [0,T]
         u(x,0)  = sin(pi*x),    x in [0,1]
    with RHS b(x,t) = -sin(pi*x)(sin(t) - a*pi^2*cos(t))
    => solution u(x,t) = sin(pi*x)*cos(t)
    """

    def __init__(self, x_start, x_end, nx, dt, a, *args, **kwargs):
        super(Heat1DBDF2, self).__init__(*args, **kwargs)
        self.x_start = x_start
        self.x_end = x_end
        self.x = np.linspace(self.x_start, self.x_end, nx)
        self.x = self.x[1:-1]
        self.nx = nx - 2
        self.dt = dt
        self.a = a
        self.dx = self.x[1] - self.x[0]

        self.u_ex = self.u_exact_complete(x=self.x, t=np.linspace(self.t_start, self.t_end, (self.nt - 1) * 2 + 1))

        self.identity = identity(self.nx, dtype='float', format='csr')

        self.space_disc = self.compute_matrix()

        self.vector_template = VectorHeat1D2Pts(self.nx)  # Create initial value solution
        self.vector_t_start = VectorHeat1D2Pts(self.nx)
        self.vector_t_start.set_values(first_time_point=self.u_exact(self.x, self.t[0]),
                                       second_time_point=self.u_exact(self.x, self.t[0] + dt))

    def compute_matrix(self):
        """
        Space discretization
        """

        fac = self.a / self.dx ** 2

        diagonal = np.ones(self.nx) * (4 / 3) * fac
        lower = np.ones(self.nx - 1) * -(2 / 3) * fac
        upper = np.ones(self.nx - 1) * -(2 / 3) * fac

        matrix = sp.diags(
            diagonals=[diagonal, lower, upper],
            offsets=[0, -1, 1], shape=(self.nx, self.nx),
            format='csr')

        return matrix

    def u_exact(self, x, t):
        """
        Solution for one time point
        """
        return np.sin(np.pi * x) * np.cos(t)

    def f(self, x, t):
        """
        Right-hand-side
        """
        return - np.sin(np.pi * x) * (np.sin(t) - 1 * np.pi ** 2 * np.cos(t))

    def u_exact_complete(self, x, t):
        """
        Solution for all time points
        """
        ret = np.zeros((np.size(t), np.size(x)))
        for i in range(np.size(t)):
            ret[i] = self.u_exact(x, t[i])
        return ret

    def step(self, u_start: VectorHeat1D2Pts, t_start: float, t_stop: float) -> VectorHeat1D2Pts:
        """
        BDF2 in time
        """
        first, second = u_start.get_values()
        rhs = (4 / 3) * second - \
              (1 / 3) * first + \
              (2 / 3) * self.f(self.x, t_stop) * (t_stop - t_start - self.dt)

        tmp1 = spsolve((t_stop - t_start - self.dt) * self.space_disc + self.identity, rhs)

        rhs = (4 / 3) * tmp1 - \
              (1 / 3) * second + \
              (2 / 3) * self.f(self.x, t_stop + self.dt) * self.dt

        tmp2 = spsolve(self.dt * self.space_disc + self.identity, rhs)

        ret = VectorHeat1D2Pts(u_start.size)
        ret.set_values(first_time_point=tmp1, second_time_point=tmp2)

        return ret
