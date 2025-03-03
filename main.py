from flask import Flask, render_template, request, send_file, jsonify
import os
import logging
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline
from utils import gigachat_utils, image_utils, comic_utils

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize Stable Diffusion Pipeline
MODEL_ID = "stabilityai/stable-diffusion-2-1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
pipe = None  # Initialize pipe as None
try:
    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID)
    pipe = pipe.to(DEVICE)
    logging.info(f"Stable Diffusion pipeline successfully loaded on {DEVICE}")
    if DEVICE == "cuda":
        logging.info(f"GPU is available!")
        logging.info(f"GPU name: {torch.cuda.get_device_name(0)}")
        logging.info(f"Available GPU memory: {torch.cuda.get_device_properties(0).total_memory}")
    else:
        logging.info("GPU is not available, using CPU.")
except Exception as e:
    logging.error(f"Error loading Stable Diffusion pipeline: {e}")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate_comic', methods=['POST'])
def generate_comic(text=None):
    try:
        if text is None:
            text = request.form['text']
        logging.info(f"Received text from user: {text}")

        # 1. Split the text into scenes
        scenes = comic_utils.split_into_scenes(text)
        logging.info(f"Text split into {len(scenes)} scenes.")

        # 2. Generate a scenario for the comic using GigaChat
        full_scenario = ""
        for i, scene in enumerate(scenes):
            logging.info(f"Generating scenario for scene {i + 1}: {scene}")
            scenario = gigachat_utils.generate_comic_scenario(scene)  # Using GigaChat
            if scenario:
                full_scenario += scenario + "\n\n"
                logging.info(f"Scenario for scene {i + 1} successfully generated.")
            else:
                scenario = "Failed to generate scene description."
                logging.error(f"Failed to generate scenario for scene {i + 1}.")
                full_scenario += scenario + "\n\n"

        # 3. Generate images for the comic
        comic_file = generate_comic_from_text(full_scenario)

        if comic_file:
            return send_file(comic_file, as_attachment=True, download_name='comic.png')
        else:
            return render_template('error.html', message="Failed to generate comic.")

    except Exception as e:
        logging.exception("Error during comic generation:")
        return render_template('error.html', message=f"An error occurred: {str(e)}")

@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"Internal server error: {e}")
    return render_template('error.html', message="Internal server error"), 500


def generate_comic_from_text(text):
    """Generates a comic from text (scenario)."""
    scenes = text.split('\n\n')  # Split text into scenes
    image_paths = []
    images = []

    try:
        # Guarantee processing of only the first 1 scene
        for i, scene in enumerate(scenes[:1]):  # MODIFIED: PROCESSING ONLY THE FIRST SCENE
            scene = scene.strip()
            if scene:  # Check that the scene is not empty
                # Split the scene into 4 frames
                kadrs = scene.split('Frame')  # Assume that the frames are separated by the word "Frame"
                kadrs = [k.strip() for k in kadrs if k.strip()]  # Clean and filter

                # Process only the first four frames
                for j, kadr in enumerate(kadrs[:4]):  # Limit to only 4 frames
                    prompt = f"comic: {kadr}, bright colors, anime"
                    logging.info(f"Generating image for frame {j + 1}, scene {i + 1}: {prompt}")

                    try:
                        if pipe is not None:
                            image = pipe(prompt, num_inference_steps=40, guidance_scale=7.5, height=512, width=512).images[0]
                            image_path = os.path.join(image_utils.TEMP_IMAGE_DIR, f'scene_{i}_kadr_{j}.png')
                            image.save(image_path)
                            image.close()  # Free file

                            try:
                                # Add text to image
                                output_image_path = os.path.join(image_utils.TEMP_IMAGE_DIR, f'scene_{i}_kadr_{j}_with_text.png')
                                image_with_text = image_utils.add_text_to_image(image_path, kadr, output_image_path)  # not passing scene

                                if image_with_text:
                                    img = Image.open(image_with_text)  # Open the generated image
                                    images.append(img)
                                    img.close()  # Close the generated image
                                    image_paths.append(output_image_path)
                                    os.remove(image_path)  # Delete the original image
                                    logging.info(f"Text successfully added to image {output_image_path}")


                                else:
                                    image_paths.append(image_path)
                                    logging.warning(f"Failed to add text to image, using the original image {image_path}")


                            except Exception as e:
                                logging.exception(f"Error overlaying text for frame {j + 1}, scene {i + 1}: {str(e)}")
                                # Add the original image
                                image_paths.append(image_path)

                        else:
                            logging.error("Stable Diffusion pipeline is not loaded!")
                            continue #Instead of a black image, skip the frame

                    except Exception as e:
                        logging.exception(f"Error generating image for frame {j + 1}, scene {i + 1}: {str(e)}")
                        # Instead of a black image, skip the frame
                        logging.warning(
                            f"Failed to generate image for frame {j + 1}, scene {i + 1}. Skipping frame.")
                        continue  # Go to the next frame

        if images:
            comic_path = os.path.join(image_utils.TEMP_IMAGE_DIR, "comic.png")
            comic_path = image_utils.assemble_comic_strip(image_paths, comic_path)
            logging.info(f"Comic assembled and saved: {comic_path}")
            return comic_path
        else:
            logging.warning("No images were generated!")
            return None

    except Exception as e:
        logging.exception(f"Error during comic assembly: {str(e)}")
        return None
    finally:
        # Make sure temporary images are deleted
        image_utils.cleanup_images(image_paths)

if __name__ == '__main__':
    app.run(debug=True)