import pandas as pd
from collections import Counter

# Wczytujemy dane z pliku (każdy wiersz to obiekt, ostatnia kolumna to decyzja)
dane = pd.read_csv('lem2.txt', sep=" ", header=None)
n = dane.shape[1]  # liczba kolumn

# Nadajemy nazwę każdej kolumnie: a1, a2, ..., an, ostatnia to d
dane.columns = [f'a{i+1}' for i in range(n-1)] + ['d']

# atrybuty warunkowe (czyli wszystko oprócz kolumny decyzyjnej)
atrybuty = dane.columns[:-1]

# tu będziemy trzymać reguły przed scaleniem
reguly = []

# dla każdej decyzji (np. d = 1, d = 2, itd.)
for decyzja in sorted(dane['d'].unique()):

    # pozostale – indeksy obiektów, które jeszcze nie zostały pokryte regułami
    pozostale = set(dane.index[dane['d'] == decyzja])

    # dopóki są jeszcze niepokryte obiekty z tej decyzji
    while pozostale:

        # liczymy, które deskryptory (a = v) występują najczęściej w pozostałych
        czestosci = {}
        for atr in atrybuty:
            for wartosc, ile in Counter(dane.loc[list(pozostale), atr]).items():
                czestosci[(atr, wartosc)] = ile

        # wybieramy najczęstszy deskryptor jako początek reguły
        najlepszy = max(czestosci.items(), key=lambda x: x[1])[0]
        regula = [najlepszy]

        # rozbudowujemy regułę, dopóki jest sprzeczna (czyli pasuje też do innych decyzji)
        while True:
            # sprawdzamy które obiekty spełniają aktualną regułę
            dopasowane = set(dane.index)
            for atr, val in regula:
                dopasowane &= set(dane.index[dane[atr] == val])

            # jeśli wszystkie dopasowane obiekty mają decyzję, o którą nam chodzi – kończymy
            if all(dane.loc[i, 'd'] == decyzja for i in dopasowane):
                break

            # szukamy obiektów, które są dopasowane i nadal niepokryte
            kandydaci = dopasowane & pozostale
            if not kandydaci:
                break  # nie mamy jak dalej rozszerzyć

            wybrany = min(kandydaci)  # bierzemy pierwszy z brzegu
            wiersz = dane.loc[wybrany]  # jego wartości

            mozliwe = []
            for atr in atrybuty:
                nowy = (atr, wiersz[atr])
                if nowy not in regula:
                    # próbujemy dodać nowy warunek i sprawdzamy ile obiektów z tej decyzji on pokrywa
                    nowa = regula + [nowy]
                    nowe_dop = set(dane.index)
                    for a_, v_ in nowa:
                        nowe_dop &= set(dane.index[dane[a_] == v_])
                    pokrycie = len(nowe_dop & set(dane.index[dane['d'] == decyzja]))
                    mozliwe.append((nowy, pokrycie))

            if not mozliwe:
                break  # nie ma z czego wybierać

            # wybieramy nowy warunek z największym pokryciem (a jak remis – wg kolejności atrybutów)
            mozliwe.sort(key=lambda x: (-x[1], list(atrybuty).index(x[0][0])))
            regula.append(mozliwe[0][0])

        # ustalamy które obiekty z pozostałych są pokryte tą regułą
        pokryte = set(dane.index)
        for a, v in regula:
            pokryte &= set(dane.index[dane[a] == v])
        pokryte &= pozostale

        # zapisujemy regułę: lista warunków, decyzja, ile obiektów pokryła
        reguly.append((regula, decyzja, len(pokryte)))

        # usuwamy pokryte obiekty, żeby nie tworzyć dla nich więcej reguł
        pozostale -= pokryte

# SCALANIE – jeśli dwie reguły mają te same warunki, ale różne decyzje, łączymy je
scalone = []

for regula, decyzja, sup in reguly:
    znalezione = False
    for reg in scalone:
        if reg["warunki"] == regula:
            reg["decyzje"].add(decyzja)
            reg["support"] += sup
            znalezione = True
            break
    if not znalezione:
        scalone.append({
            "warunki": regula,
            "decyzje": {decyzja},
            "support": sup
        })

# WYŚWIETLAM końcowe reguły
for i, reg in enumerate(scalone, 1):
    # składanie lewej strony: warunki typu (a1 = 2) ∧ (a2 = 3) ...
    lewa = " ∧ ".join(f"({a} = {v})" for a, v in reg["warunki"])
    # skladanie prawej strony: np. (d = 1) | (d = 2)
    prawa = " | ".join(f"(d = {d})" for d in reg["decyzje"])
    # jeśli więcej niż 1 obiekt – pokazujemy [support]
    sup = f"[{reg['support']}]" if reg["support"] > 1 else ""
    print(f"reg: {i} {lewa} => {prawa}{sup}")
