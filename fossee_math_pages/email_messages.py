#Email handling
def auth_token_message(firstname, lastname, username, activation_link, password_token):
    subject = "[Activate Account] FOSSEE Animations Mathematics"
    message = "activate_user.html"
    return subject, message

#Function for message check
def got_a_message(firstname, lastname, subtopic_name, from_user, message, messages_link):
    subject = "[FOSSEE Animations | Math] New Message Recived"
    message = """Hey {}, {} \n\n
    You have recived a message for "{}" by {}. Please find the message below: \n
    ____________________
    \n
    {}
    \n
    ____________________\n\n You can reply to this message at: {}
    \n
    Best Regards,
    FOSSEE Animations Team""".format(firstname, "", subtopic_name, from_user, message, messages_link)
    return subject, message

#submission status message
def submission_status_changed(firstname, lastname, subtopic, submission_status, message_link, submission_link):
    subject = "[Submission Update] Submission Status changed at FOSSE Animations | Math"
    message = """Hey {}, {}\n\n
    The status for your submission "{}" has been changed to "{}" \n
    Please go through the recent messages for more details: {}.\n\n
    Submission Link: {}\n
    Best Regards,
    FOSSEE Animations Team""".format(firstname, "", subtopic, submission_status, message_link, submission_link)
    return subject, message

#topic assignation message
def topic_assigned(firstname, lastname, topic_name, submission_url):
    subject = "[Topic Assigned] A new topic has been assigned to You"
    message = """Hey {}, {}\n\n
    You have been assigned a new topic: {}\n
    To can start editing your submissions by clicking here: {}

    Best Regards, 
    FOSSEE Animations Team""".format(firstname, "", topic_name, submission_url)
    return subject, message
