from dame.versionable import Versionable


class PlusOne(Versionable):
    provides = ("p1",)

    def apply(self, *, number):
        return {"p1": number + 1}


class PlusTwo(Versionable):
    provides = ("p2",)

    def apply(self, *, p1):
        return {"p2": p1 + 1}


class PlusXN(Versionable):

    provides = ("pxn",)

    def __init__(self, x, n=0):
        self.x = x
        self.n = n

    def apply(self, *, number):
        return {"pxn": number + self.x ** self.n}


class ThreeNums:
    provides = ("number",)

    def __getitem__(self, idx):
        if idx > 2 or idx < 0:
            raise IndexError
        return {"number": idx}

    def __len__(self):
        return 3
