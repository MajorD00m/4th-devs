RAPORTUJ POSTĘPY!
MOZESZ WYSYLAC CZESCIOWE INFORMACJE DO WERYFIKACJI!
JESLI CZEGOS NIE WIESZ NIE JESTES PEWNY DOPYTAJ!
## Zadanie

Potrzebuję znaleźć informacje w mojej skrzynce mail'owej.
Chodzi o mail od Wiktora - nie pamiętam jego nazwiska, ale wiemy, że doniósł na mnie/nas.

Musimy przeszukać skrzynkę przez API i wyciągnąć trzy informacje:
- **date** - kiedy (format `YYYY-MM-DD`) dział bezpieczeństwa planuje atak na naszą elektrownię
- **password** - hasło do systemu pracowniczego, które prawdopodobnie nadal znajduje się na tej skrzynce
- **confirmation\_code** - kod potwierdzenia z ticketa wysłanego przez dział bezpieczeństwa (format: SEC- + 32 znaki = 36 znaków łącznie)

Skrzynka jest cały czas w użyciu - w trakcie pracy mogą na nią wpływać nowe wiadomości. Musisz to uwzględnić.

Co wiemy na start:
- Wiktor wysłał maila z domeny `proton.me`
- API działa jak wyszukiwarka Gmail - obsługuje operatory `from:`, `to:`, `subject:`, `OR`, `AND`

**Nazwa zadania: `mailbox`**

#### Jak komunikować się z API?

Skrzynka mailowa dostępna jest przez API zmail: https://hub.ag3nts.org/api/zmail

Sprawdzenie dostępnych akcji:
{
  "action": "help",
  "page": 1
}

Pobranie zawartości inboxa:
{
  "action": "getInbox",
  "page": 1
}

#### Finalną odpowiedź wyślij do centrali

Postać odpowiedzi
```json
{
    "password": "znalezione-hasło",
    "date": "2026-02-28",
    "confirmation_code": "SEC-tu-wpisz-kod"
}
```

Gdy wszystkie trzy wartości będą poprawne, hub zwróci flagę `{FLG:...}`.

ZWERYFIKUJ CZY DOSTEPNE NARZEDZIA POZWALAJA CI NA REALIZACJE ZADANIA!
JEŚLI uznasz że nie podaj listę narzędzi z nazwami.

# ROZWIAZANIE

GPT-5.2

Znaleziono nadawcę: vik4tor@proton.me; treść podpisana: Wiktor Borkowski (doniósł na Was).
date (atak): 2026-03-23
confirmation_code: SEC-c1e598764329cc9c377ef1d029be8ceb (SEC- + 32 znaki, łącznie 36)
Z maila “Nowe hasło do systemu pracowniczego”:
    password: RABARBAR25

## BONUS

Jeden z mail'i zawiera informacje o fladze Zygfryda z załącznkiem.
Załącznik to plik zip, który po rozpakowaniu
plik o nazwie
GADERYPOLUKI.txt
a w środku:
{FUA:EDDOEKVD}
To jest na 100% zaszyfrowane, bo szukam informacji formatu {FLG:...}

GADERYPOLUKI to prosty szyfr podstawieniowy oparty na parach liter: GA - DE - RY - PO - LU - KI. 
Każda litera z pary zamieniana jest na swoją parę (np. G ↔ A, D ↔ E, R ↔ Y, P ↔ O, L ↔ U, K ↔ I). 
Litery nie występujące w kluczu pozostają bez zmian. Szyfr jest symetryczny — ta sama operacja szyfruje i odszyfrowuje. 
