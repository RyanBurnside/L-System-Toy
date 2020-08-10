# Ryan Burnside
# Tkinter template for visualization
#

try:
    from tkinter import *
except ImportError:
    raise "Tkinter is not present, install it to continue"
import copy
import math
import re

root = Tk()
base_frame = Frame(root)
menu_bar = Menu(root)

# Global canvas Lines
canvas_lines = []
angle = StringVar()
angle.set(45)

def interpolate(val, val2, percent):
    return val + (val2 - val) * percent

def multiple_replace(string, rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in rep_dict.keys()]), 
                         re.M)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)

class Turtle:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = (0, 0, 0)
        self.tail_down = True
    def fd(self, length):
        old_x = self.x
        old_y = self.y
        self.x += math.cos(math.radians(self.direction)) * length
        self.y -= math.sin(math.radians(self.direction)) * length
        if(self.tail_down == True):
            canvas_lines.append(canvas.create_line(old_x, old_y, 
                                                   self.x, self.y))
    def copy(self):
        return copy.deepcopy(self)

    def rt(self, angle):
        self.direction += angle
    def lt(self, angle):
        self.direction -= angle
    def pu(self):
        self.tail_down = False
    def pd(self):
        self.tail_down = True

def find_bounding_box():
    global canvas_lines
    if(len(canvas_lines) < 1):
        print("returning")
        return

    # set some defaults
    smallest_x = canvas.coords(canvas_lines[0])[0]
    smallest_y = canvas.coords(canvas_lines[0])[1]
    biggest_x = canvas.coords(canvas_lines[0])[2]
    biggest_y = canvas.coords(canvas_lines[0])[3]

    for i in canvas_lines:
        coords = canvas.coords(i)
        x1 = coords[0]
        y1 = coords[1]
        x2 = coords[2]
        y2 = coords[3]

        if x1 < smallest_x:
            smallest_x = x1
        if x1 > biggest_x:
            biggest_x = x1

        if x2 < smallest_x:
            smallest_x = x2
        if x2 > biggest_x:
            biggest_x = x2

        if y1 < smallest_y:
            smallest_y = y1
        if y1 > biggest_y:
            biggest_y = y1

        if y2 < smallest_y:
            smallest_y = y2
        if y2 > biggest_y:
            biggest_y = y2
    return (smallest_x, smallest_y, biggest_x, biggest_y)

def fit_drawing():
    # Current limits for lines
    limits = find_bounding_box()
    smallest_x = limits[0]
    smallest_y = limits[1]
    biggest_x = limits[2]
    biggest_y = limits[3]
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    # Make drawing fit a square area
    if(canvas_width < canvas_height):
        canvas_height = canvas_width
    elif(canvas_height < canvas_width):
        canvas_width = canvas_height

    for l in canvas_lines:
        canvas_coords = canvas.coords(l)
        x1 = canvas_coords[0]
        y1 = canvas_coords[1]
        x2 = canvas_coords[2]
        y2 = canvas_coords[3]

        delta_x = biggest_x - smallest_x
        delta_y = biggest_y - smallest_y

        if delta_y == 0:
            delta_y = 1
        if delta_x == 0:
            delta_x = 1

        if delta_x > delta_y:
            delta_y = delta_x
        else:
            delta_x = delta_y

        x1_percent = 0
        y1_percent = 0
        x2_percent = 0
        y2_percent = 0

        if(delta_x != 0):
            x1_percent = (x1 - smallest_x) / delta_x
        new_x = interpolate(0, canvas_width, x1_percent)
        
        if(delta_x != 0):
            y1_percent = (y1 - smallest_y) / delta_y
        new_y = interpolate(0, canvas_height, y1_percent)
        
        if(delta_x != 0):
            x2_percent = (x2 - smallest_x) / delta_x
        new_x2 = interpolate(0, canvas_width, x2_percent)
        
        if(delta_x != 0):
            y2_percent = (y2 - smallest_y) / delta_y
        new_y2 = interpolate(0, canvas_height, y2_percent)

        canvas.coords(l, new_x, new_y, new_x2, new_y2)

