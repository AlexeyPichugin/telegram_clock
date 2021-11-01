# Telegram current time clock
Python script for update telegram's avatar to current time clock

# For usage needs:
1. Create your app and get user api id and hash. URL: https://my.telegram.org/auth
2. Clone files and install requirements from file.
3. Create in application directory file `.env` and put into it your API_ID and API_HASH.
4. Start application, one times again put your mobile phone and SMS-code.
5. Enjoy!
 
Thank for idea and link to library `mumtozvalijonov`
Link to original paper: https://habr.com/ru/post/457078/

# Run in docker
Docker-hub page: https://hub.docker.com/r/apichugin/telegram_clock

1. After building the image, you need initialize session and get session string. You must to set it to applications variable `<TELEGRAM_SESSION>`

```
$ docker run -it -e API_ID=<API_ID> -e API_HASH=<API_HASH> -v $(pwd)/configs/config.yaml:/srv/app/configs/config.yaml apichugin/telegram_clock:latest --init 
1ApWapzMBu0JLeT5nTNXlcdabsi_48nYHaYSSKH5cgr8a4Cc5...48nYHaYSSKH5cgr8a4Cc5KcRYPUmI=
```docker pull 

2. Run application.
You can transfer session data in 3 different ways:

- Create `.env` file:
```
API_ID=<API_ID>
API_HASH=<API_HASH>
TELEGRAM_PHONE=<TELEGRAM_PHONE>
TELEGRAM_PASSWORD=<TELEGRAM_PASSWORD>
TELEGRAM_SESSION=<TELEGRAM_SESSION>
```
and put it in docker container
```
docker run --rm -d -v $(pwd)/configs/config.yaml:/srv/app/configs/config.yaml --env-file=.env apichugin/telegram_clock:latest
```

- Pass them environment variables
```
docker run --rm -d \
    -v $(pwd)/configs/config.yaml:/srv/app/configs/config.yaml \
    -e API_ID=<API_ID> \
    -e API_HASH=<API_HASH> \
    -e TELEGRAM_PHONE=<TELEGRAM_PHONE> \
    -e TELEGRAM_PASSWORD=<TELEGRAM_PASSWORD> \
    -e TELEGRAM_SESSION=<TELEGRAM_SESSION> \
    apichugin/telegram_clock:latest
```

- Pass through CLI arguments
```
docker run --rm -d \
    -v $(pwd)/configs/config.yaml:/srv/app/configs/config.yaml \
    apichugin/telegram_clock:latest \
    --api-id <API_ID> \
    --api-hash <API_HASH> \
    --session <TELEGRAM_SESSION> \
    --phone-number <TELEGRAM_PHONE> \
    --password <TELEGRAM_PASSWORD>
```
