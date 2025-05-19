import numpy as np
import itertools

# Sprawdza, czy dwa obiekty są sprzeczne względem podanych atrybutów
# (czyli mają takie same wartości, ale różną decyzję)
def sprz(o1, o2, atr):
    return all(o1[a] == o2[a] for a in atr) and o1[-1] != o2[-1]

# Zwraca wszystkie kombinacje atrybutów o długości n
def genkom(atr, n):
    return list(itertools.combinations(atr, n))

# Zwraca indeksy obiektów pokrywanych przez regułę (czyli spełniających wszystkie warunki)
def znpok(dane, o1, kom):
    return {j for j, o2 in enumerate(dane) if all(o2[a] == o1[a] for a in kom)}

# Tworzy regułę w formie tekstu, np. o2(a1=1)(a3=3) -> (d=1)[3]
def utreg(i, o1, kom, pokakt):
    pokcount = len(pokakt)
    pokstr = f"[{pokcount}]" if pokcount > 1 else ""
    atrstr = ''.join(f'(a{a+1}={o1[a]})' for a in kom)
    return f"o{i+1}{atrstr} -> (d={o1[-1]}){pokstr}"

# Główny algorytm – Sequential Covering
# Szuka minimalnych reguł pokrywających obiekty bez sprzeczności
def seqcov(plik):
    dane = np.loadtxt(plik, dtype=int)  # wczytanie pliku .txt z danymi
    kol = dane.shape[1]                 # liczba kolumn (ostatnia to decyzja)
    atr = list(range(kol - 1))          # indeksy kolumn atrybutów

    reg = []      # lista reguł
    pok = set()   # zbiór pokrytych obiektów

    # Spróbujmy kombinacji od 1 aż do liczby atrybutów
    for ilatr in range(1, len(atr) + 1):
        for i, o1 in enumerate(dane):
            if i in pok:
                continue  # pomijamy już pokryte

            for kom in genkom(atr, ilatr):
                # jeśli sprzeczna z jakimś obiektem – pomijamy
                if i in pok or any(sprz(o1, o2, kom) for o2 in dane if not np.array_equal(o2, o1)):
                    continue

                # sprawdzamy, które obiekty pasują do tej kombinacji
                pokakt = znpok(dane, o1, kom)
                pok.update(pokakt)  # dodajemy do pokrytych

                # tworzymy opis reguły
                regakt = utreg(i, o1, kom, pokakt)

                if regakt not in reg:
                    reg.append(regakt)

    return reg

# Uruchomienie algorytmu i wypis reguł
plik = "macierz.txt"
reguly = seqcov(plik)
for r in reguly:
    print(r)
