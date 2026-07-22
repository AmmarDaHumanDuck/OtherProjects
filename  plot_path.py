import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math
import subprocess

state_swap_time = 5.0
steer_angle = math.radians(20)
speed = 4.0
wheelbase = 1.54
dt = 0.032
states = ((0, speed), (steer_angle, speed), (-steer_angle, speed), (0, 0))
state_colors = ['royalblue', 'orange', 'green', 'red']

x, z, heading = 0.0, 0.0, 0.0
path_x, path_z = [x], [z]
colors = []

t = 0.0
while t < 20.0:
    state = int(t / state_swap_time) % 4
    steer, spd = states[state]
    if abs(steer) > 1e-6:
        turning_radius = wheelbase / math.tan(steer)
        dheading = spd / turning_radius * dt
    else:
        dheading = 0.0
    heading += dheading
    x += spd * math.cos(heading) * dt
    z += spd * math.sin(heading) * dt
    path_x.append(x)
    path_z.append(z)
    colors.append(state_colors[state])
    t += dt

fig, ax = plt.subplots(figsize=(9, 9))
for i in range(len(path_x) - 1):
    ax.plot(path_x[i:i+2], path_z[i:i+2], color=colors[i], linewidth=2)

legend = [
    Line2D([0],[0], color='royalblue', lw=2, label='State 0: Straight'),
    Line2D([0],[0], color='orange',    lw=2, label='State 1: Right turn'),
    Line2D([0],[0], color='green',     lw=2, label='State 2: Left turn'),
    Line2D([0],[0], color='red',       lw=2, label='State 3: Stopped'),
]
ax.legend(handles=legend, fontsize=11)
ax.plot(path_x[0], path_z[0], 'go', markersize=12)
ax.plot(path_x[-1], path_z[-1], 'rs', markersize=12)
ax.set_xlabel("X (m)")
ax.set_ylabel("Z (m)")
ax.set_title("Demo Controller Path — One Full Cycle (20s)")
ax.axis("equal")
ax.grid(True)
plt.tight_layout()
import re

# Parse cone positions from the world file
wbt_path = '/Users/ammarrizwan/Downloads/webots_fsai-master-2/worlds/simple_trackdrive_2025_Ammar_test.wbt'
cone_x, cone_y = [], []

with open(wbt_path, 'r') as f:
    for line in f:
        m = re.match(r'\s*hidden translation_\d+ ([-\d.e+]+) ([-\d.e+]+)', line)
        if m:
            cone_x.append(float(m.group(1)))
            cone_y.append(float(m.group(2)))

ax.scatter(cone_x, cone_y, color='yellow', edgecolors='black', 
           s=40, zorder=6, label='Cones')
plt.savefig('/Users/ammarrizwan/Documents/path_plot.png', dpi=150)
print("Saved!")
subprocess.run(['open', '/Users/ammarrizwan/Documents/path_plot.png'])