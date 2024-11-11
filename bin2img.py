#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 date:3/6/2022
 author:Cla1r3 (Modified)
 Transform binary (.vmem) files in a specified directory to RGB PNG images,
 saving them in a separate output directory.
"""

import time
import math
import os
import sys
from numba import jit
from PIL import Image, ImageDraw

@jit(nopython=True, cache=True)
def determine_size(data):
    # Calculate image size based on data length
    num_bytes = len(data)
    num_pixels = int(math.ceil(float(num_bytes) / 3.0))
    sqrt = math.sqrt(num_pixels)
    size = int(math.ceil(sqrt))
    return size, size

@jit(nopython=True, cache=True)
def calccolor(byteval):
    # Map byte value to an RGB color
    return (
        ((byteval & 0o300) >> 6) * 64,
        ((byteval & 0o070) >> 3) * 32,
        (byteval & 0o007) * 32,
    )

def bin2img(data):
    colorfunc = calccolor
    xsize, ysize = size = determine_size(data)
    print(f"Image size: {xsize}x{ysize}")
    img = Image.new("RGB", size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    print("Converting file to image...")

    i = 0
    for y in range(ysize):
        for x in range(xsize):
            if i < len(data):
                draw.point((x, y), fill=colorfunc(data[i]))
                i += 1
            else:
                break

    print("Image conversion complete.")
    return img

def generate_image(infile):
    with open(infile, "rb") as f:
        data = f.read()
        print(f"Successfully read {infile}")
    return bin2img(data)

if __name__ == "__main__":
    # Specify the input directory for .vmem files and output directory for images
    input_dir = r"C:\Users\Amir\Desktop\Git\project\vmrun-python\snapshots"
    output_dir = r"C:\Users\Amir\Desktop\Git\project\vmrun-python\images"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        vmem_files = [f for f in os.listdir(input_dir) if f.endswith('.vmem')]
        for vmem_file in vmem_files:
            start_time = time.time()
            print(f"\nProcessing file: {vmem_file}")

            infile_path = os.path.join(input_dir, vmem_file)
            output_file_name = os.path.splitext(vmem_file)[0] + ".png"
            output_path = os.path.join(output_dir, output_file_name)

            img = generate_image(infile_path)
            img.save(output_path, "PNG", compress_level=9)
            print(f"Image saved at {output_path}")

            end_time = time.time()
            print(f"Processing time: {end_time - start_time:.2f} seconds")

    except KeyboardInterrupt:
        print("Process interrupted.")
