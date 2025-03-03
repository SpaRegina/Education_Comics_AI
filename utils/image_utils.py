import os
import logging
from PIL import Image, ImageDraw, ImageFont

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directory for temporary images
TEMP_IMAGE_DIR = "temp_images"

def create_black_image(width, height, filepath):
    """Creates and saves a black image."""
    try:
        image = Image.new('RGB', (width, height), color='black')
        image.save(filepath)
        image.close()
        logging.info(f"Black image created and saved: {filepath}")
    except Exception as e:
        logging.error(f"Error creating black image: {e}")

def assemble_comic_strip(image_paths, output_path):
    """Assembles a comic strip from individual images."""
    try:
        images = []
        for path in image_paths:
            try:
                img = Image.open(path)
                images.append(img)
            except Exception as e:
                logging.error(f"Error opening image {path}: {e}")
                return None  # Stop assembling the comic

        total_height = sum(img.height for img in images)
        max_width = max(img.width for img in images)

        # Create image for comic strip
        comic_image = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for img in images:
            comic_image.paste(img, (0, y_offset))
            y_offset += img.height

            img.close()  # Free resources

        comic_image.save(output_path)
        comic_image.close()  # Free resources
        logging.info(f"Comic assembled and saved: {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"Error assembling comic: {e}")
        return None

def cleanup_images(image_paths):
    """Deletes temporary image files."""
    for path in image_paths:
        try:
            os.remove(path)
            logging.info(f"Temporary file deleted: {path}")
        except OSError as e:
            logging.warning(f"Error deleting temporary file {path}: {e}")
        except Exception as e:
            logging.error(f"Failed to delete temporary file {path}: {e}")

def add_text_to_image(image_path, text, output_path="output.png"):
    """Adds text to an image."""
    try:
        image = Image.open(image_path).convert("RGBA")
        draw = ImageDraw.Draw(image)

        # Select font and size
        font_path = "arial.ttf"  # Replace with the path to your font
        try:
            font = ImageFont.truetype(font_path, size=30)
        except IOError:
            # If the font is not found, use the default font
            font = ImageFont.load_default()

        # Determine text position
        # text_width, text_height = draw.textsize(text, font=font)  <--- REPLACE THIS LINE
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
        image_width, image_height = image.size
        text_position = (10, image_height - text_height - 10)  # Bottom left

        # Add shadow for better readability (optional)
        shadow_color = (0, 0, 0, 128)  # Black semi-transparent shadow
        shadow_offset = (2, 2)
        draw.text((text_position[0] + shadow_offset[0], text_position[1] + shadow_offset[1]), text, font=font, fill=shadow_color)

        # Write text
        text_color = (255, 255, 255, 255)  # White color
        draw.text(text_position, text, font=font, fill=text_color)

        # Save image
        image.save(output_path)
        image.close()  # <--- ADD THIS LINE
        logging.info(f"Text added to image and saved as {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"Error adding text to image: {e}")
        return None