def draw_string(string):
    global angle
    heap = []
    theta = float(angle.get())
    step_size = 10
    canvas.delete("all")
    del canvas_lines[:]
    t = Turtle(canvas.winfo_width() / 2, canvas.winfo_height() / 2, 90)
    #slice string into parts for the heap -> [Turtle, step_size]
    #Seed the first turtle on the heap
    heap.append([t, step_size])
    for c in string:
        current_turt = heap[-1][0]
        step_size = heap[-1][1]
        if c == '[':
            # Duplicate current turtle and add to heap
            heap.append([current_turt.copy(), step_size])
        elif c == ']':
            # Pop last turtle off heap
            heap.pop()
        elif c == 'F':
            current_turt.pd()
            current_turt.fd(step_size)
        elif c == 'f':
            current_turt.pu()
            current_turt.fd(step_size)
        elif c == "-":
            current_turt.lt(theta)
        elif c == "+":
            current_turt.rt(theta)
    fit_drawing()

def find_result():
    global start_entry
    global replace_entry
    global with_entry
    global result_entry
    new_string = start_entry.get(1.0, END).replace(
        replace_entry.get(1.0, END).strip(),
        with_entry.get(1.0, END).strip()).strip()
    result_entry.delete(1.0, END)
    result_entry.insert(1.0, new_string)
    draw_string(new_string)

def output_to_input():
    new_string = result_entry.get(1.0, END).replace(
        replace_entry.get(1.0, END).strip(),
        with_entry.get(1.0, END).strip()).strip()
    draw_string(new_string)
    result_entry.delete(1.0, END)
    result_entry.insert(1.0, new_string)
    draw_string(new_string)

def seed_preset():
    global start_entry
    global replace_entry
    global with_entry
    global result_entry
    global presets_choice
    global angle

    start_entry.delete(1.0, END)
    replace_entry.delete(1.0, END)
    with_entry.delete(1.0, END)
    result_entry.delete(1.0, END)
    if presets_choice.get() == "Levy C Curve":
        angle.set("90")
        start_entry.insert(1.0, "F")
        replace_entry.insert(1.0, "F")
        with_entry.insert(1.0, "F+F-")
    if presets_choice.get() == "Kotch Snowflake":
        angle.set("60")
        start_entry.insert(1.0, "F--F--F")
        replace_entry.insert(1.0, "F")
        with_entry.insert(1.0, "F+F--F+F")
    if presets_choice.get() == "Weed 1":
        angle.set("25.7")
        start_entry.insert(1.0, "F")
        replace_entry.insert(1.0, "F")
        with_entry.insert(1.0, "F[+F]F[-F]F")
    if presets_choice.get() == "Weed 2":
        angle.set("20")
        start_entry.insert(1.0, "F")
        replace_entry.insert(1.0, "F")
        with_entry.insert(1.0, "F[+F]F[-F][F]")
    if presets_choice.get() == "Weed 3":
        angle.set("22.5")
        start_entry.insert(1.0, "F")
        replace_entry.insert(1.0, "F")
        with_entry.insert(1.0, "FF-[-F+F+F]+[+F-F-F]")

file_menu = Menu(menu_bar, tearoff = 0)
root.config(menu=menu_bar)
file_menu.add_command(label = "Quit", command = root.quit)
menu_bar.add_cascade(label = "File", menu = file_menu)

presets_choice = StringVar(base_frame)
presets_choice.set("Kotch Snowflake")
presets_frame = Frame(base_frame, bd = 1, relief = SUNKEN)
presets_label = Label(presets_frame, text = "Presets:")
presets_button = OptionMenu(presets_frame, presets_choice,
                            "Kotch Snowflake",
                            "Levy C Curve",
                            "Weed 1",
                            "Weed 2",
                            "Weed 3")

presets_go = Button(presets_frame, text = "Set", command = seed_preset)
presets_menu = Menu(presets_button)

theta_label = Label(base_frame, text = "Angle (Degrees): ")
theta_entry = Entry(base_frame, width = 10, textvariable = angle)

