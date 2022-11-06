import numpy as np

WATER_AREA, FEEDING_AREA = 0.4, 0.7
AGE_DELTA = 0.005
FOOD_REPLENISH = 2
BABIES_PER_DRAGONFLY_PREGNANT, BABIES_PER_MOSQUITO_PREGNANT = 30, 30
LIFESPAN_DRAGONFLY, LIFESPAN_MOSQUITO = 17, 9
RADIUS_MOSQUITO, RADIUS_DRAGONFLY = 2, 9
FOOD_PER_TICK = .3
TICK_DELTA = 10
WINDOW_MARGIN = 20

def perturb_dist(center):
	mu, sigma = 0, 0.3
	perturbation = np.random.normal(mu, sigma, 1)[0] + 1
	return perturbation * center

def get_cell_bounds(pos, size=8):
	x_1 = pos[0]*10 + WINDOW_MARGIN - 5
	y_1 = pos[1]*10 + WINDOW_MARGIN - 5
	x_2, y_2 = x_1 + size, y_1 + size
	return (x_1, y_1, x_2, y_2)

def move_to_target(x_1, y_1, x_2, y_2, distance):
	d_y = y_2 - y_1
	d_x = x_2 - x_1

	if d_y:
		ratio = d_x / d_y

		d_y = np.sqrt(np.power(distance, 2) / (np.power(ratio, 2) + 1)) * (-1 if d_y < 0 else 1)
		d_x = abs(ratio * d_y) * (-1 if d_x < 0 else 1)
	else:
		d_y = 0
		d_x = distance * (-1 if d_x < 0 else 1)

	if abs(d_x) > abs(x_2 - x_1) or abs(d_y) > abs(y_2 - y_1):
		return (x_2, y_2)
    
	return (x_1+d_x, y_1+d_y)

def cartesian(arrays):
    n = 1
    for x in arrays:
        n *= x.size
    out = np.zeros((n, len(arrays)))


    for i in range(len(arrays)):
        m = int(n / arrays[i].size)
        out[:n, i] = np.repeat(arrays[i], m)
        n //= arrays[i].size

    n = arrays[-1].size
    for k in range(len(arrays)-2, -1, -1):
        n *= arrays[k].size
        m = int(n / arrays[k].size)
        for j in range(1, arrays[k].size):
            out[j*m:(j+1)*m,k+1:] = out[0:m,k+1:]
    return out	