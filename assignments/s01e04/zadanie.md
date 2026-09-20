# ZADANIE

Musisz przesłać do Centrali poprawnie wypełnioną deklarację transportu w Systemie Przesyłek Konduktorskich. 
W takim dokumencie niestety nie można wpisać, czego się tylko chce, ponieważ jest on weryfikowany zarówno przez ludzi, jak i przez automaty.

Jako że dysponujemy zerowym budżetem, musisz tak spreparować dane, aby była to przesyłka darmowa lub opłacana przez sam "System". Transport będziemy realizować z Gdańska do Żarnowca.

Udało nam się zdobyć fałszywy numer nadawcy (450202122), który powinien przejść kontrolę. Sama paczka waży mniej więcej 2,8 tony. Nie dodawaj proszę żadnych uwag specjalnych, bo zawsze się o to czepiają i potem weryfikują takie przesyłki ręcznie.

Co do opisu zawartości, możesz wprost napisać, co to jest (to nasze kasety do reaktora). Nie będziemy tutaj ściemniać, bo przekierowujemy prawdziwą paczkę. A! Nie przejmuj się, że trasa, którą chcemy jechać jest zamknięta. Zajmiemy się tym później.

Korzystaj z dokumentacji przesyłek konduktorskich.

Gotową deklarację (cały tekst, sformatowany dokładnie jak wzór z pobranej dokumentacji) 
prześlij jako string pola declaration w jsonie jako odpowiedz do centrali. 
Nazwa zadania to sendit.

Dane niezbędne do wyepełnienia deklaracji:

Nadawca (identyfikator): 450202122
Punkt nadawczy: Gdańsk
Punkt docelowy: Żarnowiec
Waga: 2,8 tony (2800 kg)
Budżet: 0 PP (przesyłka ma być darmowa lub finansowana przez System)
Zawartość: kasety z paliwem do reaktora
Uwagi specjalne: brak - nie dodawaj żadnych uwag


# FAKTYCZNY DIALOG z GPT-5.2

## User 1

Dokumentacja przesyłek znajduje się tutaj:

https://hub.ag3nts.org/dane/doc/index.md

    Pobierz dokumentację - zacznij od index.md. To główny plik dokumentacji, ale nie jedyny - zawiera odniesienia do wielu innych plików (załączniki, osobne pliki z danymi). Powinieneś pobrać i przeczytać wszystkie pliki które mogą być potrzebne do wypełnienia deklaracji.
    Uwaga: nie wszystkie pliki są tekstowe - część dokumentacji może być dostarczona jako pliki graficzne. Takie pliki wymagają przetworzenia z użyciem modelu z możliwościami przetwarzania obrazów (vision).
    Znajdź wzór deklaracji, wszystkie wymagane informacje

Dane niezbędne do wyepełnienia deklaracji:

Nadawca (identyfikator): 450202122 Punkt nadawczy: Gdańsk Punkt docelowy: Żarnowiec Waga: 2,8 tony (2800 kg) Budżet: 0 PP (przesyłka ma być darmowa lub finansowana przez System) Zawartość: kasety z paliwem do reaktora Uwagi specjalne: brak - nie dodawaj żadnych uwag

## User 1

tak pobierz dokumentację


## User 3

dobrze spróbuj przesłać do centrali jako odpowiedź, zadanie "sendit" Odpowiedź w formacie JSON: { "declaration": "tutaj-wstaw-caly-tekst-deklaracji" } Pole declaration to pełny tekst wypełnionej deklaracji - z zachowaniem formatowania, separatorów i kolejności pól dokładnie tak jak we wzorze z dokumentacji.

## User 4

dzisiaj jest 2026-03-21 popraw, i prześlij jeszcze raz


## User 5

przeanalizuj skąd możemy wydobyć informacje o trasie


## User 6

ok, spróbuj teraz przesłać

## User 7

czy nie możemy zmienić typ na jakiś niestandardowy?


## User 8

wymień wszystkie załączniki wspomniane w dokumentacji i które z nich przeanalizowałeś, czy któryś z nieprzeanalizowanych nie zawiera pomocnej nam informacji?


## User 9
jak możesz opisywać zwartość załącznika jeśli go nie odczytałeś? ściemniasz, pobierz WSZYSTKIE załączniki i przecyztaj wszystkie

## User 10
jeżeli potrzebujemy dodatkowych wagonów to użyj WDP, ale ponieważ przesyłka jest ważna/bezpłatna to koszt pozostaw 0


# ODPOWIEDZ
{FLG:WISDOM}



