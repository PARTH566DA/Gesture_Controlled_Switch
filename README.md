# **Gesture-Controlled Switch**
---

## **Project Overview**
<p align="justify">
This project focuses on creating a gesture-controlled switch, enabling users to turn an
appliance on or off with specific hand, leg or head movements. This system uses an
MPU6050 gyroscope sensor to detect hand gestures and two ESP32 microcontrollers,
one to process the input and the other to control a relay switch.
The system captures motion data from the gyroscope sensor attached to the user's
hand, processes it using the ESP32 microcontroller, and translates the data into
meaningful gestures such as "clockwise" or "anticlockwise" rotation. These gestures
serve as commands to activate or deactivate electrical appliances by controlling the
relay module which is controlled by another ESP32 microcontroller. The relay module
allows or interrupts current flow based on the interpreted gesture, ensuring reliable
operation.
</p>

---

## **Implementation and Execution**

### **1. Component Setup**

<p align = 'justify'>The MPU6050 gyroscope sensor was interfaced with the ESP32
microcontroller to capture motion data. The sensor collects 128 data
points, including acceleration (x, y, z) and gyroscope data (x, y, z), at a
frequency of 64 Hz. These data points are processed to extract key
features such as mean, max, min, energy, median, and entropy, which are
essential for gesture classification.</p>

<p align = 'justify'> A relay module was integrated into the system to simulate the control of
appliances such as a bulb or fan, enabling practical demonstration of the
project’s utility. The entire setup was powered by a lithium-ion battery,
ensuring portability and ease of use. For testing, the components were
securely mounted on a general-purpose board, offering a stable
configuration.</p>
   
### **2. Coding**

<p align = 'justify'>
An algorithm was implemented on the ESP32 to handle real-time data
collection and feature extraction from the gyroscopic sensor. The
processed feature set was transmitted to a Flask server hosted on a local
network via POST requests.
</p>

<p align = 'justify'>
  The Flask server, developed in Python, utilized a trained Random Forest
machine learning model stored as a serialized pickle file. Upon receiving
the feature data, the server processed it through the model to predict the
corresponding gesture.
</p>

<p align = 'justify'>
A second ESP32 microcontroller acted as the receiver. It sent GET
requests to the Flask server to retrieve the predicted gesture. Based on
the gesture received, this ESP32 controlled an electric relay to manage
connected appliances, such as turning a bulb or fan on or off. This
approach ensures seamless, gesture-based control of devices.
</p>

### **3. Testing**
- **MPU6050 Sensor:** Verified accurate detection of complex movements.  
- **Feature Extraction:** Ensured meaningful feature computation.  
- **Network Communication:** Tested reliable data transfer via POST/GET requests.  
- **ML Model Validation:** Validated gesture classification accuracy using test datasets.  
- **Relay Module:** Confirmed accurate responses to ESP32 commands.

---

## **Key Features**
- **Assistive Device:** Helps physically challenged individuals control appliances effortlessly.  
- **Energy Efficiency:** Powered by a rechargeable lithium-ion battery.  
- **Scalability:** Potential for expansion into full home automation systems.

---

## **Scope for Improvement**
1. **Multiple Gesture Support:** Recognize a broader range of gestures for versatile control.  
2. **Enhanced User Interface:** Improve usability without needing mobile devices or traditional switches.  
3. **Startup Potential:** Incorporate features like voice control, compact design, and refined performance.

---

## **How to Run?**
<p align = 'justify'>
To set up and run the system, start by hosting the Flask server on your device by running the "server.py" file. Next, configure and upload the code to the ESP32 devices. For the client-side ESP32, upload the code from "client_esp.txt", and for the receiver-side ESP32, upload the code from "receiver_esp.txt". Before uploading, ensure you have entered the specific Wi-Fi SSID, password, and the IP address of your network in both ESP32 programs. Finally, make sure your device running the Flask server and both ESP32 devices are connected to the same network for seamless communication.
</p>

## **Contributors**
[Parth Bhatt](https://github.com/PARTH566DA)

[Dhruv Gohil](https://github.com/Dhruvgohil07)
