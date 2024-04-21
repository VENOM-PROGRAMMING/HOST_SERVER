from flask import Flask, render_template, request, jsonify
import requests
import os
import random
from apis import AAPanelAPI

app = Flask(__name__, static_folder='static')

@app.route('/admin')
def index():
    return render_template('admin.html')


@app.route('/')
def login():
    return render_template('login.html')

headers = {
        'Content-Type': 'application/json',
        'X-Auth-Email': 'QuirinaRoskop1964@brazilmail.com',
        'X-Auth-Key': '6ba829957601b260632c8638174bd99aa37fb'
}


aaPanelApi = 'gOPbM0PJ5zttC8SwlxEtG1oNzq5Ju4ip'
aaPanelHost = 'http://93.123.39.14:21070'

aaPanelFTP_host = "93.123.39.14"
aaPanelFTP_username = "dadadadada"
aaPanelFTP_port = 21
aaPanelFTP_password = 'WxHtiZiTcpLphxKD'

cloudflare_account_id = '32d3cce87efcd6cff1186f3aa8fb1ea3'





@app.route('/add_domain/<string:domeniu>', methods=['GET'])
def add_domain(domeniu):
    endpoint = 'https://api.cloudflare.com/client/v4/zones'
    
    data = {
        'account': {'id': cloudflare_account_id},
        'name': domeniu,
        'type': 'full'
    }
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
            print(f'Domeniul {domeniu} a fost adăugat cu succes!')
            return response.json()
    else:
        return response.json()
    




@app.route('/update_dns/<string:domeniu>/<string:ip>/<string:type>', methods=['GET'])
def update_dns(domeniu, ip,type):
    endpoint = 'https://api.cloudflare.com/client/v4/zones'
    response = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers)
    if response.status_code == 200:
        # return response.json()
        for res in response.json()['result']:
            if domeniu == res['name']:
                zone_id = res['id']
                json_data = {
                    'content': ip,
                    'name': type,
                    'proxied': True,
                    'type': 'A',
                    'ttl': 3600,
                }
                response = requests.post(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records', headers=headers, json=json_data)
                if response.status_code == 200:
                    return response.json()
                else:
                    return f'{domeniu}: {response.text}'
        return f'Domain not found'
    else:
        return f'SERVER ERROR: {response.status_code}'

    
    
@app.route('/check_ua/<string:domeniu>', methods=['GET'])
def check_ua(domeniu):
    response = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers)
    if response.status_code == 200:
        # return response.json()
        for res in response.json()['result']:
            if domeniu == res['name']:
                zone_id = res['id']
                response = requests.get(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/security_level', headers=headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    return f'{domeniu}: {response.text}'
        return f'Domain not found'
    else:
        return f'SERVER ERROR: {response.status_code}'

    
    
    
@app.route('/set_ua/<string:domeniu>/<string:sets>', methods=['GET'])
def set_ua(domeniu,sets):
    response = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers)
    data = {
        "value": sets
    }
    if response.status_code == 200:
        # return response.json()
        for res in response.json()['result']:
            if domeniu == res['name']:
                zone_id = res['id']
                print(zone_id)
                response = requests.patch(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/security_level',json=data, headers=headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    return f'{domeniu}: {response.text}'
        return f'Domain not found'
    else:
        return f'SERVER ERROR: {response.status_code}'
    

@app.route('/delete_all_dns/<string:domeniu>', methods=['GET'])
def delete_all_dns(domeniu):
    response = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers)
    if response.status_code == 200:
        
        for res in response.json()['result']:
            if domeniu == res['name']:
                zone_id = res['id']
                response = requests.get(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records', headers=headers)
                if response.status_code == 200:
                    if len(response.json()["result"]) > 0:
                        p = []
                        for x in response.json()["result"]:
                            dns_record_id = x['id']
                            zone_id = x['zone_id']
                            response = requests.delete(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}', headers=headers)
                            p.append(response.json())
                        return jsonify({'data': p})
                    else:
                        return jsonify({'data': True})
    



@app.route('/get_domain_info/<string:domeniu>', methods=['GET'])
def domain_info(domeniu):                        
    response = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers)
    if response.status_code == 200:
        domain_found = False
        # return response.json()
        for res in response.json()['result']:
            if domeniu == res['name']:
                domain_found = True
                return jsonify({'data': res})
        
        if not domain_found:
            return jsonify({'message': 'Domeniul nu a fost gasit.'}), 404
    else:
        return jsonify({'message': 'Eroare la obtinerea zonelor: ' + response.text}), response.status_code




@app.route('/all_domain', methods=['GET'])
def all_domain():                        
    response = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers)
    if response.status_code == 200:
        return jsonify({'data': response.json()['result']})
    else:
        return jsonify({'message': 'Eroare la obtinerea zonelor: ' + response.text}), response.status_code






@app.route('/delete_domain/<string:domeniu>', methods=['GET'])
def delete_domain(domeniu):                        
    response = requests.delete(f'https://api.cloudflare.com/client/v4/zones/{domeniu}', headers=headers)
    if response.status_code == 200:
        return jsonify({'data': response.json()['result']})
    else:
        return jsonify({'message': 'Eroare la obtinerea zonelor: ' + response.text}), response.status_code


@app.route('/add_site', methods=['POST'])
def add_site():
    domain = request.form.get('domain')
    zip_url = request.form.get('zip_url')
    url_zip = zip_url
    api = AAPanelAPI(key=aaPanelApi, url=aaPanelHost, domain=domain, url_zip=url_zip)
    
    
    result = api.addSite(type='php', phpversion='80', port='80', ftp=True, ftpusername='admin1', ftppassword='admin1', sql=True, userdbase='admin1', passdbase='admin1', setSsl=1, forceSsl=0)
    if 'siteStatus' in str(result):
        if result['siteStatus']:
            result = api.add_file(aaPanelFTP_host, aaPanelFTP_port, aaPanelFTP_username, aaPanelFTP_password)
            return jsonify(result)
        else:
            return jsonify({'error': 'Failed to add site'})
    else:
        return jsonify({'error': result['msg']})




@app.route('/checksite', methods=['GET'])
def checksite():
    api = AAPanelAPI(key=aaPanelApi, url=aaPanelHost, domain=None, url_zip=None)
    result = api.logs()
    return jsonify(result)


@app.route('/delete/<string:id>/<string:names>', methods=['GET'])
def delete(names, id):
    api = AAPanelAPI(key=aaPanelApi, url=aaPanelHost, domain=None, url_zip=None)
    result = api.delete(names, id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3030)
    
