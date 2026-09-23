## Zadanie praktyczne

Twoim zadaniem jest odnalezienie partyzanta ukrywającego się w ruinach Domatowa i przeprowadzenie sprawnej akcji ewakuacyjnej. Do dyspozycji masz transportery oraz żołnierzy zwiadowczych. Musisz tak rozegrać tę operację, aby odnaleźć człowieka, którego szukamy, nie wyczerpać punktów akcji i zdążyć wezwać helikopter zanim sytuacja wymknie się spod kontroli.

Po mieście możesz poruszać się zarówno transporterami, jak i pieszo. Transportery potrafią jeździć tylko po ulicach. Zanim wyślesz kogokolwiek w teren, przeanalizuj bardzo dokładnie układ terenu. Gdy tylko któryś ze zwiadowców znajdzie człowieka, wezwij śmigłowiec ratunkowy tak szybko, jak to tylko możliwe.

Nazwa zadania: **domatowo**

Odpowiedź wysyłasz do `/verify`

Przechwycony sygnał dźwiękowy:

> "Przeżyłem. Bomby zniszczyły miasto. Żołnierze tu byli, szukali surowców, zabrali ropę. Teraz jest pusto. Mam broń, jestem ranny. Ukryłem się w jednym z najwyższych bloków. Nie mam jedzenia. Pomocy."

Podgląd mapy miasta: https://hub.ag3nts.org/domatowo_preview

Z API komunikujesz się zawsze przez `https://hub.ag3nts.org/verify` i wysyłasz JSON z polami `apikey`, `task` oraz `answer`.

Podstawowy format komunikacji wygląda tak:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "..."
  }
}
```

Na początek warto pobrać opis dostępnych akcji:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "help"
  }
}
```

### Co masz do dyspozycji

- maksymalnie 4 transportery
- maksymalnie 8 zwiadowców
- 300 punktów akcji na całą operację
- mapę 11x11 pól z oznaczeniami terenu

Najważniejsze typy akcji mają swoją cenę:

- utworzenie zwiadowcy: 5 punktów
- utworzenie transportera: 5 punktów opłaty bazowej oraz dodatkowo 5 punktów za każdego przewożonego zwiadowcę
- ruch zwiadowcy: 7 punktów za każde pole
- ruch transportera: 1 punkt za każde pole
- inspekcja pola: 1 punkt
- wysadzenie zwiadowców z transportera: 0 punktów

### Rozpoznanie terenu

Najpierw zapoznaj się z układem miasta. Możesz pobrać całą mapę:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "getMap"
  }
}
```

Możesz także wyświetlić podgląd mapy uwzględniający tylko konkretne jej elementy, podając je w opcjonalnej tablicy `symbols`.

### Tworzenie jednostek

Możesz utworzyć transporter z załogą zwiadowców - tutaj przykład 2-osobowej załogi:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "create",
    "type": "transporter",
    "passengers": 2
  }
}
```

Możesz też wysłać do miasta pojedynczego zwiadowcę:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "create",
    "type": "scout"
  }
}
```

### Ewakuacja

Helikopter można wezwać dopiero wtedy, gdy któryś zwiadowca odnajdzie człowieka. Finalne zgłoszenie wygląda tak:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "callHelicopter",
    "destination": "F6"
  }
}
```

W polu `destination` podajesz współrzędne miejsca, do którego ma przylecieć śmigłowiec. Musisz tam wskazać pole, na którym zwiadowca potwierdził obecność człowieka.

### Co musisz zrobić

- rozpoznaj mapę miasta i zaplanuj trasę tak, by nie przepalić punktów akcji
- utwórz odpowiednie jednostki i rozlokuj je na planszy
- wykorzystaj transportery do szybkiego dotarcia w kluczowe miejsca
- wysadzaj zwiadowców tam, gdzie dalsze sprawdzanie terenu wymaga działania pieszo
- przeszukuj kolejne pola akcją `inspect` i analizuj wyniki przez `getLogs`
- gdy odnajdziesz partyzanta, wezwij helikopter akcją `callHelicopter`

Jeśli poprawnie odnajdziesz ukrywającego się człowieka i zakończysz ewakuację, Centrala odeśle flagę.


# BONUS

Jak odkodowac coś takiego: 4a,61,6b,20,6d,69,61,c5,82,20,6e,61,20,69,6d,69,65,20,67,6f,c5,9b,c4,87,20,6f,64,20,56,69,67,65,6e,c3,a8,72,65,3f,0a,2d,2d,2d,0a,50,20,75,61,73,61,71,20,71,7a,6a,6d,c5,ba,76,64,6a,70,20,70,77,20,73,72,68,74,65,74,6b,6f,76,20,78,c3,b3,77,71,20,53,64,62,6b,65,74,3f,0a,6d,6b,68,6e,66,3a,2f,2f,63,7a,73,2e,6f,65,33,61,6f,78,2e,66,66,65,2f,71,76,73,76,2f,6f,78,6e,75,6a,63,5f,67,63,70,6d,6a,6b,2e,61,6e,34

Pierwsza część wiadomości to zaszyfrowane w systemie szesnastkowym pytanie: 4a 61 6b 20 ... po odkodowaniu z HEX i UTF-8 daje: "Jak miał na imie gość od Vigenère?"

Odpowiedź na to pytanie brzmi: Blaise (od Blaise de Vigenère). Słowo to jest jednocześnie kluczem do odszyfrowania dalszej części wiadomości (za pomocą szyfru Vigenère'a).

Odkodowana treść pytania (z kluczem BLAISE): "O jakim pojeździe po torach mówi Sekret?"

Odkodowany link (szyfr kontynuowany dla każdego znaku, ignorując znaki specjalne jak :// czy _): https://www.x3dom.org/docs/latest/api_reference.html

(Proces dekodowania adresu URL uwzględnia kontynuację pozycji klucza 'BLAISE' na kolejnych literach ciągu mkhnf://czs.oe3aox.ffe/qvsv/oxnujc_gcpmjk.an4).


# FLAGA

{FLG:WEVEGOTHIM} @ F2
