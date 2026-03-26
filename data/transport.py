transport = {
    ("Tana", "Nosy Be"): {"cout": 50, "duree": 0.5},
    ("Tana", "Andasibe"): {"cout": 20, "duree": 0.5},
    ("Nosy Be", "Andasibe"): {"cout": 60, "duree": 1},
}

for (v1, v2), val in list(transport.items()):
    transport[(v2, v1)] = val