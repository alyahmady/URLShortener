"""
! IMPORTANT

This script is not a part of project structure

Here's just a test lab to approve mistakes or take time benchmarks or ...

"""

import random
import secrets
import string
import time

characters = string.ascii_letters + string.digits

count = 10000000


# Faster than random string generation
# On average, 1 in 10,000,000 would not be unique which cause a re-process on DB
def secrets_token_generation():
    start = time.time()
    data = [
        secrets.token_urlsafe(6).replace("_", "").replace("-", "") for _ in range(count)
    ]
    duplicate_count = len(data) - len(set(data))
    end = time.time()
    return (end - start), duplicate_count


def random_string_generation():
    start = time.time()
    data = [
        "".join(random.choice(string.ascii_letters + string.digits) for i in range(8))
        for _ in range(count)
    ]
    duplicate_count = len(data) - len(set(data))
    end = time.time()
    return (end - start), duplicate_count


print(secrets_token_generation())
print(random_string_generation())
