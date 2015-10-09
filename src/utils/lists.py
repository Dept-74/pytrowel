# -*- coding: utf-8 -*-

# @author: Romain DURAND


def insort(a, x, key=lambda x: x):
    """
    Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the right of the rightmost x.
    """
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if key(x) < key(a[mid]):
            hi = mid
        else:
            lo = mid+1
    a.insert(lo, x)


def bisect_right(a, x, key=lambda x: x):
    """
    Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.
    """

    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if key(x) < key(a[mid]):
            hi = mid
        else:
            lo = mid+1
    return lo


def bisect_left(a, x, key=lambda x: x):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.
    """

    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if key(a[mid]) < key(x):
            lo = mid+1
        else:
            hi = mid
    return lo
