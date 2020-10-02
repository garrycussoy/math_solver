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
import random
import string
import json

# Import core modules
from core.main import get_problem
from core.main import solve_problem

# Following function will render main page of the apps
def index(request):
    return render(request, 'index.html')

"""
Following functions will handle the logic when user submit the problem through form
"""
# This first function will take the image and topic from user, and then send it to the server
def upload_image(request):
    try:
        # Get the input image
        problem_image = request.FILES['problem_image'].read()
        problem_image = base64.b64encode(problem_image)
        problem_image = Image.open(BytesIO(base64.b64decode(problem_image)))

        # Generate random 16-digit string
        file_name = ''.join(random.choice(string.ascii_lowercase) for count in range(16)) + '.png'

        # Save the image in the folder
        problem_image.save('math_solver_app/static/problem/' + file_name, 'PNG')

        # Render problem detection loading page
        container = {
            'image_path': '../static/problem/' + file_name,
            'file_name': file_name,
            'topic_field': request.POST['topic_field']
        }
        return render(request, 'problemDetectionLoading.html', container)
    except:
        # Prepare error message
        message = {
            'message': 'No Image Uploaded or File Not Supported'
        }

        # Render error page
        return render(request, 'error.html', message)

# This second function will scan the image to extract the problem
def extract_problem(request):
    try:
        # Get image file name and the problem topic
        file_name = request.POST['file_name']
        topic = request.POST['topic_field']

        # Read the image in numpy format and then delete the image file
        problem_image = cv2.imread('math_solver_app/static/problem/' + file_name)
        os.remove('math_solver_app/static/problem/' + file_name)

        # Get the features
        features = get_problem(problem_image)

        # Save the features into json file
        file_name = file_name[:-4] + '.json'
        file_path = 'math_solver_app/static/features/' + file_name
        with open(file_path, 'w+') as features_file:
            json.dump(features, features_file, indent = 4)

        # Render solving problem loading page
        container = {
            'file_path': file_path,
            'topic': topic
        }
        return render(request, 'solvingProblemLoading.html', container)
    except:
        # Prepare error message
        message = {
            'message': 'An Error Occured While Scanning The Problem'
        }

        # Render error page
        return render(request, 'error.html', message)

# This third function will solve the problem and return the result back to the user
def solve(request):
    try:
        # Get file path and topic
        file_path = request.POST['file_path']
        topic = request.POST['topic']
        # Get features which are stored in a json file
        features = None
        with open(file_path) as features_file:
            features = json.load(features_file)
        
        # Remove json file
        os.remove(file_path)

        # Solve the problem
        qna_dict = solve_problem(features, topic)

        # Render solution page
        return render(request, 'solution.html', qna_dict)
    except:
        # Prepare error message
        message = {
            'message': 'An Error Occured While Solving The Problem'
        }

        # Render error page
        return render(request, 'error.html', message)
