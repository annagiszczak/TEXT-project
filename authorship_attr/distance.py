from collections import Counter
import pandas as pd


def compute_author_ngram_frequencies(df: pd.DataFrame, n: int = 2) -> dict:
    freqs = {}  # dane dla każdego autora

    for author, group in df.groupby("author", sort=False):
        words = group["lemma"].tolist()
        ngrams = [" ".join(words[i:i+n]) for i in range(len(words) - n + 1)]
        author_ngram_counts = Counter(ngrams)
        total_ngrams_author = sum(author_ngram_counts.values())
        freqs[author] = {}
        for ngram, count in author_ngram_counts.items():
            freqs[author][ngram] = count / total_ngrams_author

    return freqs

def cng_distance(freq_x: dict, freq_y: dict, L: int = 1000) -> float:
    
    # Sortujemy n-gramy w freq_x i freq_y malejąco wg częstości
    top_x = sorted(freq_x.items(), key=lambda x: x[1], reverse=True)[:L]
    top_y = sorted(freq_y.items(), key=lambda x: x[1], reverse=True)[:L]
    # Wyciągamy same n-gramy (bez częstości) i robimy z nich set
    top_x_ngrams = set([ng[0] for ng in top_x])
    top_y_ngrams = set([ng[0] for ng in top_y])
    
    # Unia najczęstszych n-gramów
    union_ngrams = top_x_ngrams.union(top_y_ngrams)
    
    distance = 0.0
    for g in union_ngrams:
        fxg = freq_x.get(g, 0.0)
        fyg = freq_y.get(g, 0.0)
        denominator = fxg + fyg
        if denominator != 0:
            numerator = 2 * (fxg - fyg)
            distance += (numerator / denominator) ** 2
    
    return distance

def calculate_distances(freqs):
    authors = list(freqs.keys())
    distances = {}
    L_chosen = 200

    for i in range(len(authors)):
        for j in range(i+1, len(authors)):
            a1 = authors[i]
            a2 = authors[j]
            dist = cng_distance(freqs[a1], freqs[a2], L=L_chosen)
            distances[(a1, a2)] = dist
    return distances
