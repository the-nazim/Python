from cryptography.fernet import Fernet

key = "uxt1hzWaFwkG9Hd2LxBXIdHo2BdNcmYYX0dOVb-YsY0="

system_information_e = "e_sysinfo.txt"
clipboard_information_e = "e_clipbrd.txt"
keys_information_e = "e_keys_log.txt"

encrypted_file = [system_information_e, clipboard_information_e, keys_information_e]
count = 0

for decrypt_files in encrypted_file:
    with open(encrypted_file[count], 'rb') as f:
        data = f.read()
    
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_file[count], 'wb') as f:
        f.write(decrypted)
    
    count += 1

