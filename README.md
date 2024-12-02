Install the required packages:
Python 3.9.6
pip
imagehash
Pillow
requests==2.32.3
pytesseract


DB:
sqlite3

To Run:
Execute the code with the command "python main.py". 
The camera will be turned on; press "S" on your keyboard to capture the image. It will be stored the imges in captured_images and and create a json in events_data.json. 
The JSON data will be compared with the database data and will indicate any duplicates or threats. Duplicates will not be stored in the database.
Note: It can identify face and liscence plate(accuracy might be low somtimes).If neither the face nor the license plate detected, it will consider the image as unknown.

Use the command uvicorn server:app --reload to start the server