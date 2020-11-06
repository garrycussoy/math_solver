# Import django related tools
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Import other packages
from PIL import Image
from io import BytesIO
from firebase_admin import storage
import numpy as np
import cv2
import base64
import os
import random
import string
import json
import urllib

# Import core modules
from core.main import get_problem
from core.main import solve_problem

"""
Following function will create blob that connect to an image path in firebase
"""
def create_blob(file_path):
    # Connect to bucket
    bucket = storage.bucket()

    # Create blob
    blob = bucket.blob(file_path)
    return blob

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

        # Get the size of inputted image
        width, height = problem_image.size

        # Resize inputted image
        max_long = 300
        new_width = 0
        new_height = 0
        if width > height:
            new_width = max_long
            new_height = (height * max_long) // width
        else:
            new_height = max_long
            new_width = (width * max_long) // height
        problem_image = problem_image.resize((new_width, new_height))

        # Save as byte array
        img_byte_arr = BytesIO()
        problem_image.save(img_byte_arr, format = 'PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Generate random 16-digit string for image name
        image_name = ''.join(random.choice(string.ascii_lowercase) for count in range(16))

        # Create blob to upload the image to firebase
        blob = create_blob('problem/' + image_name)
        blob.upload_from_string(img_byte_arr)

        # Get public URL for that image
        blob.make_public()
        image_url = blob.public_url

        # Render problem detection loading page
        container = {
            'image_url': image_url,
            'image_name': image_name,
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
        # Get image name and the problem topic
        image_name = request.POST['image_name']
        topic = request.POST['topic_field']

        # Get the image from firebase
        blob = create_blob('problem/' + image_name)
        bytes_img = blob.download_as_bytes()
        problem_image = cv2.imdecode(np.frombuffer(bytes_img, np.uint8), -1)

        # Process the feature and get the features
        features, processed_image = get_problem(problem_image)

        # Save processed image as byte array
        _, encoded_image = cv2.imencode('.png', processed_image)
        encoded_bytes = encoded_image.tobytes()

        # Generate random 16-digit string for processed image name
        processed_image_name = ''.join(random.choice(string.ascii_lowercase) for count in range(16))

        # Save processed image to firebase
        blob = create_blob('problem/' + processed_image_name)
        blob.upload_from_string(encoded_bytes)

        # Get public URL for that processed image
        blob.make_public()

        # Turn dictionary features into string
        features_str = json.dumps(features)

        # Render solving problem loading page
        container = {
            'original_image_name': image_name,
            'processed_image_name': processed_image_name,
            'features_string': features_str,
            'topic': topic
        }
        return render(request, 'solvingProblemLoading.html', container)
    except:
        # Remove original image from firebase
        blob = create_blob('problem/' + image_name)
        blob.delete()

        # Prepare error message
        message = {
            'message': 'An Error Occured While Scanning The Problem'
        }

        # Render error page
        return render(request, 'error.html', message)

# This third function will solve the problem and return the result back to the user
def solve(request):
    try:
        # Get features, image name (both processed and original image) and topic
        features_string = request.POST['features_string']
        original_image_name = request.POST['original_image_name']
        processed_image_name = request.POST['processed_image_name']
        topic = request.POST['topic']

        # Get the processed image from firebase
        req = urllib.request.urlopen('https://storage.googleapis.com/math-solver-app.appspot.com/problem/' + processed_image_name)
        arr = np.asarray(bytearray(req.read()), dtype = np.uint8)
        image = cv2.imdecode(arr, -1)

        # Turn back string features into dictionary format
        features = json.loads(features_string)

        # Solve the problem
        qna_dict = solve_problem(image, features, topic)

        # Remove the image (both original and processed image)
        blob = create_blob('problem/' + original_image_name)
        blob.delete()
        blob = create_blob('problem/' + processed_image_name)
        blob.delete()

        # Render solution page
        return render(request, 'solution.html', qna_dict)
    except:
        # Remove the image (both original and processed image)
        blob = create_blob('problem/' + original_image_name)
        blob.delete()
        blob = create_blob('problem/' + processed_image_name)
        blob.delete()

        # Prepare error message
        message = {
            'message': 'An Error Occured While Solving The Problem'
        }

        # Render error page
        return render(request, 'error.html', message)
