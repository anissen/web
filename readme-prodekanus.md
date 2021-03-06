# TÅGEKAMMERETS webside på prodekanus

På prodekanus ligger Django projektet under `/home/tkammer/tkweb/`. Det er ejet
af brugeren `tkammer`, men bliver håndteret igennem WSGI af apache2 og brugeren
`www-data`. WSGI bruger et python3.4 virualenv der ligger i
`/home/tkammer/tkweb/venv/`.

Apache2 håndterer også de statiske filer. Mediefiler ligger på et stor drev
`/Picture/tkammer/media/`.

Databasen er en fælles lokal MySQL.

## Opdatering
For at opdatere siden med de nyeste ændring fra Github skal du gøre følgende:
```sh
    sudo -u tkammer -s  # start en ny shell med tkammer som bruger
    cd /home/tkammer/tkweb  # Skift til mappen med siden.
    source venv/bin/activate  # Aktiver virtualenv.
    git pull  # Hent de nyeste ændringer fra Github.
    pip install -U pip -r requirements.txt  # Installer og opdater alle python pakker i virtualenv. Det kan være at den skal køres flere gange.
    python3 manage.py migrate --settings=tkweb.settings.prod  # Migrer databasen til en evt. ny model.
    python3 manage.py collectstatic --settings=tkweb.settings.prod  # Saml statiske filer så apache kan finde dem.
    sudo service apache2 restart  # Genstart apache så de nye filer bliver taget i brug.
```


## Indstillinger
De vigtigste konfigurationsfiler er følgende:
```sh
/etc/apache2/sites-available/taagekammeret.conf  # apache2
/home/tkammer/tkweb/tkweb/settings/prod.py  # django
```

### SSL
The SSL private key /home/tkammer/tkweb/tkweb-tls.key is used to decrypt
incoming TLS traffic. Don't modify or delete it!


## Logs
Se følgende logs hvis noget går galt:
```sh
/var/log/apache2/*  # apache2
/home/tkammer/tkweb/django.log  # django
```


## Adgang
Du skal være på AUs net for at have adgang til til `prodekanus.studorg.au.dk`.

Man har typisk en personlige konto som man bruger til at få adgang via `sudo`
til `tkammer`-kontoen.
