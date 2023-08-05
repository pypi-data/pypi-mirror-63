import inspect

"""
Taken from http://code.activestate.com/recipes/204197-solving-the-metaclass-conflict/ and slightly
modified
"""

__all__ = ['metaclass_maker']


def skip_redundant(iterable, skipset=None):
    """Redundant items are repeated items or items in the original skipset."""
    if skipset is None: skipset = set()
    for item in iterable:
        if item not in skipset:
            skipset.add(item)
            yield item


def remove_redundant(metaclasses):
    skipset = set([type])
    for meta in metaclasses:  # determines the metaclasses to be skipped
        skipset.update(inspect.getmro(meta)[1:])
    return tuple(skip_redundant(metaclasses, skipset))


memoized_metaclasses_map = {}


def get_noconflict_metaclass(bases, left_metas, right_metas):
    """Not intended to be used outside of this module, unless you know
    what you are doing."""
    # make tuple of needed metaclasses in specified priority order
    metas = left_metas + tuple(map(type, bases)) + right_metas
    needed_metas = remove_redundant(metas)

    # return existing confict-solving meta, if any
    if needed_metas in memoized_metaclasses_map:
        return memoized_metaclasses_map[needed_metas]
    # nope: compute, memoize and return needed conflict-solving meta
    elif not needed_metas:  # wee, a trivial case, happy us
        meta = type
    elif len(needed_metas) == 1:  # another trivial case
        meta = needed_metas[0]
    # check for recursion, can happen i.e. for Zope ExtensionClasses
    elif needed_metas == bases:
        raise TypeError("Incompatible root metatypes", needed_metas)
    else:  # gotta work ...
        metaname = '_' + ''.join([m.__name__ for m in needed_metas])
        meta = metaclass_maker_f()(metaname, needed_metas, {})
    memoized_metaclasses_map[needed_metas] = meta
    return meta


def metaclass_maker_f(left_metas=(), right_metas=()):
    def make_class(name, bases, adict):
        metaclass = get_noconflict_metaclass(bases, left_metas, right_metas)
        return metaclass(name, bases, adict)

    return make_class


def metaclass_maker(name, bases, adict):
    """
    Automatically construct a compatible meta-class like interface. Use like:

    >>> class C(A, B, metaclass=metaclass_maker):
    >>>     pass
    """
    metaclass = get_noconflict_metaclass(bases, (), ())
    return metaclass(name, bases, adict)
