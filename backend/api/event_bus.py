from functools import partial
from urllib import response
from admin import Admin

from flask import jsonify
from authentication import Authentication

import sys
sys.path.insert(0, '../database')
sys.path.insert(1, '../email_user')
from send_email import Send_Email
import base64
import json
from database import Database
from image import Image
from evaluator import Evaluator
from imageDB import imageDB

db = Database()
auth = Authentication(db)
img = Image()
imagedb = imageDB(db)
admin = Admin(db)
eventBus = []

def executeBus(event_number):
    res = eventBus[event_number]()
    del eventBus[event_number]
    return res

def event_resetPassword(email):
    eventBus.append(partial(auth.findUser, email))
    event_number = len(eventBus) - 1
    response = executeBus(event_number)
    if(response[1] == 200): #returns a tuple, element at 1 is the status code
        email_res = event_forgotPasswordEmail(email)
        tokenStore = event_storeToken(email, email_res["token"])
        if(tokenStore[1] != 200):
            return jsonify({'response': "Forgot password token unsuccessfully set"}), 401
        return email_res
    else:
        return response
    
def event_storeToken(email, token):
    eventBus.append(partial(auth.addToken, email, token))
    event_number = len(eventBus) - 1
    return executeBus(event_number)

def event_forgotPasswordEmail(email):
    eventBus.append(partial(Send_Email.forgotPasswordEmail, email))
    event_number = len(eventBus) - 1
    return executeBus(event_number)

def event_changePassword(token, password):
    eventBus.append(partial(auth.resetPassword, token, password))
    event_number = len(eventBus) - 1
    return executeBus(event_number)
        

def event_register(email, password, username):
    eventBus.append(partial(auth.register, email, password, username))
    event_number = len(eventBus) - 1
    return executeBus(event_number)

def event_uploadImage(id, imagechar, image, file):
    eventBus.append(partial(Image.uploadImage, img, id, imagechar, image, file))
    event_number = len(eventBus) - 1
    return jsonify(executeBus(event_number))

def event_sendImage(id, image_char, image, file, writing_style):
    e = Evaluator(writing_style, image_char)
    feedback = e.testCharacter() # call AI
    score = feedback[1]
    if(score == 0):
        return jsonify({'response': "image evaluation failed."}), 401
    else:
        exitcode = event_uploadImage(id, image_char, image, file)
        if(exitcode.status_code == 200):
            storeToDB = event_saveToDB(id, file, image_char, score, writing_style)
            if(storeToDB == True):
                strokes = feedback[0]
                return jsonify({'response': "image upload successful", 'data': {'stroke1' : strokes[0], 'stroke2': strokes[1], 'stroke3': strokes[2],'score': score}}), 200
            else:
                return jsonify({'response': "Database storage failed"}), 401
        else:
            return jsonify({'response': "Storage to cloud service failed"}), 401

def event_viewImages(id):
    eventBus.append(partial(imagedb.getImages, id))
    event_number = len(eventBus) - 1
    images = executeBus(event_number)
    code = jsonify(images).status_code
    if(code == 200):
        eventBus.append(partial(Image.viewImages, img, images))
        event_number2 = len(eventBus) - 1
        return executeBus(event_number2)
    else:
        return jsonify({"response": "User image retrieval from database failed"}), 401

def event_sendToEvaluator(image, image_char):
    obj = Evaluator(image, image_char)
    eventBus.append(partial(obj.testCharacter, image, image_char))
    event_number = len(eventBus) - 1
    return executeBus(event_number)

def event_saveToDB(id, file, image_char, score, writing_style):
    eventBus.append(partial(imagedb.saveToDB, id, file, image_char, score, writing_style))
    event_number = len(eventBus) - 1
    return executeBus(event_number)

def event_getImageUsers():
    eventBus.append(partial(imagedb.getImageUsers))
    event_number = len(eventBus) - 1
    return executeBus(event_number)

def event_getUser(id):
    eventBus.append(partial(imagedb.getUser, id))
    event_number = len(eventBus) - 1
    return executeBus(event_number)

def event_login(email, password):
    eventBus.append(partial(auth.login, email, password))
    event_number = len(eventBus) -  1
    status = executeBus(event_number)
    print(status)
    if(status != None):
        return status
    else:
        return None

def event_getCharacters():
    eventBus.append(partial(img.getCharacters))
    event_number =  len(eventBus) - 1
    return executeBus(event_number)

def eventListUsers(id):
    eventBus.append(partial(auth.listUsers, id))
    event_number = len(eventBus) - 1
    return executeBus(event_number)

def event_editUserPrivileges(id, ad):
    eventBus.append(partial(admin.editUserPrivileges, id, ad))
    event_number = len(eventBus) - 1
    status = executeBus(event_number)
    if(status != None):
        return status
    else:
        return None
    
def event_listModelData():
    eventBus.append(partial(admin.listModelData))
    event_number = len(eventBus) - 1
    status = executeBus(event_number)
    if(status != None):
        return status
    else:
        return None
   
def eventViewModelData(version):
    eventBus.append(partial(admin.viewModelData, version))
    event_number = len(eventBus) - 1
    status = executeBus(event_number)
    if(status != None):
        return status
    else:
        return None
     
"""
guest Upload Image function:
    uploads the given image to firebase and sends it to the evaluator
parameters: 
    image_char: the charector of the image
    image: the guest user image
return:
    json response
"""
def event_guestUplaodImage(imagechar, image, style):
    image = image.partition(",")[2]
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.b64decode(image))
        
    e = Evaluator(style, imagechar)
    feedback = e.testCharacter() # call AI
    score = feedback[1]
    if score == 0:
        return jsonify({'response': "image evaluation Failed."}), 401
    else:
        strokes = feedback[0]
        return jsonify({'response': "image upload successful", 'data': {'stroke1' : strokes[0], 'stroke2': strokes[1], 'stroke3': strokes[2],'score': score}}), 200
