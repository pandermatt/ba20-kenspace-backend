import pytest

from evaluation.evaluate_model import calculate_purity, calculate_entropy
from models.clustered_data_structure import ClusteredStructure

cluster_id_genres_mapping = {
    121: {'Animation': 1, 'Comedy': 1, 'Family': 1},
    86: {'Adventure': 1, 'Fantasy': 1, 'Family': 1},
    25: {'Romance': 1, 'Comedy': 1},
    65: {'Comedy': 1, 'Drama': 1, 'Romance': 1},
    90: {'Comedy': 1},
    11: {'Action': 1, 'Crime': 1, 'Drama': 1, 'Thriller': 1},
    106: {'Comedy': 1, 'Romance': 1},
    24: {'Action': 1, 'Adventure': 1, 'Drama': 1, 'Family': 1},
    180: {'Action': 1, 'Adventure': 1, 'Thriller': 1},
    183: {'Adventure': 1, 'Action': 1, 'Thriller': 1}
}
data = [
    ClusteredStructure('Toy Story', [], 121),
    ClusteredStructure('Jumanji', [], 86),
    ClusteredStructure('Grumpier Old Men', [], 25),
    ClusteredStructure('Waiting to Exhale', [], 65),
    ClusteredStructure('Father of the Bride Part II', [], 90),
    ClusteredStructure('Heat', [], 11),
    ClusteredStructure('Sabrina', [], 106),
    ClusteredStructure('Tom and Huck', [], 24),
    ClusteredStructure('Sudden Death', [], 180),
    ClusteredStructure('GoldenEye', [], 183)
]

movie_title_genres_mapping = {'Toy Story': ['Animation', 'Comedy', 'Family'],
                              'Jumanji': ['Adventure', 'Fantasy', 'Family'],
                              'Grumpier Old Men': ['Romance', 'Comedy'],
                              'Waiting to Exhale': ['Comedy', 'Drama', 'Romance'],
                              'Father of the Bride Part II': ['Comedy'],
                              'Heat': ['Action', 'Crime', 'Drama', 'Thriller'],
                              'Sabrina': ['Comedy', 'Romance'],
                              'Tom and Huck': ['Action', 'Adventure', 'Drama', 'Family'],
                              'Sudden Death': ['Action', 'Adventure', 'Thriller'],
                              'GoldenEye': ['Adventure', 'Action', 'Thriller']}


def test_calculate_purity():
    assert calculate_purity(cluster_id_genres_mapping, data, movie_title_genres_mapping) == pytest.approx(1)
    assert calculate_purity(
        {
            121: {'Animation': 1, 'Comedy': 1, 'Family': 1, 'Adventure': 1, 'Fantasy': 1},
        },
        [
            ClusteredStructure('Toy Story', [], 121),
            ClusteredStructure('Jumanji', [], 121),
        ],
        {
            'Toy Story': ['Animation', 'Comedy'],
            'Jumanji': ['Adventure', 'Fantasy', 'Family'],
        }) == pytest.approx(0.5)


def test_calculate_entropy():
    assert calculate_entropy(cluster_id_genres_mapping, data, movie_title_genres_mapping,
                             all_labels=False) == pytest.approx(0)
    assert calculate_entropy(cluster_id_genres_mapping, data, movie_title_genres_mapping,
                             all_labels=True) == pytest.approx(0)
    cluster_id = {
        121: {},
    }
    data_2 = [
        ClusteredStructure('Toy Story', [], 121),
        ClusteredStructure('Jumanji', [], 121),
    ]
    genre = {
        'Toy Story': ['Animation', 'Comedy', 'Family'],
        'Jumanji': ['Adventure', 'Fantasy'],
    }
    assert calculate_entropy(cluster_id, data_2, genre, all_labels=False) == pytest.approx(1)
    assert calculate_entropy(cluster_id, data_2, genre, all_labels=True) == pytest.approx(1.0766913)
    data_3 = [
        ClusteredStructure('Toy Story', [], 121),
        ClusteredStructure('Toy Story 2', [], 121),
        ClusteredStructure('Toy Story 3', [], 121),
        ClusteredStructure('Jumanji', [], 121),
    ]
    genre_3 = {
        'Toy Story': ['Animation', 'Comedy', 'Family'],
        'Toy Story 2': ['Animation', 'Comedy', 'Family'],
        'Toy Story 3': ['Animation', 'Comedy', 'Family'],
        'Jumanji': ['Adventure', 'Fantasy'],
    }
    assert calculate_entropy(cluster_id, data_3, genre_3, all_labels=True) == pytest.approx(0.832857131)
    assert calculate_entropy(cluster_id, data_3, genre_3, all_labels=False) == pytest.approx(0.81127812)
    assert calculate_entropy(
        cluster_id,
        [
            ClusteredStructure('Toy Story', [], 121),
            ClusteredStructure('Jumanji', [], 121),
            ClusteredStructure('Pascal', [], 121),
        ],
        {
            'Toy Story': ['Fantasy', 'Advent'],
            'Jumanji': ['Fantasy', 'Advent'],
            'Pascal': ['Fantasy', 'Advent'],
        }) == pytest.approx(0)