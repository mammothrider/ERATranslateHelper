__all__ = ['pyjsTranslated']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['e', 'n'])
@Js
def PyJsHoisted_n_(r, o, this, arguments, var=var):
    var = Scope({'r':r, 'o':o, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'o', 'r', 't'])
    #for JS loop
    var.put('t', Js(0.0))
    while (var.get('t')<(var.get('o').get('length')-Js(2.0))):
        try:
            var.put('a', var.get('o').callprop('charAt', (var.get('t')+Js(2.0))))
            def PyJs_LONG_0_(var=var):
                return PyJsComma(PyJsComma(var.put('a', ((var.get('a').callprop('charCodeAt', Js(0.0))-Js(87.0)) if (var.get('a')>=Js('a')) else var.get('Number')(var.get('a')))),var.put('a', (PyJsBshift(var.get('r'),var.get('a')) if PyJsStrictEq(Js('+'),var.get('o').callprop('charAt', (var.get('t')+Js(1.0)))) else (var.get('r')<<var.get('a'))))),var.put('r', (((var.get('r')+var.get('a'))&Js(4294967295.0)) if PyJsStrictEq(Js('+'),var.get('o').callprop('charAt', var.get('t'))) else (var.get('r')^var.get('a')))))
            PyJs_LONG_0_()
        finally:
                var.put('t', Js(3.0), '+')
    return var.get('r')
