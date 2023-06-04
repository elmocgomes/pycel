# -*- coding: UTF-8 -*-
#
# Copyright 2011-2019 by Dirk Gorissen, Stephen Rauch and Contributors
# All rights reserved.
# This file is part of the Pycel Library, Licensed under GPLv3 (the 'License')
# You may not use this work except in compliance with the License.
# You may obtain a copy of the Licence at:
#   https://www.gnu.org/licenses/gpl-3.0.en.html

"""
Python equivalents of various excel functions
"""
import math
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP, ROUND_UP

import numpy as np

from pycel.excelutil import (
    coerce_to_number,
    DIV0,
    ERROR_CODES,
    flatten,
    handle_ifs,
    is_array_arg,
    is_number,
    list_like,
    NA_ERROR,
    NUM_ERROR,
    VALUE_ERROR,
)
from pycel.lib.function_helpers import (
    excel_helper,
    excel_math_func,
)


def _numerics(*args, keep_bools=False, to_number=lambda x: x):
    # ignore non numeric cells
    args = tuple(flatten(args))
    error = next((x for x in args if x in ERROR_CODES), None)
    if error is not None:
        # return the first error in the list
        return error
    else:
        args = (
            to_number(a) for a in args if keep_bools or not isinstance(a, bool)
        )
        return tuple(x for x in args if isinstance(x, (int, float)))


@excel_math_func
def abs_(value1):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ABS-function-3420200F-5628-4E8C-99DA-C99D7C87713C
    return abs(value1)

