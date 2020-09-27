# Import django related tools
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Import other packages
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import base64
import os

# Import core modules
from core.main import solve

# Following function will render main page of the apps
def index(request):
    return render(request, 'index.html')

# Following function will handle the logic when user submit the problem through form
def get_problem(request):
    # Get the image and turn it into numpy array format
    try:
        problem_image = request.FILES['problem_image'].read()
        problem_image = base64.b64encode(problem_image)
        problem_image = Image.open(BytesIO(base64.b64decode(problem_image)))
        problem_image.save('core/images/problem.png', 'PNG')
        problem_image = cv2.imread('core/images/problem.png')
        os.remove('core/images/problem.png')
    except:
        # Prepare error message
        message = {
            'message': 'No Image Uploaded or File Not Supported'
        }

        # Render error page
        return render(request, 'error.html', message)

    # Solve the problem
    try:
        qna_dict = solve(problem_image, request.POST['topic_field'])
    except:
        # Prepare error message
        message = {
            'message': 'There Is An Error Occured While Solving The Problem'
        }

        # Render error page
        return render(request, 'error.html', message)

    # Render the view
    return render(request, 'solution.html', qna_dict)
