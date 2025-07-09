Welcome to EmotIQ! 
EmotIQ – Brainwave Emotion Recognition Team 
We are developing an AI system that understands human emotions from brainwaves using machine learning and EEG signal analysis.
“Where Emotion Meets Intelligence”
## 🔗 External Files (Google Drive)

Due to GitHub file size limits, please download the following files manually:
[Download Emotion_Detection.h5](https://drive.google.com/file/d/1I_jukVYBF5CjJiKszI_7_J3MV6xjlb_O/view?usp=drive_link)
[Download fer2013.csv](https://drive.google.com/file/d/127d9TDp6zt7KsBIDEOAXOmgKVPoTk_NX/view?usp=drive_link)
➡️ After downloading, place the files in the project folder:

Team Member:👩‍💻
Souriya Sultana(C223212)
Umama Morshed(C223220)
Tasnim Showkat Diba(C223225)


✒️Project Description:

EmotIQ is a deep learning-based emotion detection system that leverages computer vision to
recognize and classify human emotions in real-time using a webcam. It utilizes a Convolutional
Neural Network (CNN) trained on the FER2013 dataset to detect key facial expressions.
Emotions such as 'Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral' are accurately
identified through facial landmarks and patterns.
The system is lightweight, user-friendly, and capable of running on standard hardware.
Applications range from mental health tracking to smart surveillance and interactive assistants.
By providing instant emotional feedback, EmotIQ enhances human-computer interaction.
Its real-time response makes it ideal for live monitoring environments.


✒️Objectives:

 To detect and classify human emotions from facial expressions using image data.
 To build and train a CNN model for high-accuracy real-time emotion classification.
 To integrate OpenCV for live face detection and classification via webcam.
 To preprocess facial images effectively for consistent input to the model.
 To visualize and display detected emotions on-screen in real-time.
 To support multiple emotion classes including 'Angry', 'Disgust', 'Fear', 'Happy', 'Sad',
'Surprise',’Surprise’
 To evaluate model performance using metrics like accuracy and loss on test data.
 To create a user-friendly interface for monitoring emotions without technical barriers.
 To test system responsiveness under different environmental conditions (lighting,
distance).
 To explore use cases in mental health monitoring, customer service, and smart
systems

✒️Software Requirements:

Python 3.x – Programming language
TensorFlow/Keras – Deep learning framework
OpenCV – Face detection and webcam integration
Pandas, NumPy – Data preprocessing
Matplotlib – Optional, for visualization
FER2013 Dataset – Training data


✒️Features :

The EmotIQ system includes several cutting-edge features that enable real-time emotion
detection using facial expressions. These features make it applicable in AI systems requiring
emotional awareness and user engagement.

 Real-Time Emotion Detection
The model uses the webcam feed to detect and classify human emotions on the fly. As
soon as a face is detected, it processes the facial region and displays the corresponding
emotion label

 Deep Learning-Based CNN Model
EmotIQ uses a Convolutional Neural Network (CNN) trained on the FER2013 dataset,
a benchmark dataset for facial expression recognition. The model is built using Keras
with TensorFlow backend, ensuring robust and accurate performance.

 Automatic Face Detection
OpenCV's Haar Cascade classifier is used to detect faces in real-time. This ensures that
only the relevant portion (Region of Interest - ROI) is fed to the emotion classifier.

 Five Emotion Categories
The model classifies emotions into five key categories:
 'Angry',
 'Disgust',
 'Fear',
 'Happy',
 'Sad',
 'Surprise',
 'Neutral'
These emotions are commonly used in affective computing and user mood analysis.

 Graphical Display:
The system overlays bounding boxes on detected faces and displays the predicted
emotion on the video feed, offering a clear and visual representation of the analysis.

 Fail-Safe Message Handling
When no face is detected in the camera view, the application displays a "No Face
Found" message instead of crashing or giving false predictions.

 User-Friendly and Lightweight
EmotIQ runs directly from the terminal using python test.py, making it simple and
accessible for testing or integration with larger systems.


✒️Purpose:

The primary purpose of the EmotIQ – Brainwave Emotion Recognition system is to create an
interactive tool that can understand and respond to human emotional states using facial
expressions. In today’s digital world, emotion-aware systems are increasingly important across
various domains:
 Human-Computer Interaction (HCI):
Emotion detection enhances user experience by allowing machines to react appropriately
to users’ emotional states.

 Mental Health Monitoring:
Real-time emotion tracking helps therapists and AI-driven mental health platforms
monitor users for signs of depression, stress, or anxiety.

 Educational Environments:
In e-learning, the tool can track student emotions like confusion or boredom, helping
educators adjust their teaching strategies.

 Marketing and User Feedback:
Understanding customer reactions while they interact with products or ads can help
companies optimize their content and strategy.

 Smart Surveillance Systems:
Detecting anger or fear in public settings can trigger alerts in security systems to prevent
conflicts or crimes.

 AI-Powered Chatbots and Assistants:
By recognizing the user's mood, digital assistants can respond more naturally and
empathetically.


✒️Output:

During execution (python test.py):
 The webcam window opens.
 The system detects faces in real-time.
 For each face detected, it displays a rectangle and the predicted emotion label.
 If no face is detected, it shows “No Face Found”.
 You can exit the application by pressing 'q' .
Example:
Detected: Happy 😄
Detected: Sad 😢
Detected: Surprise 😲


✒️Conclusion:

The EmotIQ project successfully implements a real-time facial emotion recognition system
using CNNs and OpenCV. It classifies five basic emotions with considerable accuracy. With
further improvements like data augmentation, facial landmarks, and more emotion classes, it
can be integrated into advanced AI systems, providing machines with emotional intelligence.


📌📌Contributors and Roles:

🏷[C223212-Souriya Sultana]-
Data Scientist & Model Trainer

Collected and preprocessed EEG and facial emotion datasets (e.g., FER-2013)

Trained and evaluated machine learning models

Tuned hyperparameters and improved model accuracy

Contributed to performance analysis and result validation

🏷[C223220-Umama Morshed]- 
Hardware & Integration Specialist

Handled EEG device setup and signal acquisition

Connected hardware with the software pipeline

Conducted system testing, debugging, and validation

Assisted in documentation and presentation design

🏷[C223225-Tasnim Showkat Diba]-
Project Lead & AI Developer

Designed the overall system architecture

Developed the emotion recognition model using CNN

Implemented face detection using Haar Cascade and real-time processing

Managed integration of EEG signal analysis

 ***Integrate CNN-based emotion detection with real-time EEG and face input details:

  Added face detection using Haar Cascade

  Connected trained CNN model (Emotion_Detection.h5) for emotion classification

  Integrated real-time EEG input with emotion prediction

  Displayed predicted emotion labels on webcam feed

  Verified accuracy with sample inputs


This project is all about identifying the real emotions by a trained AI model. Hope this project will waork and bring satisfaction.
Thank you.





