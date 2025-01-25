from flask import Flask, request, render_template
import google.generativeai as gen_ai
from face_emotion import emotions_extract
from image_to_ import detect_objects_and_scene
from scene_detect import classify_scene

# Initialize Flask app
app = Flask(__name__)

# Set up the Google API Key and configure the generative AI model
GOOGLE_API_KEY = "AIzaSyA2JNXTR65XZ-wU3tVPcgoeW_bwKZagMPk"
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

def generate_story(emotions, objects, scene):
    # Create a prompt based on the detected inputs  
    prompt = (
        f"Write a simple story that should contain a moral for children based on the following:\n\n"
        f"- Detected Emotions: {', '.join(emotions)}\n"
        f"- Detected Objects: {', '.join(objects)}\n"
        f"- Scene/Background: {scene}\n\n"
        "The story should be easy to understand, with simple words. Use the emotions, objects, and scene to create a fun and happy story. "
        "Make sure the story is gentle and friendly for kids, with a happy ending."
    )

    response = model.generate_content(prompt)
    return response.text.strip()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/generate-story', methods=['POST'])
def generate_story_from_image():
    if 'image' not in request.files:
        return "No file part", 400

    image = request.files['image']
    if image.filename == '':
        return "No selected file", 400

    #Save the image
    image_path = 'uploads/' + image.filename
    image.save(image_path)

    # Extract emotions, objects, and scenes from the uploaded image
    detected_emotions = emotions_extract(image_path)
    detected_objects = detect_objects_and_scene(image_path)
    detected_scene = classify_scene(image_path)
    
    # Generate the story based on the extracted information
    story = generate_story(detected_emotions, detected_objects, detected_scene)
    
    # Display the generated story
    return  render_template("index.html",story=story)

if __name__ == '__main__':
    app.run(debug=True)
