from unittest import TestCase
from routing.optimization.vrp_solver import VRPSolver

class TestVrpSolver(TestCase):

    _distance_matrix = [[0.0, 146.39], [158.62, 0.0]]

    _vrp_solve_spected = [[0, 1, 0]]
    def test_solve(self):
        vrps_solve = VRPSolver()
        vrps_result = vrps_solve.solve(self._distance_matrix, 1, 0)
        self.assertEqual(vrps_result, self._vrp_solve_spected)

