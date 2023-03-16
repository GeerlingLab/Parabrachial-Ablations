import numpy as np
import matplotlib.pyplot as plt
def simple_beeswarm(y, x_mean=0, x_var=1, nbins=None):
    """
    Returns x coordinates for the points in ``y``, so that plotting ``x`` and
    ``y`` results in a bee swarm plot.
    """
    y = np.asarray(y)
    if nbins is None:
        nbins = len(y) // 3

    # Get upper bounds of bins
    x = np.zeros(len(y))
    ylo = np.min(y)
    yhi = np.max(y)
    dy = (yhi - ylo) / nbins
    ybins = np.linspace(ylo + dy, yhi - dy, nbins - 1)

    # Divide indices into bins
    i = np.arange(len(y))
    ibs = [0] * nbins
    ybs = [0] * nbins
    nmax = 0
    for j, ybin in enumerate(ybins):
        f = y <= ybin
        ibs[j], ybs[j] = i[f], y[f]
        nmax = max(nmax, len(ibs[j]))
        f = ~f
        i, y = i[f], y[f]
    ibs[-1], ybs[-1] = i, y
    nmax = max(nmax, len(ibs[-1]))

    # Assign x indices
    dx = x_var / (nmax // 2)
    for i, y in zip(ibs, ybs):
        if len(i) > 1:
            j = len(i) % 2
            i = i[np.argsort(y)]
            a = i[j::2]
            b = i[j + 1::2]
            x[a] = (0.5 + j / 3 + np.arange(len(b))) * dx
            x[b] = (0.5 + j / 3 + np.arange(len(b))) * -dx
    return x + x_mean


def fillan_bee_swarm(y, x_mean, x_var, x_marker_size=1.0, y_marker_size=None):
    def create_active_xs(active_markers):
        x = []
        if len(active_markers) % 2 == 0:
            current_x = -x_marker_size / 2
            for _ in active_markers:
                x.append(current_x)
                current_x = -current_x
                if current_x < 0:
                    current_x -= x_marker_size
        else:
            current_x = 0
            for _ in active_markers:
                x.append(current_x)
                current_x = -current_x
                if current_x <= 0:
                    current_x -= x_marker_size
        return x

    x = []
    if len(y) == 0:
        return []
    sorting_order = [b[0] for b in sorted(enumerate(y), key=lambda i: i[1])]
    y = sorted(y)
    if y_marker_size is None:
        range = y[-1] - y[0]
        y_marker_size = 4 * range / len(y)
    active_markers = [y[0]]
    for s in y[1:]:
        if s - active_markers[0] > y_marker_size or len(active_markers) * x_marker_size > x_var * 2:
            x.extend(create_active_xs(active_markers))
            active_markers = []
        active_markers.append(s)
    x.extend(create_active_xs(active_markers))

    unsorted_xs = [0] * len(y)
    for s, o in zip(sorting_order, x):
        unsorted_xs[s] = o + x_mean
    return unsorted_xs

if __name__ == "__main__":
    fig = plt.figure()
    fig.subplots_adjust(0.2, 0.1, 0.98, 0.99)
    ax = fig.add_subplot(1, 1, 1)
    #np.random.seed(0)
    y = np.random.gamma(20, 10, 50)
    x = fillan_bee_swarm(y, x_mean=5, x_var=5, x_marker_size=.5, y_marker_size=None)
    ax.plot(x, y, 'o')
    plt.xlim([0, 10])
    plt.show()