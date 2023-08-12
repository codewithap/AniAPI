try:
  from Cryptodome.Util.Padding import pad
  from Cryptodome.Cipher import AES
except:
  from Crypto.Util.Padding import pad
  from Crypto.Cipher import AES
from utils.useragents import useragent
from bs4 import BeautifulSoup
import base64
import requests
import json

key = b'37911490979715163134003223491201'
second_key = b'54674138327930866480207815084989'
iv = b'3134003223491201'

def request_headers():
  headers = {"User-Agent" : useragent()}
  return headers


def get_video_id(url):
  data = requests.get(url,headers=request_headers())
  html = BeautifulSoup(data.text,"html.parser")
  return html.select_one("script[data-name='episode']")["data-value"]

def unpad(data):
  padding_len = data[-1]
  return data[:-padding_len]

def urlParser(url): 
  protocol = url.split("://")[0]
  urldict = {
    "protocol" : protocol,
    "hostname" : url.strip(protocol+"://").split("/")[0],
    "params" : [{ x.split("=")[0] : x.split("=")[1]} for x in url.split("?")[1].split("&")]
  }
  return urldict

def generate_encrypted_parameters(url):
  urlDict = urlParser(url)
  url1 = f"{urlDict['protocol']}://{urlDict['hostname']}/streaming.php?id={urlDict['params'][0]['id']}" 
  vid_id = url.split("?")[1].split("&")[0].split("=")[1]
  cipher_key = AES.new(key, AES.MODE_CBC, iv)
  padded_key = pad(vid_id.encode(), AES.block_size)
  encrypted_key = cipher_key.encrypt(padded_key)
  encoded_key = base64.b64encode(encrypted_key).decode()
  script = get_video_id(url1)
  decoded_script = base64.b64decode(script)
  cipher_script = AES.new(key, AES.MODE_CBC, iv)
  decrypted_script = unpad(cipher_script.decrypt(decoded_script))
  token = decrypted_script.decode()
  encrypted_params = f"id={encoded_key}&alias={vid_id}&{token}"
  return encrypted_params

def decrypt_encrypted_response(response_data):
  decoded_data = base64.b64decode(response_data)
  cipher = AES.new(second_key, AES.MODE_CBC, iv)
  decrypted_data = cipher.decrypt(decoded_data)
  unpadded_data = unpad(decrypted_data)
  decrypted_text = unpadded_data.decode('utf-8')
  return decrypted_text

def getM3u8(iframeUrl):
  urldict = urlParser(iframeUrl)
  USER_AGENT = request_headers()["User-Agent"]
  encrypted_params = generate_encrypted_parameters(iframeUrl)
  request_url = f"{urldict['protocol']}://{urldict['hostname']}/encrypt-ajax.php?{encrypted_params}"
  headers = {"User-Agent" : USER_AGENT,"X-Requested-With": "XMLHttpRequest"}
  response = requests.get(request_url,headers = headers)
  decryptedJson = decrypt_encrypted_response(response.json()["data"])
  return json.loads(decryptedJson)
