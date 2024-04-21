<div align="center">
  <img src="https://www.thestoryoftexas.com/upload/images/events/movies/venomwisp-banner.png">
</div>
# Welcome to HOST SERVER


##  :tangerine: Features


## Installation

To install the current release of HOST SERVER, please follow of the method described below.


## 1. CREATE CLOUDLFARE AND GET 

```shell
X-Auth-Email
```
```shell
X-Auth-Key
```
```shell
cloudflare_account_id
```

## 2. INSTALL AAPANEL TO UBUNTU
## 3. TURN ON API IN AAPANLE
## 4. ADD WHITELIST API AAPANEL
## 6. CREATE FTP CONNECTION
```shell
aaPanelFTP_host = "ip"
```
```shell
aaPanelFTP_username = "dadadadada"
```
```shell
aaPanelFTP_port = 21
```
```shell
aaPanelFTP_password = 'WxHtiZiTcpLphxKD'
```



## 7. EDIT `server.py`

## 8. EDIT in admin.html line `860` ` var ifs = '93.123.39.14'` ip to setup `A RECORD`


## 9. Configure settings
    edit port here : `    app.run(debug=True, host='0.0.0.0', port=3030)` line `228`

## 10. Configure NODE JS
```shell
https://nodejs.org/dist/v20.12.2/node-v20.12.2-linux-x64.tar.xz
```

```shell
tar -xvf node-v20.12.2-linux-x64.tar.xz
```

```shell
export PATH=/usr/local/node-v20.12.2-linux-x64/bin:$PATH

```
```shell
node -v
```
```shell
npm -v
```

## 11. Installing PM2
```shell
npm install pm2 -g
```


## 12. Start an application
You can start any application (Node.js, Python, Ruby, binaries in $PATH...) like that:
```shell
pm2 start main.py
```
ok 

```shell
pm2 start main.py --interpreter python3
```
or
```shell
pm2 start main.py --interpreter python
```


## 13. To list all running applications:
```shell
pm2 list
```

<div align="center">
  <img src="https://github.com/Unitech/pm2/raw/master/pres/pm2-ls-v2.png">
</div>


## 14. Managing apps is straightforward:
```shell
$ pm2 stop     <app_name|namespace|id|'all'|json_conf>
$ pm2 restart  <app_name|namespace|id|'all'|json_conf>
$ pm2 delete   <app_name|namespace|id|'all'|json_conf>
```




### 🔴🔴🔴 SEARCH OPTION 🔴🔴🔴
USAGE:  `http://ip:port/admin`


Finally!




Finally!




