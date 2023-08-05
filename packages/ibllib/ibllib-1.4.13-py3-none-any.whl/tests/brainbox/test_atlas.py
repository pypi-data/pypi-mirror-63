import unittest

import numpy as np

from brainbox.atlas import BrainCoordinates, sph2cart, cart2sph, Trajectory


class TestInsertion(unittest.TestCase):

    def test_eval_trajectory(self):
        line = Trajectory.fit(np.array([[0.3, 0.3, 0.4], [0, 0, 1]]))
        # test integer
        self.assertTrue(np.all(np.isclose(line.eval_y(0), np.array([0, 0, 1]))))
        # test float
        self.assertTrue(np.all(np.isclose(line.eval_y(0.0), np.array([0, 0, 1]))))
        # test list
        self.assertTrue(np.all(np.isclose(line.eval_y([0.0, 0.0]), np.array([0, 0, 1]))))
        # test array
        arr = np.array([0.0, 0.0])[..., np.newaxis]
        self.assertTrue(np.all(np.isclose(line.eval_y(arr), np.array([0, 0, 1]))))
        # test void direction
        vertical = Trajectory.fit(np.array([[0, 0, 0], [0, 0, 1]]))
        self.assertTrue(np.all(np.isnan(vertical.eval_x(5))))

    def test_trajectory(self):
        np.random.seed(42)
        xyz = np.zeros([120, 3])
        xyz[:, 0] = np.linspace(1, 9, 120)
        xyz[:, 1] = np.linspace(2, 4, 120)
        xyz[:, 2] = np.linspace(-2, 3, 120)
        xyz += np.random.normal(size=xyz.shape) * 0.4
        traj = Trajectory.fit(xyz)
        # import matplotlib.pyplot as plt
        # import mpl_toolkits.mplot3d as m3d
        # ax = m3d.Axes3D(plt.figure())
        # ax.scatter3D(*xyz.T)
        # ax.plot3D(*insertion.eval_x(np.array([0, 10])).T)
        # ax.plot3D(*insertion.eval_y(xyz[:, 1]).T, 'r')
        d = xyz[:, 0] - traj.eval_y(xyz[:, 1])[:, 0]
        self.assertTrue(np.abs(np.mean(d)) < 0.001)
        d = xyz[:, 0] - traj.eval_y(xyz[:, 1])[:, 0]
        self.assertTrue(np.abs(np.mean(d)) < 0.001)
        d = xyz[:, 1] - traj.eval_z(xyz[:, 2])[:, 1]
        self.assertTrue(np.abs(np.mean(d)) < 0.001)

    def test_exit_volume(self):
        bc = BrainCoordinates((11, 13, 15), xyz0=(-5, -6, -7))
        # test arbitrary line
        line = Trajectory.fit(np.array([[0.1, 0.1, 0], [0, 0, 1]]))
        epoints = Trajectory.exit_points(line, bc)
        self.assertTrue(np.all(np.isclose(epoints, np.array([[0.8, 0.8, -7.], [-0.6, -0.6, 7.]]))))
        # test apline
        hline = Trajectory.fit(np.array([[0, 0, 0], [0, 1, 0]]))
        epoints = Trajectory.exit_points(hline, bc)
        self.assertTrue(np.all(np.isclose(epoints, np.array([[0, -6, 0], [0, 6, 0]]))))
        # test mlline
        hline = Trajectory.fit(np.array([[0, 0, 0], [1, 0, 0]]))
        epoints = Trajectory.exit_points(hline, bc)
        self.assertTrue(np.all(np.isclose(epoints, np.array([[-5, 0, 0], [5, 0, 0]]))))
        # test vertical line
        vline = Trajectory.fit(np.array([[0, 0, 0], [0, 0, 1]]))
        epoints = Trajectory.exit_points(vline, bc)
        self.assertTrue(np.all(np.isclose(epoints, np.array([[0, 0, -7.], [0, 0, 7.]]))))


class TestsCoordinatesSimples(unittest.TestCase):

    def test_brain_coordinates(self):
        vshape = (6, 7, 8)
        bc = BrainCoordinates(vshape)
        self.assertTrue(bc.i2x(0) == 0)
        self.assertTrue(bc.i2x(6) == 6)
        self.assertTrue(bc.nx == 6)
        self.assertTrue(bc.ny == 7)
        self.assertTrue(bc.nz == 8)
        # test array functions
        in_out = [([6, 7, 8], np.array([6, 7, 8])),
                  (np.array([6, 7, 8]), np.array([6, 7, 8])),
                  (np.array([[6, 7, 8], [6, 7, 8]]), np.array([[6, 7, 8], [6, 7, 8]])),
                  ]
        for io in in_out:
            self.assertTrue(np.all(bc.xyz2i(io[0]) == io[1]))
            self.assertTrue(np.all(bc.i2xyz(io[1]) == io[0]))

    def test_reverse_directions(self):
        bc = BrainCoordinates(nxyz=(6, 7, 8), xyz0=[50, 60, 70], dxyz=[-10, -10, -10])
        self.assertTrue(bc.i2x(0) == 50 and bc.i2x(bc.nx - 1) == 0)
        self.assertTrue(bc.i2y(0) == 60 and bc.i2y(bc.ny - 1) == 0)
        self.assertTrue(np.all(bc.i2z(np.array([0, 1])) == np.array([70, 60])))
        bc = BrainCoordinates(nxyz=(6, 7, 8), xyz0=[50, 60, 70], dxyz=-10)
        self.assertTrue(bc.dx == bc.dy == bc.dz == -10)

    def test_sph2cart_and_back(self):
        dv = np.array([0, -1, 1, 0, 0, 0, 0, 0, 0])  # z
        ml = np.array([0, 0, 0, 0, -1, 1, 0, 0, 0])  # x
        ap = np.array([0, 0, 0, 0, 0, 0, 0, -1, 1])  # y

        theta = np.array([0., 0., 0., 0., 180., 0., 0., -90., 90.])
        phi = np.array([0., 180., 0., 0., 90., 90., 0., 90., 90.])
        r = np.array([0., 1, 1, 0., 1, 1, 0., 1, 1])

        r_, t_, p_ = cart2sph(ml, ap, dv)
        assert np.all(np.isclose(r, r_))
        assert np.all(np.isclose(phi, p_))
        assert np.all(np.isclose(theta, t_))

        x_, y_, z_ = sph2cart(r, theta, phi)
        assert np.all(np.isclose(ml, x_))
        assert np.all(np.isclose(ap, y_))
        assert np.all(np.isclose(dv, z_))


if __name__ == "__main__":
    unittest.main(exit=False)
