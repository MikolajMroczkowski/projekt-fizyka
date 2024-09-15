import matplotlib.pyplot as plot
import io
import base64
import numpy as np


def compute(m, v, q, B):
    # m = 1.673e-27  # masa protonu w kg
    # v = 2e7        # prędkość protonu w m/s
    # q = 1.6e-19    # ładunek protonu w C
    # B = 0.2        # indukcja pola magnetycznego w T
    r = (m * v) / (q * B)
    fig, ax = plot.subplots()
    circle = plot.Circle((0, 0), r, color='black', fill=False, linestyle='dashed')
    ax.add_artist(circle)
    theta = np.linspace(0, np.pi / 2, 100)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    velocity = (0, -0.5)
    lorentz_force = (-0.5, 0)
    speed = ax.arrow(x[0], y[0], velocity[0], velocity[1], head_width=0.3, head_length=0.4, fc='blue', ec='blue')
    lorenz = ax.arrow(x[0], y[0], lorentz_force[0], -lorentz_force[1], head_width=0.3, head_length=0.4, fc='red', ec='red')
    corners = [(-r, r), (r, r), ( -r, -r), (r, -r)]
    for corner in corners:
        ax.text(corner[0], corner[1], r'$\otimes B$', fontsize=14, ha='center', va='center')
    ax.text(0, 0, r'$\otimes B$', fontsize=14, ha='center', va='center')
    ax.set_xlim(-r - 2, r + 2)
    ax.set_ylim(-r - 2, r + 2)
    ax.set_aspect('equal')
    plot.legend([speed, lorenz], ['Wektor prędkości', 'Wektor Siły Lorentza'])
    plot.title("Ruch protonu w polu magnetycznym")
    plot.tight_layout()
    buf = io.BytesIO()
    plot.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plot.close()
    return r, f'data:image/png;base64,{image_base64}'
