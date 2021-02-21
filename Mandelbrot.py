from PIL import Image

def unoptimized_plot_set(size, max_iteration):
    iterations = []
    for pixel_x in range(size[0]):
        iterations.append([])
        for pixel_y in range(size[1]):
            x0 = scale_x(pixel_x, size[0])
            y0 = scale_y(pixel_y, size[1])
            x = 0.0
            y = 0.0
            iteration = 0
            while (x*x + y*y <= 4 and iteration < max_iteration):
                xtemp = x*x - y*y + x0
                y = 2*x*y + y0
                x = xtemp
                iteration += 1
            iterations[-1].append(iteration)
    return iterations

def optimized_plot_set(size, max_iteration, position_percent = (0,0), size_percent = (1, 1)):
    iterations = []
    for pixel_x in range(size[0]):
        iterations.append([])
        for pixel_y in range(size[1]):
            x0 = scale_x(pixel_x, size[0], position_percent[0], size_percent[0])
            y0 = scale_y(pixel_y, size[1], position_percent[1], size_percent[1])
            x = 0.0
            y = 0.0
            iteration = 0
            x2 = 0
            y2 = 0
            while (x*x + y*y <= 4 and iteration < max_iteration):
                y = 2 * x * y + y0
                x = x2 - y2 + x0
                x2 = x * x
                y2 = y * y
                iteration += 1
            iterations[-1].append(iteration)
    return iterations

def scale_x(x, width, x_percent = 0, width_percent = 1 ):
    return (x_percent * 3.5) + (width_percent * x * 3.5 / width) - 2.5

def scale_y(y, height, y_percent = 0, height_percent = 1):
    return (y_percent * 2) + (height_percent * y * 2 / height) - 1

def color_set(iterationCounts, max_iteration):
    NumIterationsPerPixel = [0] * (max_iteration + 1)
    for row in iterationCounts:
        for interation in row:
            NumIterationsPerPixel[interation] += 1
    total = sum(NumIterationsPerPixel)
    hue = []
    for row in iterationCounts:
        hue.append([])
        for iteration in row:
            hue[-1].append(0.0)
            for i in range(iteration):
                hue[-1][-1] += NumIterationsPerPixel[i] / total
    return [[get_color(h) for h in row] for row in hue]

def get_color(hue):
    color = str(int(255255255 * hue))
    color = "0"*(9-len(color)) + color
    return int(color[0:3]), int(color[3:6]), int(color[6:9]) 

def make_img(hues, name):
    img = Image.new("RGB", (len(hues), len(hues[0])))
    for x, row in enumerate(hues):
        for y, color in enumerate(row):
            img.putpixel((x,y), color)
    img.save(name)
    

SIZE = 750 , 500
POSITION_PERCENT = 0,0
SIZE_PERCENT = 1,1
MAX_ITERATION = 1000
IMAGE_NAME = "./Mandelbrot.png"
make_img(
    color_set(
        optimized_plot_set(SIZE, MAX_ITERATION, POSITION_PERCENT, SIZE_PERCENT), 
        MAX_ITERATION),
    IMAGE_NAME       
)