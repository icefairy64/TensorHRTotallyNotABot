# -*- encoding: utf-8 -*-

class defaultlist(list):
    def __init__(self, fx=int):
        self._fx = fx

    def __setitem__(self, index, value):
        while len(self) <= index:
            self.append(self._fx())
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        while len(self) <= index:
            self.append(self._fx())
        return list.__getitem__(self, index)

def damerau_levenstein_distance(s, t):
    """
    Функция, возвращающая расстояние Дамерау-Левенштейна между двумя словами
    """
    len_s = len(s)
    len_t = len(t)
    if len_s == 0:
        if len_t == 0:
            return 0
        else:
            return len_t
    elif len_t == 0:
        return len_s

    replace_cost = 1
    insert_cost = 1
    delete_cost = 1
    transpose_cost = 1

    dyn = defaultlist(defaultlist) # База индукции
    len_sum = len_s + len_t

    dyn[0][0] = len_sum
    for i, letter in enumerate(s):
        dyn[i + 1][0] = len_sum
        dyn[i + 1][1] = i

    for j, letter in enumerate(t):
        dyn[1][j + 1] = j
        dyn[0][j + 1] = len_sum

    last_positions = {l: 0 for l in set(list(s + t))}

    for i in range(1, len_s):
        last = 0
        for j in range(1, len_t):
            i_ = last_positions[t[j]]
            j_ = last
            if s[i] == t[j]:
                dyn[i + 1][j + 1] = dyn[i][j]
                last = j
            else:
                dyn[i + 1][j + 1] = min(dyn[i][j] + replace_cost,
                                        dyn[i + 1][j] + insert_cost,
                                        dyn[i][j + 1] + delete_cost)
            dyn[i + 1][j + 1] = min(dyn[i + 1][j + 1],
                                    dyn[i_][j_] + (i - i_ - 1) * delete_cost +\
                                    transpose_cost + (j - j_ - 1) * insert_cost)
        last_positions[s[i]] = i

    return dyn[len_s][len_t]