start_frame = Frame(base_frame, bd = 1, relief = SUNKEN)
start_label = Label(start_frame, text = "Start String")
start_entry = Text(start_frame, width = 20, height = 5)
start_scroll = Scrollbar(start_frame)
start_entry.config(yscrollcommand = start_scroll.set)
start_scroll.config(command = start_entry.yview)

replace_frame= Frame(base_frame, bd = 1, relief = SUNKEN)
replace_label = Label(replace_frame, text = "Replace Term")
replace_entry = Text(replace_frame, width = 20, height = 5)
replace_scroll = Scrollbar(replace_frame)
replace_entry.config(yscrollcommand = replace_scroll.set)
replace_scroll.config(command = replace_entry.yview)

with_frame= Frame(base_frame, bd = 1, relief = SUNKEN)
with_label = Label(with_frame, text = "With Term")
with_entry = Text(with_frame, width = 20, height = 5)
with_scroll = Scrollbar(with_frame)
with_entry.config(yscrollcommand = with_scroll.set)
with_scroll.config(command = with_entry.yview)

result_frame= Frame(base_frame, bd = 1, relief = SUNKEN)
result_label = Label(result_frame, text = "Result")
result_entry = Text(result_frame, width = 20, height = 5)
result_scroll = Scrollbar(result_frame)
result_entry.config(yscrollcommand = result_scroll.set)
result_scroll.config(command = result_entry.yview)

buttons_frame = Frame(base_frame)
eval_button = Button(buttons_frame, text = "Evaluate", command = find_result)
iterate_button = Button(buttons_frame, text = "Iterate", 
                        command = output_to_input)
canvas = Canvas(base_frame, width = 640, height = 640, bg = "WHITE")
canvas.config(scrollregion = canvas.bbox(ALL))
base_frame.grid(column = 0, row = 0, sticky = (N, W, E, S))
start_frame.grid(column = 0, row = 1)

presets_frame.grid(column = 0, row = 0, sticky = (S, W))
presets_label.grid(column = 0, row = 0, sticky = (S, W))
presets_button.grid(column = 0, row = 1, sticky = (S, W))
presets_go.grid(column = 1, row = 1, sticky = (S, W))

theta_label.grid(column = 0, row = 1, sticky = (S, W))
theta_entry.grid(column = 0, row = 2, sticky = (N, W))

start_frame.grid(column = 0, row = 3, sticky = (S, W))
start_label.grid(column = 0, row = 0, sticky = (S, W))
start_entry.grid(column = 0, row = 1, sticky = (N, W))
start_scroll.grid(column = 1, row = 1, rowspan = 2,  sticky = (N, E, S))

replace_frame.grid(column = 0, row = 4, sticky = (S, W))
replace_label.grid(column = 0, row = 0, sticky = (S, W))
replace_entry.grid(column = 0, row = 1, sticky = (N, W))
replace_scroll.grid(column = 1, row = 1, rowspan = 2,  sticky = (N, E, S))

with_frame.grid(column = 0, row = 5, sticky = (S, W))
with_label.grid(column = 0, row = 0, sticky = (S, W))
with_entry.grid(column = 0, row = 1, sticky = (N, W))
with_scroll.grid(column = 1, row = 1, rowspan = 2,  sticky = (N, E, S))

result_frame.grid(column = 0, row = 6, sticky = (S, W))
result_label.grid(column = 0, row = 0, sticky = (S, W))
result_entry.grid(column = 0, row = 1, sticky = (N, W))
result_scroll.grid(column = 1, row = 1, rowspan = 2,  sticky = (N, E, S))

buttons_frame.grid(column = 0, row = 7, sticky = (N, W))
eval_button.grid(column = 0, row = 0, sticky = (N, W))
iterate_button.grid(column = 1, row = 0, sticky = (N, W))

canvas.grid(column = 1, row = 0, rowspan = 8,  sticky = (N, S, W, E))
root.title("Simple Lindenmayer Grammar Test")

root.mainloop()
