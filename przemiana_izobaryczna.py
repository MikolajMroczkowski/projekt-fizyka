import matplotlib.pyplot as plt
import io
import base64
import numpy as np


def calc(p, v1=None, v2=None, v=None):
    if v is None:
        vv = v2 - v1
        vv = round(vv, 6)
        return p * vv
    else:
        return p * v


def plot_uri(p, v1, v2, p_multiplier=1, v1_multiplier=1, v2_multiplier=1):
    v_names = {
        1: 'm³',
        0.001: 'dm³',
        0.000001: 'cm³'
    }
    p_names = {
        1000: 'kPa',
        100: 'hPa',
        1: 'Pa'
    }
    v1 = v1 / v1_multiplier
    v2 = v2 / v2_multiplier
    p = p / p_multiplier
    x = np.linspace(v1, v2, 100)
    y = np.full_like(x, p)
    plot = plt
    plot.plot(x, y, label=f'Ciśnienie p = {p} {p_names[p_multiplier]}')
    plot.xlabel(f'Objętość ({v_names[v1_multiplier]})')
    plot.ylabel(f'Ciśnienie ({p_names[p_multiplier]})')
    plot.legend()
    plot.grid(True)
    plot.tight_layout()
    buf = io.BytesIO()
    plot.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plot.close()
    return f'data:image/png;base64,{image_base64}'
