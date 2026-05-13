# TIFF Image Processing Tools

This section explains how to use the TIFF image processing functions.

The tools can:

- List TIFF images in a folder
- Average selected TIFF images
- Subtract a background image
- Average selected images and then subtract a background image

---

## Main functions

### `list_images(input_folder)`

Lists all `.tif` and `.tiff` files in the selected folder.

```python
from tiff_tools import list_images

input_folder = r"C:\path\to\your\tiff_folder"

list_images(input_folder)

The function prints the number of TIFF images found and shows each image with a number.

average_images(input_folder, selected_numbers, output_name=None)

Averages selected TIFF images and saves the result as a new .tiff file.

from tiff_tools import average_images

average_images(
    input_folder,
    range(1, 11),
    output_name="AVG_LED_IR_BL_D31_05_2_50us"
)

In this example, images numbered 1 to 10 are averaged.

Notes:

Image numbering starts from 1.
All selected images must have the same size.
The output image is saved in the same folder.
Do not include .tiff in output_name; it is added automatically.
subtract_images(input_folder, image_number, background_number, output_name=None)

Subtracts a background image from a selected image.

from tiff_tools import subtract_images

subtract_images(
    input_folder,
    image_number=1,
    background_number=2
)

In this example, image 2 is subtracted from image 1.

Notes:

Both images must have the same size.
Negative pixel values are set to 0.
If output_name is not provided, the result is saved using the original image name with RESULT_ added at the beginning.

Example with custom output name:

subtract_images(
    input_folder,
    image_number=1,
    background_number=2,
    output_name="CORRECTED_IMAGE"
)
average_then_subtract(input_folder, average_numbers, background_number, average_name=None, final_name=None)

First averages selected images, then subtracts a background image from the averaged result.

from tiff_tools import average_then_subtract

average_then_subtract(
    input_folder,
    average_numbers=range(1, 11),
    background_number=12,
    average_name="AVG_IMAGE",
    final_name="FINAL_CORRECTED_IMAGE"
)

In this example:

Images 1 to 10 are averaged.
Image 12 is used as the background.
The final corrected image is saved as FINAL_CORRECTED_IMAGE.tiff.
Example workflow
from tiff_tools import list_images, average_images, subtract_images


input_folder = r"H:\Shared drives\Laboratori Golem\OLOGRAFIA\11) Progetti Trasversali\14) Holographic_Diffuser\3)Characterisation result\LDW\05_05_2026\AL&BL\RED_30us"

n = "D31_05'_2_"

# Show all TIFF images with their image numbers
list_images(input_folder)

# Average images 1 to 10
average_images(
    input_folder,
    range(1, 11),
    output_name="AVG_LED_IR_BL_" + n + "_50us_"
)

# Subtract background image 2 from image 1
subtract_images(
    input_folder,
    image_number=1,
    background_number=2
)
Important notes
TIFF files with .tif and .tiff extensions are supported.
Image numbers start from 1, not 0.
Images are sorted alphabetically before numbering.
Averaging requires all selected images to have the same size.
Background subtraction requires both images to have the same size.
Output files are saved in the same input folder.
