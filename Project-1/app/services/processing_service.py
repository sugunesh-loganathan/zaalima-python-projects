from PIL import Image
import os


def resize_image(input_path: str):

    os.makedirs("processed", exist_ok=True)

    file_name = os.path.basename(input_path)

    output_path = f"processed/{file_name}"

    image = Image.open(input_path)

    image = image.resize((800, 800))

    image.save(
        output_path,
        optimize=True,
        quality=70
    )

    return output_path
def delete_file(file_path: str):

    if os.path.exists(file_path):
        os.remove(file_path)