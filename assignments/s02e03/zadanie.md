# ZADANIE

Wczoraj w elektrowni doszło do awarii. Masz dostęp do pełnego pliku logów systemowych z tego dnia - ale jest on ogromny. Twoje zadanie to przygotowanie skondensowanej wersji logów, która:

1. zawiera wyłącznie zdarzenia istotne dla analizy awarii (zasilanie, chłodzenie, pompy wodne, oprogramowanie i inne podzespoły elektrowni),
2. mieści się w 1500 tokenach,
3. zachowuje format wieloliniowy - jedno zdarzenie na linię.

Skondensowane logi wysyłasz do Centrali. Technicy weryfikują, czy na ich podstawie można przeprowadzić analizę przyczyny awarii. Jeśli tak - otrzymujesz flagę.

Pobierz pełny plik logów: https://hub.ag3nts.org/data/tutaj-twój-klucz/failure.log

Wysylaj logi do analitykow. Pole logs to string - wiersze oddzielone znakiem \n. Każdy wiersz to jedno zdarzenie.
Wymagania formatowe

1. Jeden wiersz = jedno zdarzenie - nie łącz wielu zdarzeń w jednej linii 
2. Data w formacie YYYY-MM-DD - technicy muszą wiedzieć, którego dnia zdarzenie miało miejsce
3. Godzina w formacie HH:MM lub H:MM - żeby umieścić zdarzenie w czasie
4. Możesz skracać i parafrazować - ważne żeby zachować: znacznik czasu, poziom ważności i identyfikator podzespołu
5. Nie przekraczaj 1500 tokenów - to twarde ograniczenie systemu Centrali.

Co należy zrobić w zadaniu?

1. Pobierz plik logów - sprawdź jego rozmiar. Ile ma linii? Ile tokenów zajmuje cały plik?
2. Wyfiltruj istotne zdarzenia - z tysięcy wpisów wybierz tylko te dotyczące podzespołów elektrowni i awarii. Jak można stwierdzić które zdarzenia istotnie przyczyniły się do awarii? Które są najważniejsze?
3. Skompresuj do limitu - upewnij się, że wynikowy plik mieści się w 1500 tokenach. Możesz skracać opisy zdarzeń, byleby zachować kluczowe informacje.
4. Wyślij i przeczytaj odpowiedź - Centrala zwraca szczegółową informację zwrotną od techników: czego brakuje, które podzespoły są niejasne lub niewystarczająco opisane. Wykorzystaj tę informację do poprawienia logów.
5. Popraw i wyślij ponownie - iteruj na podstawie feedbacku, aż technicy potwierdzą kompletność i otrzymasz flagę {FLG:...}.

Wskazówki

1. Plik z logami jest duży - jak możesz go sensownie przeszukiwać?
2. Feedback od techników jest bardzo precyzyjny - Centrala podaje dokładnie, których podzespołów nie dało się przeanalizować. To cenna wskazówka, czego w logach brakuje - warto ją wykorzystać do uzupełnienia wynikowego pliku.
3. Czy warto na początku wysłać wszystko co istotne? - Ile tokenów zajmują same zdarzenia WARN/ERRO/CRIT? Czy na pewno zmieszczą się w limicie bez dalszej kompresji? A może lepiej zacząć od mniejszego zestawu i uzupełniać w oparciu o feedback? Przemyśl, które podejście da szybszy wynik.
4. Zliczaj tokeny przed wysłaniem - wysyłanie logów przekraczających limit skończy się odrzuceniem. Wbuduj zliczanie tokenów jako osobny krok przed weryfikacją. Przyjmij konserwatywny przelicznik.

Przeanalizuj dostępne narzędzia, czy któreś z narzędzi nie umożliwia Ci pobranie wspomnianych logów?
następnie przygotuj plan realizacji zadania

