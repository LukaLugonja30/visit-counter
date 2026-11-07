#!/usr/bin/env bash
# Proverava da li aplikacija radi tako sto zove /health endpoint.
# Upotreba: ./scripts/healthcheck.sh http://localhost:8080





#!/usr/bin/env bash ("shebang"): prva linija kaže sistemu da skriptu izvršava Bash.
#• set -u: ako upotrebimo promenljivu koja ne postoji, skripta odmah pada umesto da tiho radi
#pogrešno.
#• $# je broj prosleđenih argumenata. -lt 1 znači "manje od 1". Ako nema URL-a, ispiše uputstvo i
#izađe sa exit 1.
#• $1 je prvi argument (URL). ${1%/} skida kosu crtu sa kraja, ako postoji, da ne dobijemo
#//health.
#• curl -s -o /dev/null -w "%{http_code}": -s tišina, -o /dev/null baci telo odgovora, -w
#ispiši samo HTTP kod (200, 503...). Ako aplikacija uopšte ne radi, curl vrati 000.
#• $(...) izvrši komandu i stavi njen izlaz u promenljivu.
#• date "+%Y-%m-%d %H:%M:%S" daje vreme u formatu 2026-10-15 10:32:01.
#• Poslednji if služi da posle petog pokušaja ne čekamo bez potrebe još 3 sekunde.



set -u

MAX_ATTEMPTS=5
SLEEP_SECONDS=3

if [ $# -lt 1 ]; then
  echo "Upotreba: $0 &lt;URL&gt;"
  echo "Primer: $0 http://localhost:8080"
  exit 1
fi

URL="${1%/}"

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  status=$(curl -s -o /dev/null -w "%{http_code}" "$URL/health")
  now=$(date "+%Y-%m-%d %H:%M:%S")
  echo "[$now] Pokušaj $attempt/$MAX_ATTEMPTS – HTTP $status"

  if [ "$status" = "200" ]; then
    echo "Aplikacija je zdrava."
    exit 0
  fi

  if [ "$attempt" -lt "$MAX_ATTEMPTS" ]; then
    sleep "$SLEEP_SECONDS"
  fi
done

echo "Aplikacija nije zdrava ni posle $MAX_ATTEMPTS pokušaja."
exit 1