import requests
import json
import numpy as np
from numpy.linalg import norm

base = "http://52.138.31.212:8080/embed/"

def cosim(original, modified):
    r1 = requests.get(base + original)
    r2 = requests.get(base + modified)
    j1 = json.loads(r1.content)
    j2 = json.loads(r2.content)

    return np.inner(j1, j2) / (norm(j1) * norm(j2))


t1 = "I love hotdogs."
t2 = "I enjoy pizza."
t3 = "Burger is my favourite food."

print(cosim(t1, t2))
print(cosim(t1, t3))
print(cosim(t2, t3))