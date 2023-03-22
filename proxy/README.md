# Https-Proxy-IRIS-Docker with Apache
Sample of an Https proxy for Intersystems Iris

## Run

```
docker-compose up -d
```

## Test

```
https://localhost/csp/bin/Systems/Module.cxw
```
and
```
https://localhost/csp/sys/UtilHome.csp
```
## How it works

The dockerfile works in 3 steps :
* Make a self-signed certificate
* Load modules
  * For proxy mode
  * For SSL
* Make config file for the proxy

The docker-compose :
* Configure arguments of the dockerfile
  * link of the IRIS docker
  * port of the IRIS docker
* Run Apache
* Run IRIS Community Edition
