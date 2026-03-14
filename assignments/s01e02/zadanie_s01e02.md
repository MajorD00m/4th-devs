## Zadanie

Musisz namierzyć, która z podejrzanych osób z poprzedniego zadania s01e01 **przebywała blisko jednej z elektrowni atomowych.** Musisz także ustalić jej **poziom dostępu** oraz informację koło której elektrowni widziano tę osobę. Zebrane tak dane prześlij do `/verify`. Nazwa zadania to **findhim**.

Jako odpowiedź należy wysłać dane:
- `name` – imię podejrzanego
- `surname` – nazwisko podejrzanego
- `accessLevel` – poziom dostępu z `/api/accesslevel`
- `powerPlant` – kod elektrowni z `findhim_locations.json` (np. `PWR1234PL`)

W formacie:
{
"name": "Jan",
"surname": "Kowalski",
"accessLevel": 3,
"powerPlant": "PWR1234PL"
}