PyJsHoisted_n_.func_name = 'n'
var.put('n', PyJsHoisted_n_)
@Js
def PyJsHoisted_e_(r, windowl, this, arguments, var=var):
    var = Scope({'r':r, 'windowl':windowl, 'this':this, 'arguments':arguments}, var)
    var.registers(['m', 'h', 'v', 'g', 'f', 'i', 'A', 'r', 'u', 'o', 'd', 'windowl', 'p', 't', 'D', 'C', 'c', 'b', 'S', 'F', 's', 'e'])
    var.put('o', var.get('r').callprop('match', JsRegExp('/[\\uD800-\\uDBFF][\\uDC00-\\uDFFF]/g')))
    if PyJsStrictEq(var.get(u"null"),var.get('o')):
        var.put('t', var.get('r').get('length'))
        ((var.get('t')>Js(30.0)) and var.put('r', (((Js('')+var.get('r').callprop('substr', Js(0.0), Js(10.0)))+var.get('r').callprop('substr', (var.get('Math').callprop('floor', (var.get('t')/Js(2.0)))-Js(5.0)), Js(10.0)))+var.get('r').callprop('substr', (-Js(10.0)), Js(10.0)))))
    else:
        #for JS loop
        var.put('e', var.get('r').callprop('split', JsRegExp('/[\\uD800-\\uDBFF][\\uDC00-\\uDFFF]/')))
        var.put('C', Js(0.0))
        var.put('h', var.get('e').get('length'))
        var.put('f', Js([]))
        while (var.get('h')>var.get('C')):
            try:
                PyJsComma((PyJsStrictNeq(Js(''),var.get('e').get(var.get('C'))) and var.get('f').get('push').callprop('apply', var.get('f'), var.get('a')(var.get('e').get(var.get('C')).callprop('split', Js(''))))),(PyJsStrictNeq(var.get('C'),(var.get('h')-Js(1.0))) and var.get('f').callprop('push', var.get('o').get(var.get('C')))))
            finally:
                    (var.put('C',Js(var.get('C').to_number())+Js(1))-Js(1))
        var.put('g', var.get('f').get('length'))
        ((var.get('g')>Js(30.0)) and var.put('r', ((var.get('f').callprop('slice', Js(0.0), Js(10.0)).callprop('join', Js(''))+var.get('f').callprop('slice', (var.get('Math').callprop('floor', (var.get('g')/Js(2.0)))-Js(5.0)), (var.get('Math').callprop('floor', (var.get('g')/Js(2.0)))+Js(5.0))).callprop('join', Js('')))+var.get('f').callprop('slice', (-Js(10.0))).callprop('join', Js('')))))
    var.put('u', PyJsComma(Js(0.0), Js(None)))
    var.put('i', var.get(u"null"))
    var.put('u', (var.get('i') if PyJsStrictNeq(var.get(u"null"),var.get('i')) else (var.put('i', (var.get('windowl') or Js(''))) or Js(''))))
    #for JS loop
    var.put('d', var.get('u').callprop('split', Js('.')))
    var.put('m', (var.get('Number')(var.get('d').get('0')) or Js(0.0)))
    var.put('s', (var.get('Number')(var.get('d').get('1')) or Js(0.0)))
    var.put('S', Js([]))
    var.put('c', Js(0.0))
    var.put('v', Js(0.0))
    while (var.get('v')<var.get('r').get('length')):
        try:
            var.put('A', var.get('r').callprop('charCodeAt', var.get('v')))
            def PyJs_LONG_3_(var=var):
                def PyJs_LONG_2_(var=var):
                    def PyJs_LONG_1_(var=var):
                        return PyJsComma(PyJsComma(var.put('A', ((Js(65536.0)+((Js(1023.0)&var.get('A'))<<Js(10.0)))+(Js(1023.0)&var.get('r').callprop('charCodeAt', var.put('v',Js(var.get('v').to_number())+Js(1)))))),var.get('S').put((var.put('c',Js(var.get('c').to_number())+Js(1))-Js(1)), ((var.get('A')>>Js(18.0))|Js(240.0)))),var.get('S').put((var.put('c',Js(var.get('c').to_number())+Js(1))-Js(1)), (((var.get('A')>>Js(12.0))&Js(63.0))|Js(128.0))))
                    return PyJsComma((PyJs_LONG_1_() if ((PyJsStrictEq(Js(55296.0),(Js(64512.0)&var.get('A'))) and ((var.get('v')+Js(1.0))<var.get('r').get('length'))) and PyJsStrictEq(Js(56320.0),(Js(64512.0)&var.get('r').callprop('charCodeAt', (var.get('v')+Js(1.0)))))) else var.get('S').put((var.put('c',Js(var.get('c').to_number())+Js(1))-Js(1)), ((var.get('A')>>Js(12.0))|Js(224.0)))),var.get('S').put((var.put('c',Js(var.get('c').to_number())+Js(1))-Js(1)), (((var.get('A')>>Js(6.0))&Js(63.0))|Js(128.0))))
                return (var.get('S').put((var.put('c',Js(var.get('c').to_number())+Js(1))-Js(1)), var.get('A')) if (Js(128.0)>var.get('A')) else PyJsComma((var.get('S').put((var.put('c',Js(var.get('c').to_number())+Js(1))-Js(1)), ((var.get('A')>>Js(6.0))|Js(192.0))) if (Js(2048.0)>var.get('A')) else PyJs_LONG_2_()),var.get('S').put((var.put('c',Js(var.get('c').to_number())+Js(1))-Js(1)), ((Js(63.0)&var.get('A'))|Js(128.0)))))
            PyJs_LONG_3_()
        finally:
                (var.put('v',Js(var.get('v').to_number())+Js(1))-Js(1))
    #for JS loop
    var.put('p', var.get('m'))
    var.put('F', ((((Js('')+var.get('String').callprop('fromCharCode', Js(43.0)))+var.get('String').callprop('fromCharCode', Js(45.0)))+var.get('String').callprop('fromCharCode', Js(97.0)))+(((Js('')+var.get('String').callprop('fromCharCode', Js(94.0)))+var.get('String').callprop('fromCharCode', Js(43.0)))+var.get('String').callprop('fromCharCode', Js(54.0)))))
    def PyJs_LONG_4_(var=var):
        return (((((Js('')+var.get('String').callprop('fromCharCode', Js(43.0)))+var.get('String').callprop('fromCharCode', Js(45.0)))+var.get('String').callprop('fromCharCode', Js(51.0)))+(((Js('')+var.get('String').callprop('fromCharCode', Js(94.0)))+var.get('String').callprop('fromCharCode', Js(43.0)))+var.get('String').callprop('fromCharCode', Js(98.0))))+(((Js('')+var.get('String').callprop('fromCharCode', Js(43.0)))+var.get('String').callprop('fromCharCode', Js(45.0)))+var.get('String').callprop('fromCharCode', Js(102.0))))
    var.put('D', PyJs_LONG_4_())
    var.put('b', Js(0.0))
    while (var.get('b')<var.get('S').get('length')):
        try:
            PyJsComma(var.put('p', var.get('S').get(var.get('b')), '+'),var.put('p', var.get('n')(var.get('p'), var.get('F'))))
        finally:
                (var.put('b',Js(var.get('b').to_number())+Js(1))-Js(1))
    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('p', var.get('n')(var.get('p'), var.get('D'))),var.put('p', var.get('s'), '^')),((Js(0.0)>var.get('p')) and var.put('p', ((Js(2147483647.0)&var.get('p'))+Js(2147483648.0))))),var.put('p', Js(1000000.0), '%')),((var.get('p').callprop('toString')+Js('.'))+(var.get('p')^var.get('m'))))
PyJsHoisted_e_.func_name = 'e'
var.put('e', PyJsHoisted_e_)
pass
pass
pass


# Add lib to the module scope
pyjsTranslated = var.to_python()