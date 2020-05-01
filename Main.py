import requests
import pyaes
import base64


def get_paste_info(url, paste_request, encoding='utf-8'):
    paste_key = (url[paste_url.find('#') + 1:] + "=")  # Extract key from URL
    paste_key = base64.urlsafe_b64decode(paste_key)
    # encrypted_txt = The whole encrypted txt with iv, salt, ct embedded
    encrypted_txt_start_index = paste_request.text.find("<code>") + 6  # Skip <code>
    encrypted_txt_end_index = paste_request.text.find("</code>")
    encrypted_txt = paste_request.text[encrypted_txt_start_index: encrypted_txt_end_index]
    paste_iv = (encrypted_txt[encrypted_txt.find("iv") + 15: encrypted_txt.find("salt") - 13] + "=" * 2)
    paste_iv = base64.b64decode(paste_iv)
    paste_salt = encrypted_txt[encrypted_txt.find("salt") + 17: encrypted_txt.find("ct") - 13]
    paste_content = encrypted_txt[encrypted_txt.find("ct") + 15: -12]

    return paste_key, paste_iv, paste_salt, paste_content


paste_url = "https://0bin.net/paste/MmRuZ+t31fCEmrct#WgOX2xQT83vzV+0Qlq6JHV3Nenh3+tcXrJl86O9Afi1"

r = requests.get(paste_url)
key, iv, salt, content = get_paste_info(paste_url, r, encoding='utf-8')

aes = pyaes.AESModeOfOperationCTR(key)
decrypted_txt = aes.decrypt(content)
decrypted_txt = decrypted_txt.decode('utf-8')
print(r.status_code)
