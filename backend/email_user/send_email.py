import json
from urllib import response
from sendgrid import sendgrid
import os
from sendgrid.helpers.mail import *
from dotenv import load_dotenv
from flask import jsonify
from secrets import token_urlsafe

load_dotenv()

class Send_Email:

    """
    forgotPasswordEmail function:
        sends an email to the user with their forgot password token
    parameters:
        email
    return:
        json response
    """
    def forgotPasswordEmail(email):
            sg = sendgrid.SendGridAPIClient(api_key = os.getenv('SENDGRID_API_KEY'))
            from_email = Email(os.environ.get('SENDGRID_EMAIL'))
            to_email = To(email)
            subject = "Forgot Password"
            site = "http://localhost:8100/forgot-password-password"
            rand = token_urlsafe(8)
            content = Content("text/html", '<div align="center" style="color: rgb(210, 4, 45); background-size: 100% 100%; background-repeat: no-repeat; background-image: url(\'https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2Femail_Background.png?alt=media&token=f72405e1-5607-47b6-957c-81cda3c94af5\');"><div><td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center"><img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:12% !important; width:12%; height:auto !important;" width="84" alt="" data-proportionally-constrained="true" data-responsive="true" src="https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2FJWE-logos_black.png?alt=media&token=4f64c15a-a0b6-4fbb-8dda-be74e7a45739"></td></div> <p>Token is: {}<p> <br><a href="{}""><button> Reset Password </button></a></div>'.format(rand, site))
            mail = Mail(from_email, to_email, subject, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            if(response.status_code == 202):
                  send = {'response': "email successfully sent", 'token': rand}
                  return send
            else:
                  return jsonify({'response': "email unsuccessfully sent"}), 401


    """
    forgotPasswordEmail function:
        sends an email to the user with their weekly progress
    parameters:
        email, score and username
    return:
        string response
    """
    def send_email(self, email, score, username):

        try:
            sg = sendgrid.SendGridAPIClient(api_key = os.getenv('SENDGRID_API_KEY'))
            from_email = Email(os.environ.get('SENDGRID_EMAIL'))
            to_email = To(email)
            subject = "Weekly Check-in from your favourite Japanese writing app"
            if(float(score) <= float(20)):
                  content = Content("text/html", '<div align="center" style="color: rgb(210, 4, 45); background-size: 100% 100%; background-repeat: no-repeat; background-image: url(\'https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2Femail_Background.png?alt=media&token=f72405e1-5607-47b6-957c-81cda3c94af5\');"><div><td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center"><img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:12% !important; width:12%; height:auto !important;" width="84" alt="" data-proportionally-constrained="true" data-responsive="true" src="https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2FJWE-logos_black.png?alt=media&token=4f64c15a-a0b6-4fbb-8dda-be74e7a45739"></td></div><h1 style="text-align: center;" "position: relative;">This week you scored: {}%</h1><h2 style="text-align: center">Keep going {}!</h2><br><p>Don\'t worry, you will get the hang of it soon.</p><h4>Come back onto the app and continue learning more characters and styles!</h4></div>'.format(round(score,2), username))
            elif(float(score) > float(20) and float(score) <= float(40)):
              content = Content("text/html", '<div align="center" style="color: rgb(210, 4, 45); background-size: 100% 100%; background-repeat: no-repeat; background-image: url(\'https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2Femail_Background.png?alt=media&token=f72405e1-5607-47b6-957c-81cda3c94af5\');"><div><td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center"><img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:12% !important; width:12%; height:auto !important;" width="84" alt="" data-proportionally-constrained="true" data-responsive="true" src="https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2FJWE-logos_black.png?alt=media&token=4f64c15a-a0b6-4fbb-8dda-be74e7a45739"></td></div><h1 style="text-align: center">This week you scored: {}%</h1><h2 style="text-align: center">Almost There {}!</h2><br><p>It\'s a steady climb, but we\'ll get to the top of the hill eventually</p><h4>Come back onto the app and continue learning more characters and styles!</h4></div>'.format(round(score,2), username))
            elif(float(score) > float(40) and float(score) <= float(60)):
              content = Content("text/html", '<div align="center" style="color: rgb(210, 4, 45); background-size: 100% 100%; background-repeat: no-repeat; background-image: url(\'https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2Femail_Background.png?alt=media&token=f72405e1-5607-47b6-957c-81cda3c94af5\');"><div><td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center"><img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:12% !important; width:12%; height:auto !important;" width="84" alt="" data-proportionally-constrained="true" data-responsive="true" src="https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2FJWE-logos_black.png?alt=media&token=4f64c15a-a0b6-4fbb-8dda-be74e7a45739"></td></div><h1 style="text-align: center">This week you scored: {}%</h1><h2 style="text-align: center">Good Work {}!</h2><br><p>Your progress is starting to show, keep up the good work!</p><h4>Come back onto the app and continue learning more characters and styles!</h4></div>'.format(round(score,2), username))
            elif(float(score) > float(60) and float(score) <= float(80)):
              content = Content("text/html", '<div align="center" style="color: rgb(210, 4, 45); background-size: 100% 100%; background-repeat: no-repeat; background-image: url(\'https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2Femail_Background.png?alt=media&token=f72405e1-5607-47b6-957c-81cda3c94af5\');"><div><td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center"><img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:12% !important; width:12%; height:auto !important;" width="84" alt="" data-proportionally-constrained="true" data-responsive="true" src="https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2FJWE-logos_black.png?alt=media&token=4f64c15a-a0b6-4fbb-8dda-be74e7a45739"></td></div><h1 style="text-align: center">This week you scored: {}%</h1><h2 style="text-align: center">Great Job {}!</h2><br><p>You have done exceptionally well this week, and I have to say, I didn\'t expect any less.</p><h4>Come back onto the app and continue learning more characters and styles!</h4></div>'.format(round(score,2), username))
            else:
              content = Content("text/html", '<div align="center" style="color: rgb(210, 4, 45); background-size: 100% 100%; background-repeat: no-repeat; background-image: url(\'https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2Femail_Background.png?alt=media&token=f72405e1-5607-47b6-957c-81cda3c94af5\');"><div><td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center"><img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:12% !important; width:12%; height:auto !important;" width="84" alt="" data-proportionally-constrained="true" data-responsive="true" src="https://firebasestorage.googleapis.com/v0/b/bug-slayers-jwe.appspot.com/o/email%2FJWE-logos_black.png?alt=media&token=4f64c15a-a0b6-4fbb-8dda-be74e7a45739"></td></div><h1 style="text-align: center">This week you scored: {}%</h1><h2 style="text-align: center">Outstanding {}!!!</h2><br><p>This week you have taken it to infinity and beyond. Keep reaching for the stars!</p><h4>Come back onto the app and continue learning more characters and styles!</h4></div>'.format(round(score,2), username))
            mail = Mail(from_email, to_email, subject, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)

            return "Email successfully sent" 
        except Exception as e:
            return "Failed"