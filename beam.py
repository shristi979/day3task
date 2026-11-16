# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 21:02:56 2026

@author: LOQ
"""

def canti_udl(x,beam):
    w = beam["w"]
    L = beam["L"]
    E = beam["E"]
    I = beam["I"]
    
    if x < 0 or x > L:
        raise ValueError("Position x must be between 0 and L")

    y = (w * x**2 * (6 * L**2 - 4 * L * x + x**2)) / (24 * E * I)

    return y


def canti_end_point(x, beam):

    P = beam["P"]
    L = beam["L"]
    E = beam["E"]
    I = beam["I"]

    if x < 0 or x > L:
        raise ValueError("Position x must be between 0 and L")

    y = (P * x**2 * (3 * L - x)) / (6 * E * I)

    return y

def ss_udl(x, beam):

    w = beam["w"]
    L = beam["L"]
    E = beam["E"]
    I = beam["I"]

    if x < 0 or x > L:
        raise ValueError("Position x must be between 0 and L")

    y = (w * x * (L**3 - 2 * L * x**2 + x**3)) / (24 * E * I)

    return y

def _offcenter_left(x, beam):

    P = beam["P"]
    L = beam["L"]
    a = beam["a"]
    b = L - a
    E = beam["E"]
    I = beam["I"]

    y = (P * b * x * (L**2 - b**2 - x**2)) / (6 * L * E * I)

    return y


def _offcenter_right(x, beam):

    P = beam["P"]
    L = beam["L"]
    a = beam["a"]
    E = beam["E"]
    I = beam["I"]

    y = (P * a * (L - x) *
         (L**2 - a**2 - (L - x)**2)) / (6 * L * E * I)

    return y


def ss_off_center_point(x, beam):

    L = beam["L"]
    a = beam["a"]

    if x < 0 or x > L:
        raise ValueError("Position x must be between 0 and L")

    if not 0 < a < L:
        raise ValueError("Off-center load position must be inside the span")

    if x <= a:
        return _offcenter_left(x, beam)

    else:
        return _offcenter_right(x, beam)
    
    
def _center_left(x, beam):

    P = beam["P"]
    L = beam["L"]
    E = beam["E"]
    I = beam["I"]

    y = (P * x * (3 * L**2 - 4 * x**2)) / (48 * E * I)

    return y


def _center_right(x, beam):

    P = beam["P"]
    L = beam["L"]
    E = beam["E"]
    I = beam["I"]

    y = (P * (L - x) *
         (3 * L**2 - 4 * (L - x)**2)) / (48 * E * I)

    return y


def ss_center_point(x, beam):

    L = beam["L"]

    if x < 0 or x > L:
        raise ValueError("Position x must be between 0 and L")

    if x <= L / 2:
        return _center_left(x, beam)

    else:
        return _center_right(x, beam)