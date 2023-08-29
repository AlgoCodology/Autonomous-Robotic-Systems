
# !pip install celluloid
from celluloid import Camera
import requests
from io import BytesIO

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image

cmap = [(0, '#0074b3'), (0.45, '#eeeeee'), (1, '#fc0000')]
cmap = cm.colors.LinearSegmentedColormap.from_list('Custom', cmap, N=256)


class Rastrigin:

    def is_dim_compatible(cls, d):
        assert (d is None) or (isinstance(d, int) and (not d < 0)), "The dimension d must be None or a positive integer"
        return (d is None) or (d > 0)

    def __init__(self, d):
        self.d = d
        self.input_domain = np.array([[-5.12, 5.12] for _ in range(d)])

    def get_param(self):
        return {}

    def get_global_minimum(self, d):
        X = np.array([0 for _ in range(d)])
        return (X, self(X))

    def __call__(self, X):
        n = X.shape[0]
        res = 10 * n + np.sum(X ** 2 - 10 * np.cos(2 * np.pi * X), axis=0)
        return res


class Rosenbrock:

    def is_dim_compatible(cls, d):
        assert (d is None) or (isinstance(d, int) and (not d < 0)), "The dimension d must be None or a positive integer"
        return d == 2

    def __init__(self, d):
        self.d = d
        self.input_domain = np.array([[-20, 20] for _ in range(d)])

    def get_param(self):
        return {}

    def get_global_minimum(self, d):
        X = np.array([0, 0])
        return (X, self(X))

    def __call__(self, X):
        x, y = X
        res = (-x) ** 2 + 100 * (y - x ** 2) ** 2  # a=0 b=100
        return res


def plot_3d(function, n_space=1000, cmap=cmap, XYZ=None, ax=None, show=True):
    X_domain, Y_domain = function.input_domain
    if XYZ is None:
        X, Y = np.linspace(*X_domain, n_space), np.linspace(*Y_domain, n_space)
        X, Y = np.meshgrid(X, Y)
        XY = np.array([X, Y])
        Z = np.apply_along_axis(function, 0, XY)
    else:
        X, Y, Z = XYZ

    # create new ax if None
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')

    # Plot the surface.
    ax.plot_surface(X, Y, Z, cmap=cmap,
                    linewidth=0, antialiased=True, alpha=0.7)
    ax.contour(X, Y, Z, zdir='z', levels=30, offset=np.min(Z), cmap=cmap)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.xaxis.set_tick_params(labelsize=8)
    ax.yaxis.set_tick_params(labelsize=8)
    ax.zaxis.set_tick_params(labelsize=8)
    if show:
        #         plt.savefig("/home/zsy/桌面/%s.png") # save picture
        plt.show()


def plot_coordinate(ax=None):
    if X.any() != None and ax == None:
        ax = fig.add_subplot(1, 1, 1)
        ax.contourf(J, K, L, levels=30, cmap=cmap, alpha=0.7)

        # add labels and set equal aspect ratio
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_aspect(aspect='equal')
        ax.scatter(X[0], X[1], color='black', s=5)
        ax.scatter(min_coor[0], min_coor[1], color='#64ed5c', marker='v')
        camera.snap()


def decoding(pop):
    x_pop = pop[:, 0::2]
    y_pop = pop[:, 1::2]

    x = np.dot(x_pop, 2 ** np.arange(DNA_LEN)[::-1].reshape(DNA_LEN, 1)) / float(2 ** DNA_LEN - 1) * (
                X_BOUND[1] - X_BOUND[0]) + X_BOUND[0]
    y = np.dot(y_pop, 2 ** np.arange(DNA_LEN)[::-1].reshape(DNA_LEN, 1)) / float(2 ** DNA_LEN - 1) * (
                X_BOUND[1] - X_BOUND[0]) + X_BOUND[0]

    return np.concatenate((x.T, y.T), axis=0)


def selection(pop):
    X = decoding(pop)
    fit = function(X)
    offspring = pop[fit.argsort()[:5], :]
    new_population = np.repeat(offspring, int(pop.shape[0] / 5), axis=0)

    return new_population


def crossover_and_mutation(pop, crossover_rate):
    new_pop = []
    temp = pop
    while temp.size != 0:
        father_num = np.random.randint(0, int(temp.shape[0]))
        father = temp[father_num]
        child1 = father.copy()
        temp = np.delete(temp, father_num, axis=0)

        mother_num = np.random.randint(0, int(temp.shape[0]))
        mother = temp[mother_num]
        child2 = mother.copy()
        temp = np.delete(temp, mother_num, axis=0)

        if np.random.rand() < crossover_rate:
            cross_points = np.random.randint(low=0, high=DNA_LEN * 2)
            child1[cross_points:] = mother[cross_points:]
            child1 = mutation(child1)
            new_pop = np.concatenate((new_pop, child1), axis=0)
            child2[cross_points:] = father[cross_points:]
            child2 = mutation(child2)
            new_pop = np.concatenate((new_pop, child2), axis=0)
        else:
            new_pop = np.concatenate((new_pop, child1), axis=0)
            child1 = mutation(child1)
            new_pop = np.concatenate((new_pop, child2), axis=0)
            child2 = mutation(child2)

    return new_pop.reshape(-1, 2 * DNA_LEN)


def mutation(child, mutation_rate=0.003):
    if np.random.rand() < mutation_rate:
        mutate_point = np.random.randint(0, DNA_LEN * 2)
        if child[mutate_point] == 1:
            child[mutate_point] = 0
        elif child[mutate_point] == 0:
            child[mutate_point] = 1
    return child


function = Rastrigin(2)
X_BOUND, Y_BOUND = function.input_domain
POP_SIZE = 20
DNA_LEN = 24
CROSSOVER_RATE = 0.8
np.random.seed(2)
pop = np.random.randint(2, size=(POP_SIZE, DNA_LEN * 2))
X = decoding(pop)
fit = function(X)

n_space = 1000
J, K = np.linspace(*X_BOUND, n_space), np.linspace(*Y_BOUND, n_space)
J, K = np.meshgrid(J, K)
JK = np.array([J, K])
L = np.apply_along_axis(function, 0, JK)

min_coor, glo_min = function.get_global_minimum(2)

plot_3d(function, n_space=1000, ax=None)
fig = plt.figure()
camera = Camera(fig)

# plot_coordinate()
if X.any() != None:
    ax = fig.add_subplot(1, 1, 1)
    ax.contourf(J, K, L, levels=30, cmap=cmap, alpha=0.7)

    # add labels and set equal aspect ratio
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_aspect(aspect='equal')
    ax.scatter(X[0], X[1], color='black', s=5)
    ax.scatter(min_coor[0], min_coor[1], color='#64ed5c', marker='v')
    camera.snap()

n_iter = 50
for i in range(n_iter):
    pop = selection(pop)
    pop = crossover_and_mutation(pop, CROSSOVER_RATE)
    X = decoding(pop)
    #     plot_coordinate()

    if X.any() != None:
        ax = fig.add_subplot(1, 1, 1)
        ax.contourf(J, K, L, levels=30, cmap=cmap, alpha=0.7)

        # add labels and set equal aspect ratio
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_aspect(aspect='equal')
        ax.scatter(X[0], X[1], color='black', s=5)
        ax.scatter(min_coor[0], min_coor[1], color='#64ed5c', marker='v')
        camera.snap()

from IPython.display import HTML

animation = camera.animate(interval=250)
animation.save('/home/zsy/桌面/animation4.mp4')
HTML(animation.to_html5_video())