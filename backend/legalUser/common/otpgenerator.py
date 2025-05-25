from random import randint

def createOTP():
    otpvalue = ""
    for _ in range(0,6):
        otpvalue += str(randint(0,9))
        
    return otpvalue
        
def verify_OTP_Template(otpvalue):
    html_content = f"""
            <html>
                <body>
                <img src= ""https://res.cloudinary.com/dwmujpiu9/image/upload/v1723810519/im4xa2jwkq3myfh77ygi.jpg"" width=100>
                <h1 style='color:#2A75EC'>Verify Your Account</h1>
                <p>To finish activating your Legal Assist account password, we just need to make sure this email address is yours.</p>
                <p>To verify your email address use this security code</p>
                <P style='font-size:20px; margin:0'><b>{otpvalue}</b></P>
                <p>If you didn't request this code, you can safely ignore this email. Someone else might have typed your email address by mistake.
                <p>Thanks,</p>
                <p>The Legal Assist Team</p>
                </body>
            </html>
            
            """
    return html_content

def account_status_update_template(role, status):
    # Determine the message based on role
    if role.lower() == "client":
        message = f"Your probono request has been <b>{status}</b>."
        heading = "Probono Status Update"
    elif role.lower() == "attorney":
        message = f"Your credentials have been <b>{status}</b>."
        heading = "Credential Status Update"
    else:
        message = f"Your account status has been updated to <b>{status}</b>."
        heading = "Account Status Update"

    html_content = f"""
        <html>
            <body>
                <img src="https://res.cloudinary.com/dwmujpiu9/image/upload/v1723810519/im4xa2jwkq3myfh77ygi.jpg" width=100>
                <h1 style='color:#2A75EC'>{heading}</h1>
                <p>{message}</p>
                <p>If you have any questions or believe this is a mistake, please contact support.</p>
                <p>Thanks,</p>
                <p>The Legal Assist Team</p>
            </body>
        </html>
    """
    return html_content

def request_received_template(role):
    # Determine the message based on role
    if role.lower() == "client":
        message = "Your request for probono approval has been received. Our team will review it shortly."
        heading = "Probono Request Received"
    elif role.lower() == "attorney":
        message = "Your request for credential verification has been received. Our team will review your documents and get back to you soon."
        heading = "Credential Verification Received"
    else:
        message = "Your request has been received. Our team will review and respond accordingly."
        heading = "Request Received"

    html_content = f"""
        <html>
            <body>
                <img src="https://res.cloudinary.com/dwmujpiu9/image/upload/v1723810519/im4xa2jwkq3myfh77ygi.jpg" width=100>
                <h1 style='color:#2A75EC'>{heading}</h1>
                <p>{message}</p>
                <p>If you have any questions, feel free to reach out to our support team.</p>
                <p>Thanks,</p>
                <p>The Legal Assist Team</p>
            </body>
        </html>
    """
    return html_content