import zwsp_steg
encoded = open('2.html').read()
decoded = zwsp_steg.decode(encoded)

print(decoded)  # hidden message