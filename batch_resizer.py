from PIL import Image
import os
import io

def batch_resize_image(image, target_directory, sizes, resample = Image.BICUBIC, max_size_kilobytes = 100, brute_force_step = 1, max_quality = 100, min_quality = 1):    
    for size in sizes:
        resized = image.resize(size, resample)
        (width, height) = size
        target_file = os.path.join(target_directory, str(width) + "x" + str(height) + ".jpg")
        quality = max_quality
        while True:
            with io.BytesIO() as output:
                resized.save(output, format = "JPEG", optimize = True, quality = quality)
                file_size = output.getbuffer().nbytes / 1000
                if file_size >= max_size_kilobytes:
                    quality -= brute_force_step
                    print("Reducing quality: " + str(quality))
                    if quality < min_quality:
                        print("Quality can't be less then zero!")
                        return False
                else:
                    print("Quality conforms restrictions: " + str(quality))
                    with open(target_file, "wb") as outfile:
                        outfile.write(output.getbuffer())
                    break
    
    return True

def batch_resize(file, target_directory, sizes, resample = Image.BICUBIC, max_size_kilobytes = 100, brute_force_step = 1, max_quality = 100, min_quality = 1):
    image = Image.open(file)

    return batch_resize_image(image, target_directory, sizes, resample, max_size_kilobytes, brute_force_step, max_quality, min_quality)