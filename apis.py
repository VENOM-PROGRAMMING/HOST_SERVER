import requests
import hashlib
import time
import os
import json
from ftplib import FTP
from io import BytesIO

class AAPanelAPI:
    def __init__(self, key, url, domain, url_zip):
        self.key = key
        self.url = url
        self.domain = domain
        self.url_zip = url_zip

    def encrypt(self):
        return {
            'request_token': hashlib.md5((str(int(time.time())) + hashlib.md5(self.key.encode()).hexdigest()).encode()).hexdigest(),
            'request_time': int(time.time())
        }
    def http_post_cookie(self, url, data, timeout=60):
        cookie_file = './' + hashlib.md5(self.url.encode()).hexdigest() + '.cookie'
        if not os.path.exists(cookie_file):
            open(cookie_file, 'w').close()

        response = requests.post(url, data=data, cookies={'cookie_name': 'cookie_value'}, timeout=timeout)
        return response.text

    def logs(self):
        complete_url = self.url + '/data?action=getData&table=sites'
        data = self.encrypt()
        data['table'] = 'sites'
        data['limit'] = 50
        data['tojs'] = 'test'
        result = self.http_post_cookie(complete_url, data)
        return json.loads(result)
   
   
   
    def sites(self):
        complete_url = self.url + '/data?action=getData'
        data = self.encrypt()
        data['limit'] = 20
        data['p'] = 1
        data['type'] = -1
        data['order'] = 'id desc'
        data['tojs'] = 'get_site_list'
        data['search'] = 'www'
        result = self.http_post_cookie(complete_url, data)
        return json.loads(result)
   
    def delete(self,id, webname):
        print(id)
        print(webname)
        complete_url = self.url + '/site?action=DeleteSite'
        data = self.encrypt()
        data['id'] = id
        data['port'] = '80'
        data['webname'] = webname
        data['domain'] = webname
        data['ftp']= 1
        data['database']= 1
        data['path']= 1
        result = self.http_post_cookie(complete_url, data)
        print(result)
        return json.loads(result)
   
    
    
    def addSite(self,type='php', phpversion='80', port='80', ftp=None, ftpusername=None, ftppassword=None, sql=None, userdbase=None, passdbase=None, setSsl=0, forceSsl=0):
        complete_url = self.url + '/site?action=AddSite'
        type_id = 1
        datajson = {
            'domain': self.domain,
            'domainlist': [],
            'count': 0,
        }
        data = self.encrypt()
        data['webname'] = json.dumps(datajson)
        data['path'] = "/www/wwwroot/" + self.domain
        data['ps'] = self.domain
        data['type_id'] = type_id
        data['type'] = type
        data['version'] = phpversion
        data['port'] = port

        if ftp is not None:
            data['ftp'] = ftp
            data['ftp_username'] = ftpusername
            data['ftp_password'] = ftppassword
        if sql is not None:
            data['sql'] = sql
            data['datauser'] = userdbase
            data['datapassword'] = passdbase

        data['codeing'] = 'utf8'
        data['set_ssl'] = setSsl
        data['force_ssl'] = forceSsl

        result = self.http_post_cookie(complete_url, data)

        return json.loads(result)
    
    
    def unzip(self, sourceFile, destinationFile, password=None):
        complete_url = self.url + '/files?action=UnZip'
        data = self.encrypt()
        data['sfile'] = sourceFile
        data['dfile'] = destinationFile
        data['type'] = 'zip'
        data['coding'] = 'UTF-8'
        data['password'] = password
        result = self.http_post_cookie(complete_url, data)
        return json.loads(result)
    
    def add_file(self, ftp_address,ftp_port,username ,password):
        ftp = FTP()
        ftp.connect(ftp_address, ftp_port)
        ftp.login(username, password)
        contents = ftp.nlst()
        print("Conținutul directorului:")
        for item in contents:
            if self.domain.lower() == item.lower():
                print('Domain find in file.')
                ftp.cwd(item)
                contents = ftp.nlst()
                for item in contents:
                    try:
                        ftp.delete(item)
                        print(f"Fișierul {item} a fost șters.")
                    except Exception as e:
                        print(f"Eroare la ștergerea fișierului {item}: {e}")
                response_download = requests.get(self.url_zip, timeout=50)
                zip_content = response_download.content
                total_size = len(zip_content)
                name_zip = 'upload_pages.zip'
                with BytesIO(zip_content) as zip_file:
                    result = ftp.storbinary(f'STOR {name_zip}', zip_file)

                if 'successfully' in str(result):
                    print('Upload completed successfully')
                    result = self.unzip(sourceFile=f'/www/wwwroot/{self.domain}/{name_zip}', destinationFile=f'/www/wwwroot/{self.domain}/')
                    if 'status' in str(result):
                        if result['status']:
                            return True
                else:
                    print(result)
