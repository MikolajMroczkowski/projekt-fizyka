import schemdraw
import schemdraw.elements as elm
import io
import base64


def schema_uri(e1=None, r1=None, e2=None, r2=None, R1=None, R2=None, A=None, V=None):
    print(e1, r1, e2, r2, R1, R2, A, V)
    with schemdraw.Drawing() as d:
        if A is not None:
            elm.MeterA().right().at((0, 0)).label(f'{A}A')
        else:
            elm.MeterA().right().at((0, 0))
        if e2 is not None:
            elm.BatteryCell().left(length=1).label('E2').at((5, 0))
        else:
            elm.BatteryCell().left(length=1).label('E2').at((5, 0))
        elm.Line().left().length(2)
        if r2 is not None:
            elm.Resistor().right().label(f'r2 ({r2} Ω)').at((5, 0))
        else:
            elm.Resistor().right().label('r2').at((5, 0))
        if R2 is not None:
            elm.Resistor().down().label(f'R2 ({R2} Ω)')
        else:
            elm.Resistor().down().label('R2')
        elm.Line().left(length=4)
        if R1 is not None:
            elm.Resistor().left(length=0.25).label(f'R1 ({R1} Ω)')
        else:
            elm.Resistor().left(length=0.25).label('R1')
        if e1 is not None:
            elm.BatteryCell().left().label(f'E1 ({e1} V)')
        else:
            elm.BatteryCell().left().label('E1')
        if r1 is not None:
            elm.Resistor().up().label(f'r1 ({r1} Ω)', loc='bot')
        else:
            elm.Resistor().up().label('r1')
        elm.Dot().right().at((0, -0.5))
        elm.Line().right().length(2).at((-2, -0.5))
        elm.Line().down().at((-2, -0.5)).length(0.5)
        if V is not None:
            elm.MeterV().down(length=0.75).at((-2, -1)).label(f'{V}V')
        else:
            elm.MeterV().down(length=0.75).at((-2, -1))
        elm.Line().down().at((-2, -2)).length(0.5)
        elm.Line().right().length(2).at((-2, -2.5))
        elm.Dot().right().at((0, -2.5))
        buf = io.BytesIO(d.get_imagedata('png'))
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        return f'data:image/png;base64,{image_base64}'


def calculate(e1, r1, e2, r2, R1, R2):
    I = (e1 - e2) / (r1 + R1 + r2 + R2)
    V = I * R1
    return I, V
