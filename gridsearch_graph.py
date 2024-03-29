import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def interpolate_color(min_value, max_value, min_color, max_color, value):
    norm = mcolors.Normalize(vmin=min_value, vmax=max_value)
    cmap = mcolors.LinearSegmentedColormap.from_list('custom', [min_color, max_color])
    rgba_color = cmap(norm(value))
    hex_color = mcolors.to_hex(rgba_color)
    return hex_color

min_color = 'red'
max_color = 'lime'

datas = [
    [
        [5, 4.00, 8.00, 12.00, 16.00],
        [2.00, 388032, 393128, 388228, 425684],
        [4.00, 395568, 439116, 423192, 413628],
        [6.00, np.nan, 444188, 408700, 393384],
        [8.00, np.nan, 451060, 427936, 407020],
        [10.00, np.nan, np.nan, 425112, 440580],
    ],
    [
        [10, 4.00, 8.00, 12.00, 16.00],
        [2.00, 405504, 399728, 398488, 386600],
        [4.00, 402112, 418724, 428208, 358528],
        [6.00, np.nan, 415104, 389588, 393596],
        [8.00, np.nan, 423776, 425428, 392284],
        [10.00, np.nan, np.nan, 392136, 408148],
    ],
    [
        [15, 4.00, 8.00, 12.00, 16.00],
        [2.00, 394360, 409068, 374780, 393148],
        [4.00, 391944, 396824, 383852, 434060],
        [6.00, np.nan, 426788, 429136, 391332],
        [8.00, np.nan, 403240, 385240, 405884],
        [10.00, np.nan, np.nan, 422876, 393156],
    ],
]

mapping = {}
# Iterate through the table and create the mapping
for data in datas:
    for row in range(1, len(data)):
        for col in range(1, len(data[row])):
            if not np.isnan(data[row][col]):
                key = (
                    int(data[0][col]),
                    data[0][0],
                    int(data[row][0]),
                )
                value = data[row][col]
                mapping[key] = value
                
max_val = max(mapping.values())
min_val = min(mapping.values())

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

sol_options = [4, 8, 12, 16]
gen_options = [5, 10, 15]
par_options = [2, 4, 6, 8, 10]

# Plot points
for s in sol_options:
    for g in gen_options:
        for p in par_options:
            if p > s:
                ax.scatter(s, g, p, c="r", marker="x")
                continue
            value = mapping[(s, g, p)]
            result_color = interpolate_color(min_val, max_val, min_color, max_color, value)
            ax.scatter(s, g, p, c=result_color, marker="o")

# Define the range for the planes
range_min = min(min(sol_options), min(gen_options), min(par_options))
range_max = max(max(sol_options), max(gen_options), max(par_options))
range_points = np.linspace(range_min, range_max, 100)

# Plane: x=y
X, Y = np.meshgrid(range_points, range_points)
Z = X
ax.plot_surface(X, Y, Z, alpha=0.3, color="blue")


ax.set_xlabel("Solutions")
ax.set_ylabel("Generations")
ax.set_zlabel("Parents")
plt.show()
