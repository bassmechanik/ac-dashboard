# Assetto Corsa Arduino LC-Display Dashboard

This piece of software provides the ability to connect an Arduino attached with a LC-Display-Shield to display some game relevant informations in real time. This project is currently in it's very beginning. The software needs refactoring that will probably happen within the next months. 


## Python

This library already comes with an pySerial version which is required to communicate with the Arduino. To run the Assetto Corsa phyton app you just have to add the whole **ArduinoDash** folder to your Assetto Corsa installation which can be found in your Steam installation under */Steam/SteamApps/common/assettocorsa/apps/python*

You have to configure the right COM-port on your PC. Otherwise the app will crash until it tries to connect again on the next start of a race. 
