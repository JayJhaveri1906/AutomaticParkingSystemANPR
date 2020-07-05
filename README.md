# AutomaticParkingSystemANPR

## Demo yt vid: - 
[Automatic Number Plate Recognition system - Automated Parking](https://www.youtube.com/watch?v=i64AUqCuKV8&feature=youtu.be)

## Steps to run: -
1) Download [THIS](https://drive.google.com/file/d/10lYoIKufiyKaw570UvLbRHbUY6YGYlht/view?usp=sharing) and add this to BackendPy folder.
2) Firebase Setup: -
   - Create a new project in firebase.
   - Add app android
   - Follow the steps given there. ( package name for this app `com.example.database`)
   - Create a new database( test mode )
   - Download the json file and use it to build a database on firebase.(import json option). It should then look something like this: -
![](images/database.png)
3) Android Stuff: -
  1. 
4) Install requirements.txt for the backend python part.
5) Install the app on phone/emulator.
6) TESSERACAT OCR STUFF TBD
7) Open video_final.py and on line number 235(with ui) or on 246(without ui) give path to a video or keep path = 0 to activate webcam( use a printed number plate )
  [Sample video](https://drive.google.com/file/d/1QL5nR2pNM71CKH2vehXpEgiqdH6SAAho/view?usp=sharing)
8) In the Advance(auth) button, select the floating button and add your number plate there.
9) To run without the PyQt5 ui directly run video_final.py and enter 1 for entry, then 0 for exit.
10) To run with ui, Run the design.py code.

## Team X Æ A-4
Jay Jhaveri: https://github.com/JayJhaveri1906

Prem Chhabria: https://github.com/premchhabria

Abhay Gupta: https://github.com/abhay8463

Sahil Lotya: https://github.com/sahillotya

Rahul Koli: https://github.com/rahul2429

Prasad Govekar: https://github.com/govekarmohit
