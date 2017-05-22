from __future__ import absolute_import, division, print_function, unicode_literals
from future import standard_library
from future.utils import bytes_to_native_str
standard_library.install_aliases()
from builtins import input
from builtins import object
import getpass

password_prompt = bytes_to_native_str(b"Password :")

print("Udacity Login required.")
email = input('Email :')
print(email)
password = getpass.getpass(password_prompt)
print(password)