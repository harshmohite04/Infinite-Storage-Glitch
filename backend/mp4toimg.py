import cv2
import os
from PIL import Image

def image_to_binary(image_path):
    """Convert an image to a binary string based on pixel color."""
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    binary_str = ""

    for x in range(width // 3):
        r, g, b = 0, 0, 0
        for i in range(3):
            for j in range(3):
                r1, g1, b1 = pixels[3 * x + j, i]
                r += r1
                g += g1
                b += b1

        if r < 200 and g < 200 and b < 200:
            binary_str += "1"
        elif r > 200 and g > 200 and b > 200:
            binary_str += "0"

    for y in range(6, height, 6):
        for x in range(0, width, 6):
            r, g, b = pixels[x, y]
            if r < 200 and g < 200 and b < 200:
                binary_str += "1"
            elif r > 200 and g > 200 and b > 200:
                binary_str += "0"

    return binary_str

def binary_string_to_file(binary_string, file_path):
    """Convert a binary string back to a file."""
    with open(file_path, 'wb') as file:
        bytes_list = [int(binary_string[i:i + 8], 2) for i in range(0, len(binary_string), 8)]
        bytes_arr = bytearray(bytes_list)
        file.write(bytes_arr)

def capture_frame(file_path):
    """Extract frames from a video file using OpenCV."""
    if not os.path.exists('data'):
        os.makedirs('data')

    video = cv2.VideoCapture(file_path)
    frame_count = 0

    while True:
        success, frame = video.read()
        if not success:
            break

        output_frame_path = f"data/binary_image_{frame_count + 1}.png"
        cv2.imwrite(output_frame_path, frame)
        frame_count += 1

    video.release()

def remove_img(path):
    """Remove an image file."""
    try:
        os.remove(path)
    except OSError:
        print(f"No image found at: {path}")

def reconstruct_file_from_images(file_path, original_length=None):
    """Reconstruct a file from binary data extracted from images."""
    file_name = file_path.split('.')
    print(f"Split file name: {file_name}")  

    if len(file_name) < 2:  
        print("Error: File name does not contain enough parts.")
        return

    capture_frame(file_path)

    hm = {}
    binary_from_image = ""

    directory = "data"
    onlyfiles = next(os.walk(directory))[2]
    number_of_images = len(onlyfiles)

    for i in range(number_of_images):
        image_path = f"data/binary_image_{i + 1}.png"
        binary_from_image = image_to_binary(image_path)

        key = int(binary_from_image[:160], 2)
        if key not in hm:
            hm[key] = binary_from_image[160:]

        remove_img(image_path)

    sorted_keys = sorted(hm.keys())
    sorted_dict = {key: hm[key] for key in sorted_keys}

    original_binary_str = ""
    for _, v in sorted_dict.items():
        original_binary_str += v

    if original_length is not None:
        original_binary_str = original_binary_str[:original_length]
    else:
        # Optional: You can just use the length of the reconstructed string
        # original_binary_str = original_binary_str[:len(original_binary_str)]
        print("Warning: Original length not provided, using full reconstructed string length.")

    binary_string_to_file(original_binary_str, f"{file_name[0]}-output.{file_name[1]}")
    print(f"Reconstructed file created: {file_name[0]}-output.{file_name[1]}")

file_path = r"test.mp4"
original_file_path = r"test.mp4"
original_file_length = os.path.getsize(original_file_path)
reconstruct_file_from_images(file_path, original_length=original_file_length)
