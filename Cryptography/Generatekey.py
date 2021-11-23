from cryptography.fernet import Fernet

key = Fernet.generate_key()
file = open("encruption_key.txt", "wb")                  #This complete generates a key everytime we run the file
file.write(key)
file.close()