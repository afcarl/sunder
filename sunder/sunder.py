'''
A small Axes-splitting utility to make subplot positioning more pleasant.
'''

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import numpy as np


def split_axes(ax=None, x=None, y=None, select=None, exclude=None,
               flatten=False):
    '''
    Creates one more matplotlib Axes by "splitting" an existing Axes along the
    x and y dimensions.

    Args:
        ax (Axes, Figure): A reference matplotlib Axes or Figure instance used
            to define the boundaries of the new Axes. If a Figure is passed,
            the entire plot boundaries will be used as the reference (subject 
            to any limits imposed by the existing SubplotParams). If ax is
            None, a new Figure and Axes will be created.
        x (int, list): Specifies how to split the Axes along the x dimension.
            If an int is passed, the width of the reference Axes is divided
            evenly into this many new Axes. For example, if the width of the
            reference Axes is 400, and x = 8, each new Axes will have a width
            of 50 (with left edges respectively beginning at 0, 50, 100, etc.).
            If a list is passed, each element must be a 2-element list or
            tuple, where the first element is the left edge of the new Axes,
            and the second element is the right edge. Values are specified as
            a fraction of the original Axes width. For example, if the
            reference Axes spans (0.5, 1.0) in its parent Figure, passing the
            list [(0.1, 0.3), (0.7, 0.9)] as the x argument will create two
            new Axes with Figure x ranges of (0.55, 0.65) and (0.85, 0.95),
            respectively.
        y (int, list): Specifies how to split the Axes along the y dimension.
            Behaves identically to the x argument.
        select (int, iterable): Specifies which Axes to construct.
        exclude (list): specifies which Axes not to construct.
        flatten (bool): If True, the ndarray of Axes to be returned is
            flattened into a single list, and all non-initialized cells are
            removed.

    Returns:
        If only a single Axes is created, it is returned directly.
        Otherwise, a 1d or 2d numpy array containing multiple Axes is returned,
        with shape determined by the x and y arguments.

    Notes:
        When both the x and y arguments are passed, a grid is returned by
        combining all elements in each list in a pairwise manner. E.g.,
        passing x=4 and y=2 will return a 2d numpy array of shape (4, 2);
        passing x=[(0.1, 0.2), (0.05, 0.15)] and y=5 will return an array with
        shape (2, 5), and so on.

    '''
    if ax is None:
        ax = plt.gca()

    elif isinstance(ax, matplotlib.figure.Figure):
        ax = ax.gca()
    
    fig = ax.get_figure()
    bb = ax.get_position()
    
    def process_axis(bounds, start, span):

        if bounds is None:
            bounds = [(start, start + span)]

        else:
            if isinstance(bounds, int):
                s = 1. / float(bounds)
                _lower = np.arange(bounds) * s
                bounds = list(zip(list(_lower), list(_lower + s)))

            if isinstance(bounds, (list, tuple)):
                bounds = [(start+(b[0]*span), start+(b[1]*span)) for b in bounds]

        return bounds

    x = process_axis(x, bb.x0, bb.width)
    y = process_axis(y, bb.y0, bb.height)[::-1]
    nx, ny = len(x), len(y)

    # Mark cells to select or exclude
    valid_inds = np.ones((nx, ny))

    def get_array_inds(inds):
        if isinstance(inds, int):
            inds = [inds]
        _inds = []
        for i in inds:
            if isinstance(i, int):
                i = ((i-1) % ny, (i-1) // ny)
            _inds.append(tuple(i))
        return list(zip(*_inds))

    if select is not None:
        valid_inds *= 0
        valid_inds[get_array_inds(select)] = 1
    if exclude is not None:
        valid_inds[get_array_inds(exclude)] = 0

    axes = np.ndarray((nx, ny), dtype=np.object)
    for i, _x in enumerate(x):
        for j, _y in enumerate(y):
            if valid_inds[i, j]:
                bbox = Bbox([[_x[0], _y[0]], [_x[1], _y[1]]])
                axes[i, j] = fig.add_axes(bbox)

    if flatten:
        axes = [x for x in list(axes.ravel()) if x is not None]

    return axes
