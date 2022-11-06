import tkinter as tk
from src.classes import *

WINDOW_MARGIN = 20
IS_RESET =  IS_RUNNING = False

MESSAGES = dict(
	WATER_AREA="Fraction of the camp ground that is water",
	AGE_DELTA="How much to advance age each tick",
	FOOD_REPLENISH="Frequency of mosquito food refresh [years]",
	FOOD_PER_TICK="Food consumed per tick",
	BABIES_PER_DRAGONFLY_PREGNANT="Babies per Dragonfly birth",
	BABIES_PER_MOSQUITO_PREGNANT="Babies per Mosquito birth",
	LIFESPAN_DRAGONFLY="Lifespan of Dragonfly",
	LIFESPAN_MOSQUITO="Lifespan of Mosquito",
	RADIUS_MOSQUITO="Radius of mosquito food search",
	RADIUS_DRAGONFLY="Radius of dragonfly food search",
	TICK_DELTA="Delta of every tick in ms",
)

def reposition(element, x, y):
	element.place(x=x)
	element.place(y=y)


def reset():
	global IS_RESET
	global IS_RUNNING
	IS_RESET = True
	IS_RUNNING = False
	reposition(WINDOW, -1024, -1024)


def run_simulation():
	global IS_RESET
	global IS_RUNNING
	if IS_RUNNING:
		print('Already running')
		return
	IS_RUNNING = True

	def step():
		if IS_RESET:
			WINDOW.delete("all")
			WINDOW.config(background='grey')
			INFO_MOSQUITO.config(text="Mosquitos:   ")
			INFO_DRAGONFLY.config(text="Dragonflys: ")
			return

		model.step()
		if model.count == 0:
			return
		INFO_MOSQUITO.config(text="Mosquitos:   "+str(model.Mosquito_count))
		INFO_DRAGONFLY.config(text="Dragonflys: "+str(model.Dragonfly_count))
		window.after(int(TICK_DELTA), step)

	for s in OPTS.children.values():
		name = s.name
		val = s.get()
		globals()[name] = val

	reposition(WINDOW, WINDOW_MARGIN, WINDOW_MARGIN+100)
	OPTS.lower()
	IS_RESET = False
	model = Mosquito_model(int(MOSQUITO_ENTRY.get()), int(DRAGONFLY_ENTRY.get()), 80, 80, WINDOW)
	window.after(0, step)


window = tk.Tk()
window.title("Mosquito Model")
window.geometry('1024x1024')
INFO_MOSQUITO = tk.Label(window, text="Mosquitos:", justify='left')
reposition(INFO_MOSQUITO, WINDOW_MARGIN, WINDOW_MARGIN)

MOSQUITO_ENTRY = tk.Entry(window, width=25)
reposition(MOSQUITO_ENTRY, WINDOW_MARGIN+130, 5)

INFO_DRAGONFLY = tk.Label(window, text="Dragonflys:", justify='left')
reposition(INFO_DRAGONFLY, WINDOW_MARGIN, WINDOW_MARGIN+45)

DRAGONFLY_ENTRY = tk.Entry(window, width=25)
reposition(DRAGONFLY_ENTRY, WINDOW_MARGIN+130, WINDOW_MARGIN+20)

RESET_BUTTON = tk.Button(window, text="Reset", command=reset, width=10)
reposition(RESET_BUTTON, 450, WINDOW_MARGIN+40)

GO_BUTTON = tk.Button(window, text="Go", command=run_simulation, width=10)
reposition(GO_BUTTON, 450, WINDOW_MARGIN)

WINDOW = tk.Canvas(window, width=830, height=830)
reposition(WINDOW, WINDOW_MARGIN, WINDOW_MARGIN+100)

OPTS = tk.Frame(width=400, height=800)
reposition(OPTS, WINDOW_MARGIN, WINDOW_MARGIN+100)

y_axis = 0

for n, desc in sorted(MESSAGES.items()):
	v = globals()[n]
	high = v*5
	resolution = high/100
	SLIDER = tk.Scale(OPTS, from_=0, to=high, orient='horizontal', length=300,
					  label=desc, resolution=resolution, width=20)
	SLIDER.set(v)
	SLIDER.name = n
	reposition(SLIDER, 0, y_axis)
	y_axis += 60

window.update()
WIDTH = WINDOW.winfo_x() + WINDOW.winfo_width() + WINDOW_MARGIN
HEIGHT = WINDOW.winfo_y() + WINDOW.winfo_height() + WINDOW_MARGIN
window.geometry(str(WIDTH)+'x'+str(HEIGHT))

reset()
window.mainloop()