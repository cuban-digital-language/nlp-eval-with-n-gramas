try:
    from .progress_bar import get_progressbar
except (ModuleNotFoundError, ImportError):
    from progress_bar import get_progressbar


def get_n_grams_hash_list(n=3):
    def f(text: str):
        text = text.lower()
        index, len_, result = 0, len(text), []

        while index < len_:
            _break, next_index = False, index

            for i in range(index, len_):
                if text[i] == ' ':
                    _break = True
                if _break and text[i] != ' ':
                    next_index = i
                    break
            else:
                break

            n_gram, iter = '', n

            for i in range(index, len_):
                if text[i] == ' ':
                    iter -= 1
                if iter == 0:
                    break
                n_gram += text[i]

            result.append(hash(n_gram))
            index = next_index

        return result
    return f


class EvalPercentageNLModel:
    def __init__(self, n_grams_func) -> None:
        self.n_grams_func = n_grams_func
        self.memory = []
        self.len = 0

    def training(self, text_list):
        bar = get_progressbar(
            len(text_list), "  Learning all n grams in text list  ")

        bar.start()
        for i, text in enumerate(text_list):
            self.memory += self.n_grams_func(text)
            bar.update(i+1)

        bar.finish()
        self.memory = list(set(self.memory))
        self.memory.sort()
        self.len = len(self.memory)

    def eval(self, text):
        n_grams = self.n_grams_func(text)
        return sum([self.binary_search_in_memory(hsh) for hsh in n_grams])/len(n_grams)

    def binary_search_in_memory(self, value):
        l, r = 0, self.len
        while r != l:
            m = (l + r) >> 1
            if r < l:
                raise "Inverted Binary Search"
            if self.memory[m] == value:
                return 1

            if value < self.memory[m]:
                r = m
            if self.memory[m] < value:
                l = m + 1
        return 0
