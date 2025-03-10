import sys

import pyotp

def get_totp():
    totp = pyotp.TOTP("DKLXV462Z2VUQARWLJ4CEG2DGBJDGQBP") # Seed 2fa of account
    print("Current OTP:", totp.now(), flush=True) # Get current 2fa code
    sys.stdout.flush()
    return totp.now()