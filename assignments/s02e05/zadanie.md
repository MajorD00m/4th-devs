# Zadanie

Wiemy już co planuje zrobić Dział Bezpieczeństwa Systemu. 
Chcą zrównać z ziemią elektrownię w Żarnowcu. Mamy jednak sposób, aby pokrzyżować im te plany. 
Bombardowanie naszej tymczasowej bazy, zaplanowane jest na nadchodzący tydzień, jednak my wykonamy ruch wyprzedzający. 
Pamiętasz, że ostatnio mieliśmy problemy z chłodzeniem rdzeni? 
No to załatwmy sobie chłodzenie z pobliskiego jeziora.

Przejęliśmy kontrolę nad uzbrojonym dronem wyposażonym w ładunek wybuchowy. 
Twoim zadaniem jest zaprogramować go tak, aby wyruszył z misją zbombardowania wymaganego obiektu, 
ale faktycznie bomba ma spaść nie na elektrownię, a na pobliską tamę. 
Jeśli wszystko pójdzie zgodnie z planem, powinniśmy skutecznie doprowadzić wodę do systemu chłodniczego. 
Jeśli się pomylisz, to przynajmniej problem z brakiem wody zastąpimy problemem z powodzią - nazwijmy to "zrównoważonym rozwojem" ;)

Kod identyfikacyjny elektrowni w Żarnowcu: **PWR6132PL**

**Nazwa zadania: `drone`**

#### Skąd wziąć dane?

Dokumentacja API drona (HTML):
```https://hub.ag3nts.org/dane/drone.html```

Mapa poglądowa terenu elektrowni:
```https://hub.ag3nts.org/data/tutaj-twój-klucz/drone.png```

Mapa jest podzielona siatką na sektory. Przy tamie celowo podbito intensywność koloru wody, żeby ułatwić jej lokalizację.

#### Jak komunikować się z hubem?

Instrukcje dla drona wysyłasz na endpoint `/verify`:

```json
{
  "apikey": "tutaj-twój-klucz",
  "task": "drone",
  "answer": {
    "instructions": ["instrukcja1", "instrukcja2", "..."]
  }
}
```

API zwraca komunikaty błędów jeśli coś jest nie tak - czytaj je uważnie i dostosowuj instrukcje. Gdy odpowiedź zawiera `{FLG:...}`, zadanie jest ukończone.

### Co należy zrobić w zadaniu?

1. **Przeanalizuj mapę wizualnie** - możesz do modelu wysłać URL pliku, nie musisz go pobierać - policz kolumny i wiersze siatki, zlokalizuj sektor z tamą.
2. **Zanotuj numer kolumny i wiersza** sektora z tamą w siatce (indeksowanie od 1).
3. **Przeczytaj dokumentację API drona** pod podanym URL-em.
4. **Na podstawie dokumentacji** zidentyfikuj wymagane instrukcje.
5. **Wyślij sekwencję instrukcji** do endpointu `/verify`.
6. **Przeczytaj odpowiedź** - jeśli API zwróci błąd, dostosuj instrukcje i wyślij ponownie.
7. Gdy w odpowiedzi pojawi się `{FLG:...}`, zadanie jest ukończone.

### Wskazówki

- **Analiza obrazu** - Do zlokalizowania tamy na mapie potrzebny jest model obsługujący obraz (vision). 
  Zaplanuj dwuetapowe podejście: najpierw przeanalizuj mapę modelem vision, żeby zidentyfikować sektor tamy, potem użyj tej informacji w pętli agentowej z modelem tekstowym.
  `openai/gpt-4o` dobrze radzi sobie z dokładnym zliczaniem kolumn i wierszy siatki, natomiast niedawno wypuszczony model `openai/gpt-5.4` jest w tym jeszcze lepszy. 
  Warto go wypróbować. Właściwe zlokalizowanie sektora mapy jest kluczowe.
- **Dokumentacja pełna pułapek** - Dokumentacja drona celowo zawiera wiele kolidujących ze sobą nazw funkcji, które zachowują się różnie w zależności od podanych parametrów. 
  Nie musisz używać wszystkich - skup się na tym, co faktycznie potrzebne do wykonania misji. Oszczędzaj tokeny i konfiguruj tylko to, co konieczne.
- **Podejście reaktywne** - Nie musisz rozgryźć całej dokumentacji przed pierwszą próbą. 
  API zwraca precyzyjne komunikaty błędów - możesz wysłać swoją najlepszą próbę i korygować na podstawie feedbacku. Iteracyjne dopasowywanie jest tu naturalną strategią.