@excel_math_func
def acos(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ACOS-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.acos(value)


@excel_math_func
def acosh(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ACOSH-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.acosh(value)

@excel_math_func
def asin(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ASIN-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.asin(value)

@excel_math_func
def asinh(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ASINH-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.asinh(value)

@excel_math_func
def atan(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ATAN-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.atan(value)

@excel_math_func
def atan2_(x_num, y_num):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ATAN2-function-C04592AB-B9E3-4908-B428-C96B3A565033

    # swap arguments
    return math.atan2(y_num, x_num)

@excel_math_func
def atanh(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ATANH-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.atanh(value)


@excel_math_func
def averagea(*args):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   AVERAGEA-function-047BAC88-D466-426C-A32B-8F33EB960CF6
    data = _numerics(*args, keep_bools=True)
    if isinstance(data, str):
        return data

    # if no non numeric cells, return zero (is what excel does)
    return np.mean(data) if data else 0


@excel_math_func
def ceiling(number, significance):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   CEILING-function-0A5CD7C8-0720-4F0A-BD2C-C943E510899F
    if significance < 0 < number:
        return NUM_ERROR

    if number == 0 or significance == 0:
        return 0

    if number < 0 < significance:
        return significance * int(number / significance)
    else:
        return significance * math.ceil(number / significance)


@excel_math_func
def ceiling_math(number, significance=1, mode=0):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ceiling-math-function-80f95d2f-b499-4eee-9f16-f795a8e306c8
    if significance == 0:
        return 0

    significance = abs(significance)
    if mode and number < 0:
        significance = -significance
    return significance * math.ceil(number / significance)



@excel_math_func
def ceiling_precise(number, significance=1):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ceiling-precise-function-f366a774-527a-4c92-ba49-af0a196e66cb
    if significance == 0:
        return 0

    significance = abs(significance)
    return significance * math.ceil(number / significance)


def conditional_format_ids(*args):
    """helper function for getting conditional format ids"""
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   E09711A3-48DF-4BCB-B82C-9D8B8B22463D

    results = []
    for condition, dxf_id, stop_if_true in args:
        if condition:
            results.append(dxf_id)
            if stop_if_true:
                break
    return tuple(results)



@excel_math_func
def cos(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   COS-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.cos(value)

@excel_math_func
def cosh(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   COSH-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.cosh(value)

@excel_math_func
def cot(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   COT-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return 1 / math.tan(value)

@excel_math_func
def coth(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   COTH-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    if value == 0:
        return DIV0
    return 1 / math.tanh(value)

@excel_math_func
def counta(*args):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   COUNTA-function-7dc98846-2bb9-4dec-bd8e-4fe8721fffc3
    return len(_numerics(*args, keep_bools=True, to_number=lambda x: 1))

@excel_math_func
def countblank(*args):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   COUNTBLANK-function-5ebe6dcb-aa7f-4f38-824c-b0b0b0373bd0
    return sum(1 for x in flatten(args) if x == '')


@excel_math_func
def csc(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   CSC-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    if value == 0:
        return DIV0
    return 1 / math.sin(value)

@excel_math_func
def csch(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   CSCH-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    if value == 0:
        return DIV0
    return 1 / math.sinh(value)

@excel_math_func
def degrees(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   DEGREES-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.degrees(value)


@excel_math_func
def even(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   even-function-197b5f06-c795-4c1e-8696-3c3b8a646cf9
    return math.copysign(math.ceil(abs(value) / 2) * 2, value)


@excel_math_func
def exp_(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   EXP-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.exp(value)

@excel_math_func
def exp(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   EXP-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.exp(value)


@excel_math_func
def fact(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   fact-function-ca8588c2-15f2-41c0-8e8c-c11bd471a4f3
    return math.factorial(int(value)) if value >= 0 else NUM_ERROR


@excel_helper(cse_params=-1)
def factdouble(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   fact-function-ca8588c2-15f2-41c0-8e8c-c11bd471a4f3
    if isinstance(value, bool):
        return VALUE_ERROR
    value = coerce_to_number(value, convert_all=True)
    if isinstance(value, str):
        return VALUE_ERROR
    if value < 0:
        return NUM_ERROR

    return np.sum(np.prod(range(int(value), 0, -2), axis=0))


@excel_math_func
def floor(number, significance):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   FLOOR-function-14BB497C-24F2-4E04-B327-B0B4DE5A8886
    if significance < 0 < number:
        return NUM_ERROR

    if number == 0:
        return 0

    if significance == 0:
        return DIV0

    return significance * math.floor(number / significance)


@excel_math_func
def floor_math(number, significance=1, mode=0):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   floor-math-function-c302b599-fbdb-4177-ba19-2c2b1249a2f5
    if significance == 0:
        return 0

    significance = abs(significance)
    if mode and number < 0:
        significance = -significance
    return significance * math.floor(number / significance)


@excel_math_func
def floor_precise(number, significance=1):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   floor-precise-function-f769b468-1452-4617-8dc3-02f842a0702e
    if significance == 0:
        return 0

    significance = abs(significance)
    return significance * math.floor(number / significance)

@excel_math_func
def gcd(*args):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   gcd-function-0b325ea3-6c1f-4a9d-9b1a-8bc8fbc998e0
    args = _numerics(args, to_number=lambda x: int(x))
    if isinstance(args, str):
        return args
    return np.gcd.reduce(args)


@excel_math_func
def lcm(*args):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   lcm-function-8d8c2d80-ec6a-4c08-bf71-0bb212e8e83e
    args = _numerics(args, to_number=lambda x: int(x))
    if isinstance(args, str):
        return args
    return np.lcm.reduce(args)


@excel_math_func
def int_(value1):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   INT-function-A6C4AF9E-356D-4369-AB6A-CB1FD9D343EF
    return math.floor(value1)


@excel_math_func
def ln(arg):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   LN-function-81FE1ED7-DAC9-4ACD-BA1D-07A142C6118F
    return math.log(arg)


@excel_math_func
def log(number, base=10):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   LOG-function-4E82F196-1CA9-4747-8FB0-6C4A3ABB3280
    return math.log(number, base)

@excel_math_func
def log10(number):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   LOG10-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3
    return math.log10(number)

@excel_math_func
def log2(number):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   LOG2-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3
    return math.log2(number)

@excel_math_func
def logb(number, base=2):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   LOGB-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3
    return math.log(number, base)

@excel_math_func
def maxa(*args):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   MAXA-function-043EED9C-46A7-48D9-900C-80EDA63DB46C
    data = _numerics(*args, keep_bools=True)
    if isinstance(data, str):
        return data

    # if no non numeric cells, return zero (is what excel does)
    return max(data) if data else 0

@excel_math_func
def mina(*args):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   MINA-function-043EED9C-46A7-48D9-900C-80EDA63DB46C
    data = _numerics(*args, keep_bools=True)
    if isinstance(data, str):
        return data

    # if no non numeric cells, return zero (is what excel does)
    return min(data) if data else 0


@excel_math_func
def mod(number, divisor):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   MOD-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3
    if divisor == 0:
        return DIV0

    return number % divisor

@excel_math_func
def mround(number, multiple):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   MROUND-function-8f0b8def-1fc7-4a7d-bb18-2c1fda9bce45
    if multiple == 0:
        return DIV0

    return round(number / multiple) * multiple


@excel_helper(cse_params=None, err_str_params=-1, number_params=0)
def npv(rate, *args):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   NPV-function-8672CB67-2576-4D07-B67B-AC28ACF2A568

    rate += 1
    cashflow = [x for x in flatten(args, coerce=coerce_to_number)
                if is_number(x) and not isinstance(x, bool)]
    return sum(x * rate ** -i for i, x in enumerate(cashflow, start=1))


@excel_math_func
def odd(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   odd-function-deae64eb-e08a-4c88-8b40-6d0b42575c98
    return math.copysign(math.ceil((abs(value) - 1) / 2) * 2 + 1, value)

@excel_math_func
def pi():
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   pi-function-237349d1-0c7e-4e29-9e28-7e11d28f0fc3
    return math.pi


@excel_math_func
def pmt(rate, nper, pv, fv=0, type=None):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   pmt-function-0214da64-9a63-4996-bc20-214433fa6441

    if rate == 0:
        return -(fv + pv) / nper

    if type is None:
        type = 0

    return (pv * rate * (1 + rate) ** nper + fv) / (
        (1 + rate * type) * ((1 + rate) ** nper - 1)
    )


    
@excel_math_func
def power(number, power):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   POWER-function-D3F2908B-56F4-4C3F-895A-07FB519C362A
    if number == power == 0:
        # Really excel?  What were you thinking?
        return NA_ERROR

    try:
        return number ** power
    except ZeroDivisionError:
        return DIV0


@excel_math_func
def pv(rate, nper, pmt, fv=0, type_=0):
    #  Excel reference: https://support.microsoft.com/en-us/office/
    #   pv-function-23879d31-0e02-4321-be01-da16e8168cbd

    if rate != 0:
        val = pmt * (1 + rate * type_) * ((1 + rate) ** nper - 1) / rate
        return 1 / (1 + rate) ** nper * (-fv - val)
    else:
        return -fv - pmt * nper

@excel_math_func
def radians(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   RADIANS-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.radians(value)

@excel_math_func
def rand():
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   RAND-function-2b977a09-1a3c-4892-aeab-0a2a4645633c
    return np.random.random()

@excel_math_func
def randbetween(bottom, top):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   RANDBETWEEN-function-2a1de742-cca4-4a41-8b58-067075af9b61
    return np.random.randint(bottom, top + 1)


@excel_math_func
def round_(number, num_digits=0):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ROUND-function-c018c5d8-40fb-4053-90b1-b3e7f61a213c

    num_digits = int(num_digits)
    if num_digits >= 0:  # round to the right side of the point
        return float(Decimal(repr(number)).quantize(
            Decimal(repr(pow(10, -num_digits))),
            rounding=ROUND_HALF_UP
        ))
        # see https://docs.python.org/2/library/functions.html#round
        # and https://gist.github.com/ejamesc/cedc886c5f36e2d075c5

    else:
        return round(number, num_digits)


def _round(number, num_digits, rounding):
    num_digits = int(num_digits)
    quant = Decimal(f'1E{"+-"[num_digits >= 0]}{abs(num_digits)}')
    return float(Decimal(repr(number)).quantize(quant, rounding=rounding))


@excel_math_func
def rounddown(number, num_digits):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ROUNDDOWN-function-2EC94C73-241F-4B01-8C6F-17E6D7968F53
    return _round(number, num_digits, rounding=ROUND_DOWN)


@excel_math_func
def roundup(number, num_digits):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   ROUNDUP-function-F8BC9B23-E795-47DB-8703-DB171D0C42A7
    return _round(number, num_digits, rounding=ROUND_UP)

@excel_math_func
def sec(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   SEC-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    if value == 0:
        return DIV0
    return 1 / math.cos(value)


@excel_math_func
def sech(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   SECH-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return 1 / math.cosh(value)


@excel_math_func
def sign(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   sign-function-109c932d-fcdc-4023-91f1-2dd0e916a1d8
    return -1 if value < 0 else int(bool(value))


@excel_math_func
def signif(number, num_digits):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   SIGNIF-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3
    return _round(number, num_digits, rounding=ROUND_HALF_UP)

@excel_math_func
def sinh(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   SINH-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.sinh(value)

@excel_math_func
def sqrt(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   SQRT-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3
    if value < 0:
        return NUM_ERROR
    return math.sqrt(value)

def sum_(*args):
    data = _numerics(*args)
    if isinstance(data, str):
        return data

    # if no non numeric cells, return zero (is what excel does)
    return sum(data)


def sumif(rng, criteria, sum_range=None):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   SUMIF-function-169b8c99-c05c-4483-a712-1697a653039b

    # WARNING:
    # - The following is not currently implemented:
    #  The sum_range argument does not have to be the same size and shape as
    #  the range argument. The actual cells that are added are determined by
    #  using the upper leftmost cell in the sum_range argument as the
    #  beginning cell, and then including cells that correspond in size and
    #  shape to the range argument.

    if sum_range is None:
        sum_range = rng
    return sumifs(sum_range, rng, criteria)


def sumifs(sum_range, *args):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   SUMIFS-function-C9E748F5-7EA7-455D-9406-611CEBCE642B
    if not list_like(sum_range):
        sum_range = ((sum_range, ), )

    coords = handle_ifs(args, sum_range)

    # A returned string is an error code
    if isinstance(coords, str):
        return coords

    return sum(_numerics(
        (sum_range[r][c] for r, c in coords),
        keep_bools=True
    ))


def sumproduct(*args):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   SUMPRODUCT-function-16753E75-9F68-4874-94AC-4D2145A2FD2E

    # find any errors
    error = next((i for i in flatten(args) if i in ERROR_CODES), None)
    if error:
        return error

    # verify array sizes match
    sizes = set()
    for arg in args:
        assert is_array_arg(arg)
        sizes.add((len(arg), len(arg[0])))
    if len(sizes) != 1:
        return VALUE_ERROR

    # put the values into numpy vectors
    values = np.array(tuple(tuple(
        x if isinstance(x, (float, int)) and not isinstance(x, bool) else 0
        for x in flatten(arg)) for arg in args))

    # return the sum product
    return np.sum(np.prod(values, axis=0))

@excel_math_func
def tan(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   TAN-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.tan(value)

@excel_math_func
def tanh(value):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   TANH-function-239847d3-5b62-4e31-84c2-1f1d8256b0b8
    return math.tanh(value)

@excel_math_func
def trunc(number, num_digits=0):
    # Excel reference: https://support.microsoft.com/en-us/office/
    #   TRUNC-function-8B86A64C-3127-43DB-BA14-AA5CEB292721
    factor = 10 ** int(num_digits)
    return int(number * factor) / factor


# Older mappings for excel functions that match Python built-in and keywords
x_abs = abs_
xatan2 = atan2_
x_int = int_
x_round = round_
xsum = sum_
