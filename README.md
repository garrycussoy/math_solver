# Math Solver (V0.1)
***Created By : Garry Ariel***
<br /><br />
## About Math Solver
Math Solver is an app to solve mathematics problem (complete with explanation) from image uploaded by user. The apps will scan the problem contained in the image, and then return the solution to the user. The process of the app is like the following.
1. User input image (jpeg / png format) which contains mathematics problem.
2. The apps take the image and do some preprocessing step to the image.
3. The apps extract the problem contained in the processed image. To classify its features, I use simple CNN model.
4. The apps will solve the problem and then return the result back to the user.
<br /><br />
## Technology Stack
This app use Django framework and Tensorflow for the model.
<br /><br />
## Run the Apps Locally
To run the apps locally, you can follow the following steps.
1. Create and activate your virtual environment
2. Clone this repository by ```git clone https://github.com/garrycussoy/math_solver.git```
3. Go inside the folder by ```cd math_solver```
4. Install requirements needed by running ```pip install -r requirements.txt```
5. Create your own Firebase project (you can create it here https://console.firebase.google.com/)
6. Get the credentials json file (reference : third step of https://medium.com/@abdelhedihlel/upload-files-to-firebase-storage-using-python-782213060064)
7. Put your credential json file at the root folder and name it ```google-credentials.json```
8. Setup .env file (you can see the example in .env.example file)
9. Run the apps by ```python manage.py runserver```
<br /><br />
## Deployed Apps
You can also try the deployed apps in https://math-solver-app.herokuapp.com/
<br /><br />
## Limitation
This app is still in development. There are some limitations to make this app works well.
- It is recommended to not use flash when taking the image
- It is recommended to write the problem using black pen in a white paper
- Take the image so that the noise of the image as minimum as possible
- Make sure the text is horizontally oriented
- For this version, the apps can only support addition, substraction and multiplication of integers (can also use bracket)
<br /><br />
## Sample Image
For sample working images, you can find them here http://www.mediafire.com/folder/80rsd6h1kgkwj/Math_Solver_Sample_Images
