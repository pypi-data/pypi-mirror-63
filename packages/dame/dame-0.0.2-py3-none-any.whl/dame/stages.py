from inspect import getfullargspec


class Stages:
    """DAG functionality for Dataset's transforms."""

    def __init__(self, source, transforms):
        self.stages = self.topsort(source, list(transforms))
        self.source = source

    def get_requirements(self, transform):
        return getfullargspec(transform.apply)[4]

    def topsort(self, source, transforms):
        """Sorts the transforms topologistagcally."""
        provider = {key: t for t in transforms for key in t.provides}
        self.provider = provider

        dependants = {t: set() for t in transforms}
        for t in transforms:
            for key in self.get_requirements(t):
                if key not in getattr(source, "provides", tuple()):
                    dependants[provider[key]].add(t)

        requires = {
            t: set(self.get_requirements(t)) - set(source.provides) for t in transforms
        }
        Q = [t for t, deps in requires.items() if len(deps) == 0]
        ordered = []
        while Q:
            t = Q.pop()
            ordered.append(t)
            for dependant in dependants[t]:
                provides = set(t.provides)
                requires[dependant] -= provides
                if len(requires[dependant]) == 0:
                    Q.append(dependant)
        assert len(ordered) == len(transforms), "Something is wrong with topsort!"
        return ordered

    def __iter__(self):
        return iter(self.stages)

    def __getitem__(self, idx):
        return self.stages[idx]

    def to(self, *keywords):
        result = set()
        Q = list([self.provider[kw] for kw in keywords])
        while Q:
            t = Q.pop()
            if t not in result:
                result.add(t)
                Q.extend(
                    set(
                        self.provider[kw]
                        for kw in self.get_requirements(t)
                        if kw not in getattr(self.source, "provides", tuple())
                    )
                )
        return filter(lambda t: t in result, self.stages)
