import pyotp

def get_totp():
    totp = pyotp.TOTP("A4VYGB6CFOAZ77MGVPJMBIYHIP54KVJH") # Seed 2fa of account
    print("Current OTP:", totp.now()) # Get current 2fa code
    return totp.now()