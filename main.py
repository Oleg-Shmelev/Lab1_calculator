# Шмелев Олег, группа 6372, вариант 58

import math
import re


def check_brackets(s):
    depth = 0
    for i, ch in enumerate(s):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                print('Error')
                return False
    if depth > 0:
        print('Error')
        return False
    return True


def fmt(x):
    if isinstance(x, int):
        return str(x)
    if x.is_integer():
        return str(int(x))
    r = repr(x)
    if 'e' in r:
        r = format(x, '.20f').rstrip('0')
    return r


def calc(s):
    s = s.strip()

    try:
        return float(s)
    except ValueError:
        pass

    if "(" in s:
        io = s.rfind('(')
        ic = s.find(')', io)
        inner = s[io + 1:ic]
        val = calc(inner)
        if isinstance(val, str):
            return val

        head = s[:io].rstrip()
        if head.endswith("fact"):
            if not val.is_integer() or val < 0 or val > 170:
                return 'Error'
            res = math.factorial(int(val))
            return calc(head[:-4] + fmt(res) + s[ic + 1:])

        return calc(s[:io] + fmt(val) + s[ic + 1:])

    m = re.search(r"(-?\d+\.?\d*)\s*([*/])\s*(-?\d+\.?\d*)", s)
    if m:
        l = float(m.group(1))
        op = m.group(2)
        r = float(m.group(3))
        if op == '/' and r == 0:
            return 'Error'
        res = l * r if op == '*' else l / r
        return calc(s[:m.start()] + fmt(res) + s[m.end():])

    m = re.search(r"(-?\d+\.?\d*)\s*([+\-])\s*(-?\d+\.?\d*)", s)
    if m:
        l = float(m.group(1))
        op = m.group(2)
        r = float(m.group(3))
        res = l - r if op == '-' else l + r
        return calc(s[:m.start()] + fmt(res) + s[m.end():])

    m = re.search(r"(-?\d+\.?\d*)\s*&\s*(-?\d+\.?\d*)", s)
    if m:
        l = float(m.group(1))
        r = float(m.group(2))
        if not (l.is_integer() and r.is_integer()):
            return 'Error'
        res = int(l) & int(r)
        return calc(s[:m.start()] + fmt(res) + s[m.end():])

    return 'Error'


print('Введите выражение для посчета, например: "2 + 3 & fact(4 - 1) / 2 * (1 - 5)")')
s = str(input())
if check_brackets(s):
    print('Ответ: ', calc(s))
