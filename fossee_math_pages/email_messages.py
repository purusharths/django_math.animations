'''
def auth_token_message(firstname, lastname, val):
    return ''' Dear {} {}, \n\n
               Greetings from FOSEE Animations (math).\n
               Your account has been created, it will be activated when you click on the following link \n
               {} \n
               (If the abovementioned link does not work, please copy/paste it in your Web Browser).
               \n
               Upon activation you will be asked to change your password using the auth-token: {} \n
               You will then be able to log in with your email and password in order to use your account on the website.

                '''.format(firstname, lastname, activation_link)



send_mail(auth_token_message(abc))

send_mail(
            'FOSSEE ANIMATION MATH',
            'Thank you for registering with fossee_math. Your password is ' + passwordstr,
            'fossee_math',
            [email, 'fossee_math@gmail.com'],
            fail_silently=True, )
'''