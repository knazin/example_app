# Semantive Downloader

Mikroserwis zajmujacy sie gromadzeniem i udostępnianiem informacji pobranych z sieci.  
Jego zadaniem jest pobieranie testku oraz obrazów z róznych stron internetowych.


## Główne Funkcjonalności

- Pobranie tesktu z danej strony internetowej i zapis jej w systemie
- Pobranie wszystkich obrazków z danej strony i zapis ich w systemie.
- Sprawdzenie statusu zleconego zadania.
- Możliwość pobrania stworzonych zasobów (tekstu i obrazków).


## Model UML

![UML](docs/Semantive_downloader.png)


## Start / Stop Aplikacji

** wymagane jest posiadanie oprogramowania [docker](https://docs.docker.com/docker-for-mac/install/)

Aby odpalic aplikacje nalezy wejsc w terminal a nastepnie wykonac ponizsze polecenia:
```bash
$ git clone github.com/...
$ cd docker
$ docker-compose up -d --build
```

Aby sprawdzic czy wszystko na pewno dziala mozna wykonac komende
```bash
$ docker ps -a
```
i sprawdzic czy znajduja sie tam obrazy takie jak:
- semantive_redis
- semantive_database
- semantive_worker
- semantive_application

```
CONTAINER ID    ...          PORTS                     NAMES
705cde86f9f7    ...    0.0.0.0:5050->5000/tcp    semantive_application
06865662af86    ...                              semantive_worker
e2c82dfa6203    ...    0.0.0.0:6379->6379/tcp    semantive_redis
b9288cd8a39c    ...    0.0.0.0:54320->5432/tcp   semantive_database
```

Jezeli wszystko jest w porzadku mozna w pelni korzystac z aplikacji

Aby zamknac aplikacje nalezy wykonac nastepujaca komende
```bash
# bedac w sciezce .../semative_downloader/docker
$ docker-compose down
```


## Uzytkowanie

Aplikacja znajduje sie pod adresem (jesli wykorzystywana lokalnie)

<i>localhost:5050</i>

Aby pobrac tekst albo obraz z podanej przez uzytkownika strony internetowej 
nalezy podac url w body zapytania do odpowiednich adresów mikroserwisu.  

W momencie wyciagniecia zasob z serwisu typu:
- teskt - uzytkownik otrzyma go w jednym z polu zwróconego pliku JSON
- obrazy - uzytkownik otrzyma plik zip który zawiera obrazy zawarte na stronie

Szczegółową instrukcje posługiwania się mikroserwisem uzytkownik znajdzie pod nastepujacym linkiem do serwisu:
<i>/api/v1/docs/</i>

WSTAW OBRAZEK



## Testowanie

** wymagane jest posiadanie oprogramowania [docker](https://docs.docker.com/docker-for-mac/install/) oraz [python](https://www.python.org/downloads/)

Aby moc przetestowac aplikacje trzeba wykonac nastepujace czynnosci:  

1. Zmienic w pliku `app/.env` zmienic wartosc zmiennej 
   ```bash
   CONFIG_TYPE=production # jezeli korzystamy z aplikacji
   CONFIG_TYPE=local_testing # jezeli wykonywujemy testy
   ```
2. Odpalic baze redis
   ```bash
    # bedac w sciezce .../semantive_downloader/docker
    $ docker-compose up -d redis
   ```
3. W nowym oknie terminala zainstalowac biblioteke <i>virtualenv</i> (jesli docelowa maszyna tego nie zawiera)
   ```bash
    $ python -m pip install virtualenv
   ```
4. Stworzyc wlasne srodowisko oraz zainstalowac w nim zalezności
   ```bash
    # bedac w sciezce .../semantive_downloader
    $ virtualenv myenv
    $ source myenv/bin/activate # w wesji dla mac'a/linux'a 
    $ (myenv) cd app
    # /semantive_downloader/app
    $ (myenv) pip install -r requirements.txt
   ```
5. Odpalic worker'a aplikacji
   ```bash
    # bedac w sciezce .../semantive_downloader/app/tasks
    $ (myenv) celery -A tasks worker --loglevel=info
   ```
6. W kolejnym nowym oknie terminala wejsc w lokalne srodowisko <i>myenv</i> i odpalic testy
   ```bash
    # bedac w sciezce .../semantive_downloader
    $ source myenv/bin/activate
    $ (myenv) pytest -vv 
   ```

## Co nie tak
- Nie udalo zautomatyzowac tworzenie i przelaczanie z bazy produkcyjnej na baze testowa w PostgresSQL (z tego wzgledu testy sa w bazie SQLite)
- Nie udalo sie wykonywac testow automatycznych w kontenerach (zapytania http z kontera byly zbyt wolne)
- Maly balagan w pliku .env ???
- Nie uwzgledniona ew. wymiennosc http z https
- aplikacja prawdopodobnie nie jest przygotowana na wszystkie ew. defekty w url zdjec zamieszczonych w tagach
- prawdodobnie testy nie wychytuja wszytkich ew. bledow/scenariuszy