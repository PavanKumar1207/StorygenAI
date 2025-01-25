from deepface import DeepFace

def emotions_extract(image_path):
    

    analysis = DeepFace.analyze(img_path=image_path, actions=['emotion'])

    print(f"Dominant Emotion: {analysis[0]['dominant_emotion']}")
    return analysis[0]['dominant_emotion']