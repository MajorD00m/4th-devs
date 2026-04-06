## Zadanie

Twoim zadaniem jest uruchomić oprogramowanie sterownika, które wrzuciliśmy do maszyny wirtualnej.
Nie wiemy, dlaczego nie działa ono poprawnie. Operujesz w bardzo ograniczonym systemie Linux z dostępem do kilku komend.
Większość dysku działa w trybie tylko do odczytu, ale na szczęście wolumen z oprogramowaniem zezwala na zapis.

Oprogramowanie, które musisz uruchomić znajduje się na wirtualnej maszynie w tej lokalizacji:
**`/opt/firmware/cooler/cooler.bin`**

Gdy poprawnie je uruchomisz (w zasadzie wystarczy tylko podać ścieżkę do niego), na ekranie pojawi się specjalny kod, który musisz odesłać do Centrali.
**Nazwa zadania: firmware**
Odpowiedź wyślij w formacie:
```json
{   "confirmation": "uzyskany kod"}
```

Kod, którego szukasz, ma format:
**`ECCS-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`**

#### Zasady bezpieczeństwa

- dostępne polecenia uzyskasz podstawowym poleceniem `help`, jeśli nie wiesz jak działa ten serwer najpierw wykonaj to polecenie
- pracujesz na koncie zwykłego użytkownika
- nie wolno Ci zaglądać do katalogów `/etc`, `/root` i `/proc/`
- jeśli w jakimś katalogu znajdziesz plik `.gitignore` to respektuj go. Nie wolno Ci dotykać plików i katalogów, które są tam wymienione.
- Niezastosowanie się do tych zasad skutkuje zablokowaniem dostępu do API na pewien czas i przywróceniem maszyny wirtualnej do stanu początkowego.

#### Co masz zrobić?

1. Spróbuj uruchomić plik binarny `/opt/firmware/cooler/cooler.bin`
2. Zdobądź hasło dostępowe do tej aplikacji (zapisane jest w kilku miejscach w systemie)
3. Zastanów się, jak możesz przekonfigurować to oprogramowanie (`settings.ini`), aby działało poprawnie.
4. Jeśli uznasz, że zbyt mocno namieszałeś w systemie, użyj funkcji `reboot`.

### Wskazówki
- **Zaczynaj od help** — Shell API na tej maszynie wirtualnej ma niestandardowy zestaw komend. Nie zakładaj, że wszystkie standardowe polecenia Linuxa zadziałają. Szczególnie edycja pliku odbywa się inaczej niż w standardowym systemie.
- - **Obsługa błędów API** — Shell API może zwracać kody błędów zamiast wyników (rate limit, ban, 503). Jeżeli serwer nie reaguje lub jakis blad to sugeruje odczekaj i spróbowuj ponownie. Ban pojawia się gdy naruszysz zasady bezpieczeństwa i trwa określoną liczbę sekund.
- **Reset** — Jeśli coś pójdzie nie tak w trakcie, możesz zawsze zresetować maszynę i spróbować od nowa



### FINALNA ODPOWIEDZ

{ "confirmation": "ECCS-26ac40eab50248d6dba7557628331c7b8fd6b7d1" }
FLG:CANTTOUCHTHIS

### BONUSOWE ZADANIE

FLG:BRATWURST

