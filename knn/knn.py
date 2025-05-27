import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from collections import Counter

# Krok 1: Wczytanie danych
iris = load_iris()
X = iris.data      # atrybuty (cechy kwiatów)
y = iris.target    # klasy decyzyjne (0, 1, 2)

# Krok 2: Podział na dane treningowe i testowe (losowo, 70% / 30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Krok 3: Obliczanie odległości Euklidesowej
def odleglosc(p1, p2):
    suma_kwadratow = np.sum((p1 - p2) ** 2)
    return np.sqrt(suma_kwadratow)

# Krok 4: Własna funkcja KNN
def knn(X_tren, y_tren, X_test, k):
    przewidziane = []
    for obiekt_testowy in X_test:
        dystanse = []
        for i in range(len(X_tren)):
            d = odleglosc(obiekt_testowy, X_tren[i])
            dystanse.append((d, y_tren[i]))  # zapisujemy dystans i klasę

        # sortujemy po dystansie i bierzemy k najbliższych
        dystanse.sort(key=lambda x: x[0])
        k_najblizszych = [klasa for _, klasa in dystanse[:k]]

        # wybieramy najczęściej występującą klasę
        najczestsza = Counter(k_najblizszych).most_common(1)[0][0]
        przewidziane.append(najczestsza)

    return przewidziane

# Krok 5: Uruchomienie algorytmu KNN dla k = 3
k = 3
y_pred = knn(X_train, y_train, X_test, k)

# Krok 6: Liczymy dokładność klasyfikacji
trafienia = 0
for i in range(len(y_test)):
    if y_pred[i] == y_test[i]:
        trafienia += 1

dokladnosc = trafienia / len(y_test)
print(f"Dokładność dla k={k}: {dokladnosc * 100:.2f}% ({trafienia}/{len(y_test)})")
