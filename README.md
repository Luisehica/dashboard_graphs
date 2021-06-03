# Beak Data Challenge

## About the project


#### App
src/python index.py

#### App Url
http://18.191.13.86:8080/main

## Quickstart
Dashboard deploy with EC2

### Install git
```
yum install git
```
### Instal docker 
```
yum install docker
```
### Instal docker-compose

Download docker-compose 1.22.0 
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Apply executable permissions to the binary
```
sudo chmod +x /usr/local/bin/docker-compose
```

Verify docker-compose version
```
docker-compose --version
```


### Deploy the app

```
git clone https://github.com/Luisehica/Beak_Data_Challenge.git
```

```
docker-compose up -d
```
```
localhost:8080
```

## Development

###  Links and additional data

**Github:**
https://github.com/Luisehica/Beak_Data_Challenge

**Notion:**
https://www.notion.so/luisehica/Beak-Data-Challenge-ed5404842b214f9395c3c0894ccb0e3f
