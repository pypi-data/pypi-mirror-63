import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import spsolve

from pymgrit.core import application
from pymgrit.heat_equation_bdf2 import vector_standard_bdf2


class HeatEquation(application.Application):
    """
    Heat equation 1-d example
    u_t - a*u_xx = b(x,t),  a > 0, x in [0,1], t in [0,T]
         u(0,t)  = u(1,t) = 0,   t in [0,T]
         u(x,0)  = sin(pi*x),    x in [0,1]
    with RHS b(x,t) = -sin(pi*x)(sin(t) - a*pi^2*cos(t))
    => solution u(x,t) = sin(pi*x)*cos(t)
    """

    def __init__(self, x_start, x_end, nx, dt, d, *args, **kwargs):
        super(HeatEquation, self).__init__(*args, **kwargs)
        self.x_start = x_start
        self.x_end = x_end
        self.x = np.linspace(self.x_start, self.x_end, nx)
        self.x = self.x[1:-1]
        self.nx = nx - 2
        self.dt = dt
        self.d = d

        self.u_ex = self.u_exact_complete(x=self.x, t=np.linspace(self.t_start, self.t_end, (self.nt - 1) * 2 + 1))

        self.a1 = self.heat_sparse(np.size(self.x), (self.d * (self.t[1] - self.t[0] - self.dt)) / (
                self.x[1] - self.x[0]) ** 2)  # setup matrix that acts in space for time integrator Phi
        self.a2 = self.heat_sparse(np.size(self.x), (self.d * self.dt) / (
                self.x[1] - self.x[0]) ** 2)  # setup matrix that acts in space for time integrator Phi

        self.u = vector_standard_bdf2.VectorStandardBDF2(self.nx)  # Create initial value solution
        self.u.vec_first_time_point = self.u_exact(self.x, self.t[0])  # Set initial value
        self.u.vec_second_time_point = self.u_exact(self.x, self.t[0] + dt)  # Set initial value

    @staticmethod
    def heat_sparse(nx, fac):
        """
        Central FD in space for bdf2
        """
        diagonal = np.zeros(nx)
        lower = np.zeros(nx - 1)
        upper = np.zeros(nx - 1)

        diagonal[:] = 1 + (4 / 3) * fac
        lower[:] = -(2 / 3) * fac
        upper[:] = -(2 / 3) * fac

        a = sp.diags(
            diagonals=[diagonal, lower, upper],
            offsets=[0, -1, 1], shape=(nx, nx),
            format='csr')

        return sp.csc_matrix(a)

    @staticmethod
    def u_exact(x, t):
        """
        Solution for one time point
        """
        return np.sin(np.pi * x) * np.cos(t)

    @staticmethod
    def f(x, t):
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

    def step(self, u_start: vector_standard_bdf2.VectorStandardBDF2, t_start: float,
             t_stop: float) -> vector_standard_bdf2.VectorStandardBDF2:
        """
        BDF2 in time
        """
        rhs = (4 / 3) * u_start.vec_second_time_point - \
              (1 / 3) * u_start.vec_first_time_point + \
              (2 / 3) * self.f(self.x, t_stop) * (t_stop - t_start - self.dt)

        tmp1 = spsolve(self.a1, rhs)

        rhs = (4 / 3) * tmp1 - \
              (1 / 3) * u_start.vec_second_time_point + \
              (2 / 3) * self.f(self.x, t_stop + self.dt) * self.dt

        tmp2 = spsolve(self.a2, rhs)

        ret = vector_standard_bdf2.VectorStandardBDF2(u_start.size)
        ret.vec_first_time_point = tmp1
        ret.vec_second_time_point = tmp2

        return ret
