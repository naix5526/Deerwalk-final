from .forms import ImageUploadForm
from django.shortcuts import render
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np


def handle_uploaded_file(f):
    with open('D:\environment\porfolio\img.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def skills(request):
    return render(request, 'skills.html')


def project(request):
    return render(request, 'project.html')


def demo(request):
    return render(request, 'demo.html')


def imageprocess(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['image'])
            model = ResNet50(weights='imagenet')
            img_path = 'img.jpg'

            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            preds = model.predict(x)
            print('Predicted:', decode_predictions(preds, top=3)[0])

            html = decode_predictions(preds, top=3)[0]
            res = []
            for e in html:
                res.append((e[1], np.round(e[2] * 100, 2)))

            return render(request, 'imgprocess.html', {'res': res})

    return render(request, 'imgprocess.html')