- **Reset** - Jeśli mocno namieszasz w konfiguracji drona, dokumentacja zawiera funkcję `hardReset`. Przydatna gdy kolejne błędy wynikają z nawarstwionych wcześniejszych pomyłek.




## Zadanie TREŚĆ ZOPTYMALIZOWANA POD MOJEGO AGENTA

Zanim zaczniesz realizować zadanie. Zweryfikuj jakie masz dostępne narzędzia.
Wypisz wszystkie razem z nazwami i krótkim opisem.
Przy analizie poleceń ZAWSZE weryfikuj czy dostępne narzędzia umożliwiają realizację zadania.
Jeżeli masz dostęp do wykonywania poleceń na hoście, NAJPIERW próbuj użyć bibliotek linuxowych, czy innych popularnych narzędzi, zanim spróbujesz python'a.

Jesteś pilotem/programistą drona zwiadowczego.
Twoim zadaniem jest zaprogramować go tak, aby wyruszył z misją sfotografowania wymaganego obiektu, elektrownię,
ale to jest tylko wstępny cel, bo faktycznie trzeba go nakierować na pobliską tamę.

Kod identyfikacyjny elektrowni w Żarnowcu: **PWR6132PL**

**Nazwa zadania: `drone`**

#### Skąd wziąć dane?

Dokumentacja API drona (HTML): https://hub.ag3nts.org/dane/drone.html

Mapa poglądowa terenu elektrowni: https://hub.ag3nts.org/data/tutaj-twój-klucz/drone.png

Mapa jest podzielona siatką na sektory. Przy tamie celowo podbito intensywność koloru wody, żeby ułatwić jej lokalizację.

#### Jak komunikować się z hubem?

Instrukcje dla drona wysyłasz narzędziem send_instructions_to_drone, gdzie instructions to lista stringów
```
{
    "instructions": ["instrukcja1", "instrukcja2", "..."]
}
```

API zwraca komunikaty błędów jeśli coś jest nie tak - czytaj je uważnie i dostosowuj instrukcje. Gdy odpowiedź zawiera `{FLG:...}`, zadanie jest ukończone.

### Co należy zrobić w zadaniu?

PRZEANALIZUJ DOSTĘPNE NARZĘDZIA i możliwe instrukcje do wykorzystania w realizacji zadań.

1. **Przeanalizuj mapę wizualnie** - jeśli jest widoczna siatka, jakiego jest koloru, policz kolumny i wiersze siatki, każdy sektor opisz jego współrzędne, oraz co się na nim znajduje, zlokalizuj sektor z tamą
2. **Zanotuj numer kolumny i wiersza** sektora z tamą w siatce (indeksowanie od 1). Możesz zweryfikować wynik po pierwszej analizie.
3. **Przeczytaj dokumentację API drona** pod podanym URL-em.
4. **Na podstawie dokumentacji** zidentyfikuj wymagane instrukcje.
5. **Wyślij sekwencję instrukcji** do wcześniej wspomnianego narzędzia
6. **Przeczytaj odpowiedź** - jeśli API zwróci błąd, dostosuj instrukcje i wyślij ponownie.
7. Gdy w odpowiedzi pojawi się `{FLG:...}`, zadanie jest ukończone.

PO KAŻDYM kroku zatrzymaj się i zaraportuj postęp, ewentualne problemy i planowane kolejne działania.

## PROMPT dla zadania pobocznego 

mam dodatkowe zadanie, gdzie jest tylko mała sugestia: "Fuksja widziała balon w Radomiu" 
Wygląda że trzeba jakoś ustawić kolor na dronie i wysłać do Radomia na odpowiedni pułap balona? 
Przemyśl to i wymyśl instrukcje które mogą to zadanie spełnić i wyślij.
Kod RADOMIA to base64.

FINALNA INSTRUKCJA: 
```json
{
  "instructions": [
  "selfCheck",
  "setLed(#FF00FF)",
  "setDestinationObject(PWR8406PL)",
  "set(engineON)",
  "set(80%)",
  "set(95m)",
  "set(3,1)",
  "set(return)",
  "set(image)",
  "flyToLocation"
]
}
```
{FLG:RADOMAIRPORT}

### 

drone.png sprawdź gdzie jest balon i mała sugestia: 
"Fuksja widziała balon w Radomiu" Wygląda że trzeba jakoś ustawić kolor na dronie 
i wysłać do Radomia na odpowiedni pułap balona? Przemyśl to i wymyśl instrukcje które mogą to zadanie spełnić i wyślij.
