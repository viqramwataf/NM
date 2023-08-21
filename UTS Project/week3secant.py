import sys
import math
from tabulate import tabulate

result_list = [
    ["i", "xi-1", "xi", "f(xi-1)", "f(xi)", "xi+1", "f(xi+1)", "\u03B5 a"]]
result_type = ""
root_approx = None


def epss(n):
    return 0.5 * 10 ** (2 - n)


def function(x):
    # return x ** 3 + 5 * (x ** 2) - 10
    return math.exp(-x)-x
    # return (x**3)-x

# def functiondev(x):
#     # return (-math.exp(-x))-1
#     return (3*(x**2))-1


# print(function(6))
# print(functiondev(3))
# print(function(-100))
# print(functiondev(-100))
# print(function(2))

def esparesult(xb, xlnew):
    return abs((xb - xlnew) / xb * 100)


def xbresult(xl, xb, fxl, fxb):
    return xb-((fxb*(xl-xb)/(fxl-fxb)))


def secantespa(xl, xb, min_espa):
    counter = 1
    current_espa = 1
    global result_type
    result_type = f"Secant using \u03B5 a, x0 = {xl}, x1 = {xb}, minimum \u03B5 a = {min_espa}" + result_type
    while ((current_espa > min_espa) & (xl != xb)):
        # print(f'Iterasi ke-{counter}')
        xlnew = xb
        xb = xbresult(xl, xb, function(xl), function(xb))
        current_espa = esparesult(xb, xlnew)
        result_list.append([counter, xl, xlnew, function(
            xl), function(xlnew), xb, function(xb), current_espa])
        # print(f'x{counter-1}={xl}, x{counter}={xlnew}, f(x{counter-1})= {function(xl)}, f(x{counter})={function(xlnew)}, \nx{counter+1}={xb}, abs(esp a)= {current_espa}\n\n')
        xl = xlnew
        counter += 1
    return xb


def secantfx(xl, xb, res_fx):
    counter = 1
    current_espa = 1
    global result_type
    result_type = f"Secant using f(x), x0 = {xl}, x1 = {xb}, f(x) = {res_fx}"
    while ((abs(function(xb)) >= res_fx) & (xl != xb)):
        # print(f'Iterasi ke-{counter}')
        xlnew = xb
        xb = xbresult(xl, xb, function(xl), function(xb))
        current_espa = esparesult(xb, xlnew)
        result_list.append([counter, xl, xlnew, function(
            xl), function(xlnew), xb, function(xb), current_espa])
        # print(f'x{counter-1}={xl}, x{counter}={xlnew}, f(x{counter-1})= {function(xl)}, f(x{counter})={function(xlnew)}, \nx{counter+1}={xb}, abs(esp a)= {current_espa}\n\n')
        xl = xlnew
        counter += 1
    return xb


def secantmaxiter(xl, xb, max_iter):
    counter = 1
    current_espa = 1
    global result_type
    result_type = f"Secant using maximum iterations, x0 = {xl}, x1 = {xb}, maximum iterations = {max_iter}"
    while ((counter <= max_iter) & (xl != xb)):
        # print(f'Iterasi ke-{counter}')
        xlnew = xb
        xb = xbresult(xl, xb, function(xl), function(xb))
        current_espa = esparesult(xb, xlnew)
        result_list.append([counter, xl, xlnew, function(
            xl), function(xlnew), xb, function(xb), current_espa])
        # print(f'x{counter-1}={xl}, x{counter}={xlnew}, f(x{counter-1})= {function(xl)}, f(x{counter})={function(xlnew)}, \nx{counter+1}={xb}, abs(esp a)= {current_espa}\n\n')
        xl = xlnew
        counter += 1
    return xb


def secant(xl, xb, sig_digits=None, res_fx=None, max_iter=None):
    stop_criterias = [sig_digits, res_fx, max_iter]
    can_continue = False
    global root_approx
    if (stop_criterias.count(None) == len(stop_criterias)-1):
        can_continue = True
    if (can_continue == False):
        sys.exit(
            "Error: You must choose only one, either you set min_espa, res_fx, or max_iter")
    if (sig_digits != None):
        print("Just a reminder: you must put sig_digits as an integer, or else (float, double, etc) it'll floored")
        if (int(sig_digits) <= 0):
            sys.exit("Error: sig_digits must be an integer, and sig_digits >= 1")
        min_espa = 0.5*(10**(2-int(sig_digits)))
        print(f"\u03B5 a = {min_espa}")
        root_approx = secantespa(xl, xb, min_espa)
    elif (res_fx != None):
        if (res_fx < 0 or res_fx > 1):
            sys.exit("Error: You must set res_fx so that \"0 <= res_fx <= 1\"")
        root_approx = secantfx(xl, xb, res_fx)
    elif (max_iter != None):
        root_approx = secantmaxiter(xl, xb, max_iter)


try:
    xl = float(input("Enter x0: "))
    xb = float(input("Enter x1: "))
    if (xl == xb or xl > xb):
        sys.exit(
            "Error: x0 and x1 cannot be the same value and x0 must be smaller than x1 (x0 < x1) !")
    print("Choose stop criteria: \n\t(1) Significant digits\n\t(2) f(x) value\n\t(3) Maximum iterations")
    choose = input("Selected: ").lower()
    if ((choose == "1") or (choose == "(1)") or (choose == "significant digits")):
        sig_digits = int(input("Enter sigificant digits (Required):") or None)
        result_type = f", significant digits = {sig_digits}"
        secant(xl, xb, sig_digits=sig_digits)
    elif ((choose == "2") or (choose == "(2)") or (choose == "f(x) value")):
        res_fx = float(input("Enter f(x) value (Required):") or None)
        secant(xl, xb, res_fx=res_fx)
    elif ((choose == "3") or (choose == "(3)") or (choose == "maximum iterations")):
        max_iter = int(input("Enter maximum iterations (Required):") or None)
        secant(xl, xb, max_iter=max_iter)
    else:
        sys.exit(
            "Error: I have no idea which stop criteria you choose, try typing for example: 1, (1), or significant digits")
    dec_places = int(input("Enter decimal places: "))
except ValueError:
    sys.exit("Error: Need numbers!")

tab_result = tabulate(result_list, headers="firstrow",
                      tablefmt="fancy_grid", floatfmt=f".{dec_places}f")
# print(tab_result)

txtfile = open("/home/ken/Programming/Numerical Method/resultsecant.txt", "w")
if (root_approx == 1):
    txtfile.write(
        f"{result_type}\n\n{tab_result}\n\nTrivial answer, x = {round(root_approx,dec_places)} (based on the last xi+1)")
else:
    txtfile.write(
        f"{result_type}\n\n{tab_result}\n\nNon-trivial answer, x = {round(root_approx,dec_places)} (based on the last xi+1)")
txtfile.close()
