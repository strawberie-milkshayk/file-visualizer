import png
import sys

# python img_generator.py 1 [file name] [image name]
# python img_generator.py 2 [image name] [file name]
# python img_generator.py 3 [config file name]
# python img_generator.py 4 [file name] [image width/height (square)]

def main():
    print('starting!')
    args = process_sys_args(sys.argv)
    program(args)

def program(args):
    mode = args[1]
    if mode == "1":
        run_mode1(args[2], args[3])
    elif mode == "2":
        run_mode2(args[2], args[3])
    elif mode == "3":
        run_mode3(args[2])
    elif mode == "4":
        run_mode4(args[2], args[3])


def process_sys_args(args):
    if len(args) <= 1:
        args = get_args(args)
        return args


def get_args(args):
    file_location = args[0]
    mode_input_message = '1: file to single image\n2: single image to file\n3: multiple images to file (requires decode config file)\n4: file to multiple images (also generates decode config file)\ninput mode [1, 2, 3, 4]: '
    mode_params = ['x = int(x)', 'assert int(x) in range(1, 5)']
    mode = persistant_data_get(mode_input_message, 'please try again!', mode_params)
    mode = int(mode)
    if mode == 1:
        mode1_file_params = ['f = open(x, \'rb\')', 'f.read()', 'f.close()']
        mode1_img_params = ['assert 1 == 1']
        file_name = persistant_data_get('input file name: ', 'please try again!', mode1_file_params)
        img_name = persistant_data_get('output image name: ', 'please try again!', mode1_img_params)
        return [file_location, "1", file_name, img_name]
    elif mode == 2:
        mode2_img_params = ['f = open(x, \'rb\')', 'f.read()', 'f.close()']
        mode2_file_params = ['assert 1 == 1']
        img_name = persistant_data_get('input image name: ', 'please try again!', mode2_img_params)
        file_name = persistant_data_get('output file name: ', 'please try again!', mode2_file_params)
        return [file_location, '2', img_name, file_name]
    elif mode == 3:
        mode3_config_params = ['f = open(x, \'r\')', 'f.read()', 'f.close()']
        config_file_name = persistant_data_get('input config file name: ', 'please try again!', mode3_config_params)
        return [file_location, '3', config_file_name]
    elif mode == 4:
        mode4_file_params = ['f = open(x, \'rb\')', 'f.read()', 'f.close()']
        mode4_dimensions_params = ['assert int(x) >= 3', 'assert int(x) <= 10000']
        file_name = persistant_data_get('input file name: ', 'please try again!', mode4_file_params)
        dimensions = persistant_data_get('input single number for width/height[3-10000]: ', 'please try again!', mode4_dimensions_params)
        return [file_location, '4', file_name, dimensions]


def run_mode1(file_name, img_name):
    file_to_single_img(file_name, img_name)


def run_mode2(img_name, file_name):
    img_to_file(img_name, file_name)


def run_mode3(config_file_name):
    f = open(config_file_name, 'r')
    config_data = f.read()
    f.close()
    config_data = config_data.split('\n')
    new_config_data = [item for item in config_data if item]
    config_data = new_config_data
    version = config_data[0]
    file_name = config_data[1]
    ordered_image_names = [0 for x in range(2,len(config_data))]
    for row in config_data[2:len(config_data)]:
        row_data = row.split('\t')
        index = int(row_data[0])
        img_name = row_data[1]
        ordered_image_names[index] = img_name
    all_bytes = []
    for image in ordered_image_names:
        data = extract_byte_array_from_png(image)
        all_bytes += data[0]
    write_file_from_byte_array(all_bytes, file_name)


def run_mode4(file_name, dimensions):
    dimensions = int(dimensions)
    config_file_name = 'config.txt'
    f = open(config_file_name, 'w')
    f.write('1.0\n')
    f.write(file_name + '\n')
    file_data = read_binary_file(file_name)
    values_per_image = dimensions* dimensions * 3
    images = []
    image = []
    for val in file_data:
        image.append(val)
        if len(image) == values_per_image:
            images.append(image)
            image = []
    if image:
        images.append(image)
        image = []
    idx = 0
    for image1 in images:
        img_name = 'generated_image' + str(idx) + '.png'
        write_png(image1, img_name, [dimensions, dimensions])
        f.write(str(idx) + '\t' + img_name + '\n')
        idx += 1
    f.close()
        

    
def persistant_data_get(input_message, fail_message, params):
    valid = False
    while not valid:
        try:
            x = input(input_message)
            for param in params:
                exec(param)
            valid = True
            return x
        except:
            print(fail_message)

def img_to_file(img_name, file_name):
    try:
        data = extract_byte_array_from_png(img_name)
        write_file_from_byte_array(data[0], file_name)
        return True
    except:
        print('unknown error!')
        return False

def file_to_single_img(file_name, img_name):
    print('reading byte array . . .')
    byte_array = read_binary_file(file_name)
    print('byte array read!')
    dimensions = calculate_dimensions(byte_array)
    print('dimensions calculated!')
    print('creating png . . .')
    write_png(byte_array, img_name, dimensions)
    print('png has been created!')


def read_binary_file(file_name):
    try:
        f = open(file_name, 'rb')
        byte_array = f.read()
        f.close()
        return byte_array
    except:
        print('unable to read', file_name)
        return False


def write_png(byte_array, file_name, dimensions):
    byte_ct = len(byte_array)
    unused_bytes = 0
    width = dimensions[0]
    height = dimensions[1]
    img_out = (byte_array,)
    max_size = width * height * 3
    try:
        assert byte_ct <= max_size
    except:
        print('image not large enough to hold data!')
        return
    img = []
    idx = 0
    progress = 0
    print('initializing png write . . .')
    print('image of', width, 'x', height, 'will be created')
    for y in range(height):
        row = ()
        progress += 1
        if progress % 30 == 0:
            print(str(round(((progress / height) * 100), 5)) + '%')
        for x in range(width):
            if idx + 2 < byte_ct:
                row = row + (byte_array[idx], byte_array[idx+1], byte_array[idx+2])
            elif idx + 1 < byte_ct:
                row = row + (byte_array[idx], byte_array[idx+1], 0)
                unused_bytes += 1
            elif idx < byte_ct:
                row = row + (byte_array[idx], 0, 0)
                unused_bytes += 2
            else:
                row = row + (0, 0, 0)
                unused_bytes += 3
            idx += 3
        img.append(row)
    with open(file_name, 'wb') as f:
        w = png.Writer(width, height, greyscale=False)
        w.write(f, img)
    print(file_name, 'with dimensions', width, 'x', height, 'has been created!')
    print('there are', unused_bytes, 'unused bytes')


def round_up(num):
    try:
        assert num == int(num)
    except:
        if float(round(num)) == float(num // 1):
            num += 1
            num = round(num)
        else:
            num = round(num)
    return num


def calculate_dimensions(byte_array):
    byte_ct = len(byte_array)
    width = ((byte_ct/3) ** 0.5)
    width = round_up(width)
    return [width, width]


def extract_byte_array_from_png(file_name):
    r=png.Reader(file_name)
    data = r.read()
    width = data[0]
    height = data[1]
    image = data[2]
    image_data = []
    for row in image:
        for value in row:
            image_data.append(value)
    while image_data[len(image_data)-1] == 0:
        image_data.pop(len(image_data)-1)
    return [image_data, [width, height]]


def write_file_from_byte_array(byte_array, file_name):
    f = open(file_name, "wb")
    arr = bytearray(byte_array)
    f.write(arr)
    f.close()
        

if __name__ == '__main__':
    main()


