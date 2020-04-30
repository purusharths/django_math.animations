def auth_token_message(firstname, lastname, activation_link, password_token):
    return ''' Dear {} {}, \n\n
    Greetings from FOSEE Animations (math).\n
    Your account has been created, you can activate it using the following link \n
    {} \n
    (If the abovementioned link does not work, please copy/paste it in your Web Browser).
    \n
    Upon activation you will be asked to change your password using the auth-token: {} \n
    You will then be able to log in with your email and password in order to use your account on the website.'''.format(firstname, lastname, activation_link, password_token)

def got_a_message(firstname, lastname, subtopic_name, from_user, message, messages_link):
    return """ Dear {} {}, \n\n
    You've recived a message for {} by {}. Please find the message below: \n\n
    {}\n\n_________________,_\n\n You can reply to this message at: {}""".format(firstname, lastname, subtopic_name, from_user, message, messages_link)

def submission_status_changed(firstname, lastname, subtopic, submission_status, message_link, submission_link, view_topic):
    return """Dear {} {}\n\n
    The status for your submission {} has been changed to {} \n
    Please go through the recent messages for more details: {}.\n\n
    Submission Link: {}""".format(firstname, lastname, subtopic, submission_status, message_link, submission_link)