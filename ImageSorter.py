
from imageai.Detection import ObjectDetection
import os

def objectDetection():
    execution_path = os.getcwd()

    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.abspath("E:/VisualProjects/ImageSorter/ImageSorter/resnet50_coco_best_v2.1.0.h5"))
    detector.loadModel()

    directoryIn = os.path.abspath("E:/VisualProjects/ImageSorter/ImageSorter/images")
    directoryOut = os.path.abspath("E:/VisualProjects/ImageSorter/ImageSorter/newImages")

    for filename in os.listdir(directoryIn):
    #for filename in glob.iglob(directoryIn + '**/**', recursive=True):
        imagePath = os.path.join(directoryIn, filename)
        outputPath = os.path.join(directoryOut, filename)
        if os.path.isfile(imagePath):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                detections = detector.detectObjectsFromImage(input_image=imagePath, output_image_path=outputPath, minimum_percentage_probability=50)
                print(imagePath)
                for eachObject in detections:
                    print(eachObject["name"], " : ", eachObject["percentage_probability"])

