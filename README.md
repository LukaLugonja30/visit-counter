[![CI](https://github.com/LukaLugonja30/visit-counter/actions/workflows/ci.yml/badge.svg)](https://github.com/LukaLugonja30/visit-counter/actions/workflows/ci.yml)

Mala Flask aplikacija koja broji posete i čuva brojač u Redis-u.
Pokreće se u Docker-u preko Docker Compose-a, a GitHub Actions je testira na svaki
push.
## Arhitektura

Korisnik komunicira sa aplikacijom, a aplikacija kounicira sa redisom



## Endpointi
| Endpoint | Odgovor |
|---|---|
| `GET /` | `{"message": "Hello DevOps", "host": "<id kontejnera>"}` |
| `GET /visits` | uveća brojač, `{"visits": 42}` |
| `GET /health` | `200 {"status": "ok"}` ili `503 {"status": "error"}` |



## Preduslovi
- Docker Desktop (ili Docker Engine + Compose plugin)
- Git
- (za lokalni razvoj) Python 3.12



## Pokretanje
```
git clone https://github.com/LukaLugonja30/visit-counter.git
cd visit-counter
cp .env.example .env
docker compose up -d --build
curl http://localhost:8080/visits
./scripts/healthcheck.sh http://localhost:8080
```
Gašenje: `docker compose down` (podaci ostaju), `docker compose down -v` (briše i
podatke).



## Testovi i linter (lokalno)
```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
pytest -v
```


## Konfiguracija
| Promenljiva | Značenje | Primer |
|---|---|---|
| `APP_PORT` | port aplikacije | `8080` |

| `REDIS_HOST` | adresa Redis-a | `redis` |
| `REDIS_PORT` | port Redis-a | `6379` |


## Važnije odluke
- **Python + Flask**: najmanje koda za 3 endpointa, lako za čitanje.
- **`python:3.12-slim`**: zvanična slika, mnogo manja od pune, a bez problema koje
Alpine ima sa nekim Python paketima.
- **`redis:7.4-alpine`**: zvanična i vrlo mala slika; tačna verzija da build bude
ponovljiv.
- **Zavisnosti pre koda u Dockerfile-u**: izmena koda ne pokreće ponovo `pip install`
(Docker cache).
- **Ne-root korisnik**: manja šteta ako neko kompromituje aplikaciju.
- **Named volume + `appendonly`**: brojač preživljava `docker compose down`.
- **Redis bez `ports`**: dostupan samo aplikaciji kroz internu Compose mrežu.
- **Healthcheck + `depends_on: service_healthy`**: aplikacija kreće tek kad je Redis
spreman.
- **ruff**: brz linter, jedan alat umesto više.



## Problemi na koje sam naišao

- docker run hello-world je vraćao "permission denied" u WSL-u.
  Docker Desktop prvo nije bio pokrenut, a ni posle pokretanja Ubuntu nije video Docker. 
  Rešenje: u Docker Desktop-u uključio sam Settings / Resources / WSL integration / Ubuntu,
  pa restartovao WSL sa wsl --shutdown iz PowerShell-a. Naučio sam da za lokalni rad
  nije potreban Docker nalog, nego da WSL bude povezan sa Docker Desktop-om.
 

## Šta bih unapredio da imam više vremena
- Više testova (npr. /visits i /health sa lažnim Redis-om, fakeredis)
- Healthcheck i za app servis
## Korišćeni alati
- Claude (AI): objašnjenje koncepata i pomoć pri pisanju Dockerfile-a, compose-a, CI-
a i skripte.
- Zvanična dokumentacija: Docker, Flask, GitHub Actions
