# Python dependencies
import string
import random
import re

# Generates a UID of 8 characters
def generate_uid():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


# Slugifies a script name (e.g. "Simon's script" -> "simons-script")
def for_uid(s):
    s = s.lower()
    for c in [" ", "-", ".", "/"]:
        s = s.replace(c, "_")
    s = re.sub("\W", "", s)
    s = s.replace("_", " ")
    s = re.sub("\s+", " ", s)
    s = s.strip()
    s = s.replace(" ", "-")

    return s
