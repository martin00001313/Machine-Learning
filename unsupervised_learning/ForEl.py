import numpy as np

R = 30  # compute via genetic alorith or smth. else


def load_data():
    return np.array([[1,2,3], [4,5,6]])


def norm(d1, d2):
    return np.sqrt(np.sum(np.power(np.array(d1) - np.array(d2), 2)))


def get_ceneter(data):
    min = None
    min_value = None
    for i in data:
        tmp_dist = np.sum(np.array(norm(i, j) for j in data if i != j))
        if min_value is None or min_value > tmp_dist:
            min = i
            min_value = tmp_dist
    return min


def ForEl(data):
    unmarked_data = data
    gen_clusters = []
    while len(unmarked_data) != 0:
        rd_idx = np.random.choice(unmarked_data)
        center_el = unmarked_data[rd_idx]
        assert rd_idx < len(unmarked_data), "MA13: error"
        cur_cluster = [i for i in unmarked_data if norm(i, center_el) < R]
        tmp_el = get_ceneter(cur_cluster)
        while center_el != tmp_el:
            center_el = tmp_el
            cur_cluster = [i for i in unmarked_data if norm(i, center_el) < R]
            tmp_el = get_ceneter(cur_cluster)
        gen_clusters.append((center_el, cur_cluster))
        unmarked_data = [i for i in unmarked_data if i not in cur_cluster]
    #    unmarked_data = list(filter(lambda x : x not in cur_cluster, unmarked_data))
    return gen_clusters


if __name__ == "__main__":
    x = load_data()
    print(x)
    #l = [norm(i, j) for i, j in zip(x, x)]
    print(norm([1,],[2,]))