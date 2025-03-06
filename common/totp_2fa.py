import pyotp

def get_totp():
    totp = pyotp.TOTP("DKLXV462Z2VUQARWLJ4CEG2DGBJDGQBP") # Seed 2fa of account
    print("Current OTP:", totp.now()) # Get current 2fa code
    return totp.now()