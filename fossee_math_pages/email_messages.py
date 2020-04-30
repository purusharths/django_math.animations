def auth_token_message(firstname, lastname, username, activation_link, password_token):
    subject = "[Activate Account] FOSSEE Animations Mathematics"
    message = "activate_user.html"
    return subject, message

def got_a_message(firstname, lastname, subtopic_name, from_user, message, messages_link):
    subject = "[FOSSEE Animations | Math] New Message Recived"
    message = """Dear {} {}, \n\n
    You have recived a message for {} by {}. Please find the message below: \n\n
    {}\n\n
    __________________\n\n You can reply to this message at: {}""".format(firstname, lastname, subtopic_name, from_user, message, messages_link)
    return subject, message

def submission_status_changed(firstname, lastname, subtopic, submission_status, message_link, submission_link):
    subject = "[Submission Update] Submission Status changed at FOSSE Animations | Math"
    message = """Dear {} {}\n\n
    The status for your submission {} has been changed to {} \n
    Please go through the recent messages for more details: {}.\n\n
    Submission Link: {}""".format(firstname, lastname, subtopic, submission_status, message_link, submission_link)
    return subject, message
