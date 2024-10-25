import subprocess
import os
import glob
from PIL import Image
import cv2

def file_to_binary_string(file_path):
    """Convert file to a binary string."""
    with open(file_path, 'rb') as file:
        binary_code = file.read()
        binary_string = ''.join(format(byte, '08b') for byte in binary_code)
    return binary_string

def binary_to_image(binary_str):
    """Convert binary string to images."""
    img_width = 480
    img_height = 360
    index = 0
    count = 0

    while index < len(binary_str):
        image = Image.new("1", (img_width, img_height), color=1)
        for y in range(6, img_height, 6):
            for x in range(0, img_width, 6):
                if index < len(binary_str):
                    color = 0 if binary_str[index] == "1" else 1
                    for i in range(3):
                        for j in range(3):
                            image.putpixel((x + j, y + i), color)
                    index += 1
                else:
                    break  

        image.save(f"./images/binary_image_{count}.png")
        count += 1

def images_to_video(video_filename):
    """Convert images to video using OpenCV."""
    input_path = "./images/*.png"
    image_files = sorted(glob.glob(input_path))

    if not image_files:
        print("No images found to create video.")
        return

    fps = 1
    img = cv2.imread(image_files[0])
    height, width, _ = img.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
    out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

    for image_file in image_files:
        img = cv2.imread(image_file)
        out.write(img)

    out.release()  

def make_video(file_path):
    """Main function to convert file to video."""
    binary_string = file_to_binary_string(file_path)
    binary_to_image(binary_string)
    
    video_name = f"{os.path.splitext(file_path)[0]}.mp4"
    images_to_video(video_name)
    
    for img_file in glob.glob("./images/*.png"):
        os.remove(img_file)

file_path = r"D:\harsh\Code Playground\Innov8ure\infiniteStorage\test.txt"
make_video(file_path)