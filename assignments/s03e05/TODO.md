NIE UKONCZONE
Poejdynczy agent się plącze.
Trzeba zrobić subagentów. 
AGNO Teams
1. GŁÓWNY agent orkiestrator
2. Agent do wyszukiwania narzędzi:
   - na wejściu dostaje proste wymaganie np. znajdź narzędzia związane z podróżą, wiedzą o terenie pojazdach itd.
   - szuka i zapisuje listę narzędzi wraz z ich definicjami
   - może zapisywać w knowledge, albo w plikach (albo i tu i tu)
3. Agent do budowania dokumentacji/wiedzy
   - z użyciem odkrytych narzędzi z punktu 2
   - dostaje definicję narzędzia i ma za zadanie wyciągnąć wszelkie informacje z danego narzędzia i je zapisać
4. Agent analityk:
   - ma wybrać OPTYMALNY zestaw informacji potrzebny do zaplanowania podróży
   - jeśli już coś potrafi wybrać, np. optymalny pojazd TO MA TO ZROBIĆ, np. ranking
4. Agent do zaplanowania trasy:
   - dostaje: mapę, wybrany pojazd i pozostałe NIEZBĘDNE informacje
   - Ma subagenta, symulator kolejnego zaproponowanego kroku:
     - czy się rozwali pojazd, czy się zbliża czy oddala od celu, czy dystans jest ten sam?
