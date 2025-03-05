import pyotp

def get_totp():
    totp = pyotp.TOTP("XZ6WMQW2RRWPR67DBLSMBJ2MASAUJ23G") # Seed 2fa of account
    print("Current OTP:", totp.now()) # Get current 2fa code
    return totp.now()