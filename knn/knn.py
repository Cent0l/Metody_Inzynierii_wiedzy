import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from collections import Counter

# KROK 1: Wczytujemy zbiór iris z biblioteki sklearn
# Zawiera dane o długościach i szerokościach płatków/działek kwiatów oraz ich klasy
iris = load_iris()
X = iris.data       # tylko atrybuty (4 kolumny liczbowe)
y = iris.target     # klasy decyzyjne (0, 1, 2 – czyli 3 różne kwiaty)

# KROK 2: Dzielimy dane na zbiór treningowy i testowy
# 70% idzie do nauki (trening), 30% do testu, stratify=y zachowuje proporcje klas
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# KROK 3: Liczymy odległość Euklidesową między dwoma punktami (czyli klasyczne √((x1 - x2)^2 + ...))
def euklides(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

# KROK 4: Nasza własna funkcja KNN – żadnych gotowców!
# Bierzemy zbiór treningowy, testowy i wartość k (ilu sąsiadów patrzymy)
def knn(X_train, y_train, X_test, k):
    przewidziane_klasy = []  # tu będziemy zapisywać klasy, które przewidzieliśmy
    for x in X_test:  # dla każdego obiektu z testowego
        # Liczymy dystans od tego obiektu do KAŻDEGO obiektu z treningowego
        dystanse = [euklides(x, xtr) for xtr in X_train]

        # Sortujemy dystanse i bierzemy indeksy k najbliższych
        najblizsi_idx = np.argsort(dystanse)[:k]

        # Zbieramy klasy tych k najbliższych sąsiadów
        najblizsze_klasy = [y_train[i] for i in najblizsi_idx]

        # Wybieramy klasę, która występuje najczęściej wśród sąsiadów
        przewidziana = Counter(najblizsze_klasy).most_common(1)[0][0]

        # Zapisujemy wynik do listy
        przewidziane_klasy.append(przewidziana)

    return przewidziane_klasy  # zwracamy przewidziane klasy dla całego testu

# KROK 5: Uruchamiamy algorytm dla k = 3
k = 3
y_pred = knn(X_train, y_train, X_test, k)

# KROK 6: Liczymy ile razy przewidzieliśmy klasę poprawnie
trafienia = sum(yp == yt for yp, yt in zip(y_pred, y_test))  # porównujemy każdą przewidzianą z rzeczywistą
dokladnosc = trafienia / len(y_test)

# Wypisujemy wynik końcowy – dokładność klasyfikacji
print(f"Dokładność klasyfikacji dla k={k}: {dokladnosc * 100:.2f}% ({trafienia}/{len(y_test)})")
