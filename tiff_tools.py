import os
import glob
import numpy as np
import tifffile as tiff


def get_tiff_files(input_folder):
    image_files = sorted(
        glob.glob(os.path.join(input_folder, "*.tif")) +
        glob.glob(os.path.join(input_folder, "*.tiff"))
    )

    if len(image_files) == 0:
        raise FileNotFoundError("No TIFF files found in the selected folder.")

    return image_files


def list_images(input_folder):
    image_files = get_tiff_files(input_folder)

    print("\nNumber of TIFF images found:", len(image_files))

    for i, file in enumerate(image_files, start=1):
        print(i, ":", os.path.basename(file))

    return image_files


def ask_output_name(message):
    output_name = input(message).strip()

    if output_name == "":
        raise ValueError("Output name cannot be empty.")

    return output_name


def check_selected_numbers(image_files, selected_numbers):
    selected_numbers = list(selected_numbers)

    for number in selected_numbers:
        if number < 1 or number > len(image_files):
            raise ValueError(
                f"Image number {number} is invalid. Choose between 1 and {len(image_files)}."
            )

    return selected_numbers


def average_images(input_folder, selected_numbers, output_name=None):
    image_files = get_tiff_files(input_folder)

    selected_numbers = check_selected_numbers(image_files, selected_numbers)
    selected_files = [image_files[i - 1] for i in selected_numbers]

    print("\nSelected images for averaging:")
    for i, file in zip(selected_numbers, selected_files):
        print(i, ":", os.path.basename(file))

    images = []

    first_img = tiff.imread(selected_files[0])
    first_shape = first_img.shape
    original_dtype = first_img.dtype

    for file in selected_files:
        img = tiff.imread(file)

        if img.shape != first_shape:
            raise ValueError("All selected images must have the same size for averaging.")

        images.append(img.astype(np.float64))

    stack = np.stack(images, axis=0)
    average_image = np.mean(stack, axis=0)

    if output_name is None:
        output_name = ask_output_name("Enter name for averaged image without extension: ")

    output_file = os.path.join(input_folder, output_name + ".tiff")
    tiff.imwrite(output_file, average_image.astype(original_dtype))

    print("\nAverage image saved as:")
    print(output_file)

    return output_file


def subtract_images(input_folder, image_number, background_number, output_name=None):
    image_files = get_tiff_files(input_folder)

    check_selected_numbers(image_files, [image_number, background_number])

    image_file = image_files[image_number - 1]
    background_file = image_files[background_number - 1]

    print("\nImage to correct:")
    print(image_number, ":", os.path.basename(image_file))

    print("\nBackground image:")
    print(background_number, ":", os.path.basename(background_file))

    image_to_correct = tiff.imread(image_file).astype(np.float64)
    background_image = tiff.imread(background_file).astype(np.float64)

    if image_to_correct.shape != background_image.shape:
        raise ValueError("Images are not the same size. Subtraction cannot be done.")

    subtracted_image = image_to_correct - background_image

    # Remove negative pixel values
    subtracted_image[subtracted_image < 0] = 0

    original_dtype = tiff.imread(image_file).dtype

    if output_name is None:
        image_base_name = os.path.splitext(os.path.basename(image_file))[0]
        output_name = "RESULT_" + image_base_name

    output_file = os.path.join(input_folder, output_name + ".tiff")
    tiff.imwrite(output_file, subtracted_image.astype(original_dtype))

    print("\nSubtracted image saved as:")
    print(output_file)

    return output_file


def average_then_subtract(
    input_folder,
    average_numbers,
    background_number,
    average_name=None,
    final_name=None
):
    average_file = average_images(input_folder, average_numbers, average_name)

    image_files = get_tiff_files(input_folder)

    average_index = None

    for i, file in enumerate(image_files, start=1):
        if os.path.abspath(file) == os.path.abspath(average_file):
            average_index = i
            break

    if average_index is None:
        raise FileNotFoundError("Average image was saved but not found after reloading folder.")

    final_file = subtract_images(
        input_folder,
        average_index,
        background_number,
        final_name
    )

    return final_file