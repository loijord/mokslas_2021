import numpy as np
import igraph as ig
import matplotlib.pyplot as plt


class Match:
    def __init__(self, shift, thresbin=None):
        self.thresbin = thresbin  # thresbin by shift
        self.shift = shift  # shift needed to output nonzeros
        self._nonzero = None
        self._connections = None

    def _set_nonzero(self):
        if self._nonzero is None:
            self._nonzero = np.nonzero(self.thresbin)

    def get_nonzero(self):
        self._set_nonzero()
        return self._nonzero

    def _set_connections(self):
        # USE with care because self.get_nonzero sets a private self._connections only with reverse=False
        if self._connections is None:
            sx, sy = self.get_nonzero()
            start = (sx, sy)  # fancy indices if starts in 2D
            end = (sx + self.shift[0], sy + self.shift[1])  # fancy_indices in edge ends in 2D
            self._connections = (start, end)

    def get_connections(self):
        self._set_connections()
        return self._connections


class ArrData:
    def __init__(self, arr, es=None, bs=None):
        if es is None:
            es = {(0, 1): (None, None), (1, 0): (None, None)}
        if bs is None:
            bs = {(0, 1): (None, None), (1, 0): (None, None)}
        self.arr = arr
        self.es = es
        self.bs = bs
        self._graph = None

    def _set_edges(self, bs=True):
        for i, j in self.es.keys():
            diff = self.arr[i:, j:] == self.arr[:self.arr.shape[0] - i, :self.arr.shape[1] - j]
            interior = Match((i, j), diff).get_connections()
            self.es[i, j] = interior
            if bs:
                exterior = Match((i, j), ~diff).get_connections()
                self.bs[i, j] = exterior

    def get_edges(self, bs=True):
        if any(n[0] is None for n in self.es.values()):
            self._set_edges(bs=bs)
        if bs:
            return self.es, self.bs
        else:
            return (self.es,)

    def map_idx(self, idx):
        "maps 2D indices to 1D"
        return self.arr.shape[1] * idx[0] + idx[1]

    def unmap_idx(self, idx):
        "maps 1D indices back to original 2D"
        return np.divmod(idx, self.arr.shape[0])

    def _set_graph(self, bs=True, mode='dense'):
        es = self.get_edges(bs=bs)[0]
        edge_map_array = []

        for i, j in es.keys():
            start, end = es[i, j]
            start_idx, end_idx = self.map_idx(start), self.map_idx(end)  # map edge ends in 2D to image_idx in 1D
            edge_map_array.append(np.transpose([start_idx, end_idx]))
        edge_map_array = np.vstack(edge_map_array)

        g = ig.Graph()
        if mode == 'dense':
            # every pixel of image is included
            g.add_vertices(np.arange(self.arr.size))  # add vertices, in any order
            g.add_edges(edge_map_array)
        elif mode == 'sparse':
            raise NotImplementedError(
                "We didn't found a way to work with data of Lidar or not fully colored images yet")
            # You might consider only edges. It can't handle disconnected nodes in this case.
            u, inv = np.unique(edge_map_array, return_inverse=True)
            e = inv.reshape(edge_map_array.shape)
            g.add_vertices(u)  # add vertices, in any order
            g.add_edges(e)  # add edges, in reindexed order
        self._graph = g  # old indices are kept in g.vs

    def get_graph(self, bs=True, mode='dense'):
        if not self._graph:
            self._set_graph(bs=bs, mode=mode)
        return self._graph


def _setup_figure(arr, figsize, fig=None, ax=None, cmap=None):
    if (fig is None) and (ax is None):
        fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect('equal')
    ax.xaxis.set_tick_params(labeltop=True)
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.xaxis.tick_top()
    ax.set_yticks(np.arange(0, arr.shape[0], max(1, arr.shape[0] // 80)))
    ax.set_xticks(np.arange(0, arr.shape[1], max(1, arr.shape[1] // 30)))
    if cmap is not None:
        ax.imshow(arr, cmap=cmap)
    else:
        ax.imshow(np.zeros_like(arr), 'Greys') #we need to trick the system to force setting xticks properly via imshow
    return fig, ax


def _draw_cs(ax, start, end, draw_contour=False, draw_connector=False, k=0.3):
    #Draw nodes with respect to the size of pixels: https://stackoverflow.com/questions/48172928
    cslist = np.vstack([np.vstack(start), np.vstack(end)]).T
    for x1, y1, x2, y2 in cslist:
        if draw_connector:
            ax.add_patch(plt.Circle((y1, x1), radius=k, linewidth=4, ec='k', fc=(1, 1, 1, 0.8)))
            ax.add_patch(plt.Circle((y2, x2), radius=k, linewidth=4, ec='k', fc=(1, 1, 1, 0.8)))
            norm = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
            ax.plot((y1 + k * (y2 - y1) / norm, y2 - k * (y2 - y1) / norm),
                    (x1 + k * (x2 - x1) / norm, x2 - k * (x2 - x1) / norm), color='k', linewidth=4)
        if draw_contour:
            ax.plot((y1 + 0.5, y2 - 0.5), (x1 + 0.5, x2 - 0.5), color='b', linewidth=3)


def viz_arr(arr, labels=None, fig=None, ax=None, cmap=None, figsize=(20, 20), fontsize='large', color="g"):
    fig, ax = _setup_figure(arr, figsize, fig=fig, ax=ax, cmap=cmap)
    if labels is not None:
        for i in range(labels.shape[0]):
            for j in range(labels.shape[1]):
                plt.text(j, i, labels[i, j], ha="center", va="center", fontsize=fontsize, color=color)
    return fig, ax


def plot_bs(arr, fig=None, ax=None, cmap=None, figsize=(20, 20), with_bs=False, with_es=False, with_us=False, k=0.3):
    fig, ax = _setup_figure(arr, figsize, fig=fig, ax=ax, cmap=cmap)
    arrdata = ArrData(arr)
    g = arrdata.get_graph(bs=True)  # creates bs attribute in a silent way
    for s1, s2 in ((0, 1), (1, 0)):
        if with_bs:
            _draw_cs(ax, *arrdata.bs[s1, s2], draw_connector=True, draw_contour=True, k=k)
        else:
            _draw_cs(ax, *arrdata.bs[s1, s2], draw_contour=True, k=k)
        if with_es:
            _draw_cs(ax, *arrdata.es[s1, s2], draw_connector=True, k=k)
        if with_us:
            for idx in g.vs.select(_degree=0).indices:
                x, y = divmod(idx, arr.shape[1])
                ax.add_patch(plt.Circle((y, x), radius=k, linewidth=4, ec='k', fc=(1, 1, 1, 0.8)))
    return fig, ax, g
