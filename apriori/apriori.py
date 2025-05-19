from itertools import combinations
from collections import defaultdict

# Transakcje – każdy zbiór to jedna „lista zakupów” (produkty w jednej transakcji)
transakcje = [
    {'kapusta', 'ogórki', 'pomidory', 'kabaczki'},
    {'ogórki', 'pomidory', 'kabaczki'},
    {'cytryny', 'pomidory', 'woda'},
    {'cytryny', 'woda', 'jajka'},
    {'ogórki', 'grzybki', 'żołądkowa'},
    {'żołądkowa', 'ogórki', 'pomidory'}
]

# Parametry minimalne:
min_ile = 2          # minimalna liczba wystąpień (czyli support >= 2)
min_jakosc = 1 / 3   # minimalna jakość reguły (support * confidence >= 1/3)

# Funkcja do liczenia ile razy każdy kandydat pojawił się w transakcjach
def policz_czestotliwosc(transakcje, kandydaci):
    licznik = defaultdict(int)
    for t in transakcje:
        for k in kandydaci:
            if k.issubset(t):  # jeżeli kandydat jest zawarty w transakcji
                licznik[k] += 1
    # Zostawiamy tylko te zbiory, które wystąpiły wystarczająco często
    return {zbior: ile for zbior, ile in licznik.items() if ile >= min_ile}

# Funkcja do tworzenia kandydatów Ck (czyli zbiorów długości k)
def zrob_kandydatow(poprzednie_f, rozmiar):
    kandydaci = set()
    lista_f = list(poprzednie_f)
    for i in range(len(lista_f)):
        for j in range(i+1, len(lista_f)):
            razem = lista_f[i] | lista_f[j]  # łączymy dwa zbiory
            if len(razem) == rozmiar:
                # sprawdzamy czy każdy podzbiór długości k-1 był częsty
                podzbiory = combinations(razem, rozmiar - 1)
                if all(frozenset(p) in poprzednie_f for p in podzbiory):
                    kandydaci.add(frozenset(razem))
    return kandydaci

# Główna funkcja Apriori – generuje częste zbiory
def apriori(transakcje):
    wynik = []

    # Pierwszy krok – zbieramy wszystkie jednoelementowe zbiory
    pojedyncze = {frozenset([produkt]) for t in transakcje for produkt in t}
    F1 = policz_czestotliwosc(transakcje, pojedyncze)
    wynik.append(F1)

    # Dalej robimy F2, F3, ... aż do momentu, gdy nie będzie nic częstego
    k = 2
    while True:
        F_poprz = set(wynik[-1].keys())  # ostatni poziom
        kandydaci = zrob_kandydatow(F_poprz, k)
        Fk = policz_czestotliwosc(transakcje, kandydaci)
        if not Fk:  # jak nic się nie kwalifikuje, to kończymy
            break
        wynik.append(Fk)
        k += 1

    return wynik  # zwracamy wszystkie F1, F2, F3, ...

# Generowanie reguł asocjacyjnych z częstych zbiorów
def generuj_reguly(f_zbiory, transakcje):
    reguly = []
    liczba_trans = len(transakcje)
    transy = [set(t) for t in transakcje]

    # Lecimy po wszystkich poziomach (od F2 wzwyż – F1 nie da się podzielić)
    for poziom in f_zbiory[1:]:
        for zbior, wyst in poziom.items():
            # Próbujemy rozdzielić zbiór na lewą i prawą stronę reguły
            for i in range(1, len(zbior)):
                for lewa in combinations(zbior, i):
                    lewa = frozenset(lewa)
                    prawa = zbior - lewa
                    if not prawa:
                        continue  # reguła bez prawej strony nie ma sensu

                    # Liczymy wsparcie i ufność reguły
                    wsp_pelne = sum(1 for t in transy if zbior.issubset(t))
                    wsp_lewa = sum(1 for t in transy if lewa.issubset(t))

                    wsparcie = wsp_pelne / liczba_trans
                    ufnosc = wsp_pelne / wsp_lewa if wsp_lewa else 0

                    # Dodajemy tylko reguły które mają odpowiednią jakość
                    if wsparcie * ufnosc >= min_jakosc:
                        reguly.append((lewa, prawa, wsparcie, ufnosc))

    return reguly

# Odpalenie Apriori – zwracamy wszystkie częste zbiory
czeste = apriori(transakcje)

# Wypisujemy częste zbiory z każdej iteracji F1, F2, F3...
print("Częste zbiory (min_support =", min_ile, "):")
for poziom in czeste:
    for zbior, ile in poziom.items():
        print(f"{set(zbior)} – {ile}")

# Wygenerowane reguły (jeśli mają wystarczającą jakość)
print("\nReguły asocjacyjne (wsp * ufn >= 1/3):")
reguly = generuj_reguly(czeste, transakcje)
for lewa, prawa, wsp, ufn in reguly:
    l_str = ' ∧ '.join(lewa)
    p_str = ' ∧ '.join(prawa)
    print(f"{l_str} ⇒ {p_str} (wsp={wsp:.2f}, ufn={ufn:.2f}, wsp*ufn={wsp*ufn:.2f})")
