from PIL import Image
import os
from tqdm import tqdm

DEFAULT_ICON_SIZES = [16, 32, 48, 128, 256]

def resize_image(image_path, output_folder, icon_sizes, convert_to_png):
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found.")
        return
    except OSError:
        print(f"❌ Error: The file '{image_path}' is not a valid image format.")
        return

    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            print(f"✅ Created folder: {output_folder}")
        except Exception as e:
            print(f"❌ Error creating folder: {e}")
            return

    for size in tqdm(icon_sizes, desc="Resizing images", unit="size", ncols=100):
        try:
            tqdm.write(f"🔄 Resizing to {size}px...")
            
            img_copy = img.copy()
            img_copy.thumbnail((size, size), Image.Resampling.LANCZOS)
            
            new_img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
            left = (size - img_copy.width) // 2
            top = (size - img_copy.height) // 2
            new_img.paste(img_copy, (left, top))
            
            output_extension = 'png' if convert_to_png else image_path.split('.')[-1].lower()
            output_path = os.path.join(output_folder, f"{size}.{output_extension}")
            
            new_img.save(output_path)
            tqdm.write(f"✅ Saved resized image: {output_path}")
        except Exception as e:
            print(f"❌ Error resizing image {size}px: {e}")

def main():
    image_path = input("Enter the image file path: ").strip('"')
    if not os.path.exists(image_path):
        print("❌ Error: The provided image path does not exist.")
        return
    
    output_folder = input("Enter the folder to save resized images (default: 'output'): ").strip()
    
    if not output_folder:
        output_folder = os.path.join(os.path.dirname(image_path), "output")

    if not os.access(output_folder, os.W_OK):
        print(f"❌ Error: No write permission in the folder '{output_folder}'.")
        return

    custom_sizes_input = input("Would you like to input custom sizes? (y/n): ").strip().lower()

    if custom_sizes_input == 'y':
        custom_sizes = input("Enter the sizes separated by commas (e.g., 16,32,64): ")
        try:
            icon_sizes = [int(size.strip()) for size in custom_sizes.split(',')]
        except ValueError:
            print("❌ Error: Please input valid integers for sizes.")
            return
    else:
        icon_sizes = DEFAULT_ICON_SIZES

    convert_to_png_input = input("Do you want to convert the images to PNG format? (y/n): ").strip().lower()

    convert_to_png = convert_to_png_input == 'y'

    resize_image(image_path, output_folder, icon_sizes, convert_to_png)

if __name__ == "__main__":
    main()
