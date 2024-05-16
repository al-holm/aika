# Entwicklungsprozess

## 1. Beschreibung des Software-Entwicklungsprozesses

### Agile Entwicklung
Wir halten es für wichtig, auf Veränderungen reagieren zu können und folgen daher einer agilen Entwicklungsstrategie. 

Das Projekt wird in gleichmäßigen Iterationen, sogenannten Sprints, entwickelt. Jeder Sprint dauert zwei Wochen, in denen die im Backlog definierten Funktionalitäten implementiert werden. Am Ende jedes Sprints findet ein Reviewsession statt, in der reflektiert wird, wie der Sprint gelaufen ist, ob das Sprintziel erreicht wurde und das Backlog angepasst wird

Obwohl wir uns am Scrum-Prozess orientieren, verzichten wir auf die für Scrum typische strikte Rollenverteilung (Product Owner, Scrum Master, Entwicklungsteam), denn kein Teammitglied hat genug Erfahrung, um eine der Rollen komplett zu übernehmen. Stattdessen treffen wir alle rollenspezifischen Entscheidungen gemeinsam.

## 2. Anzuwendende Praktiken

- **Text-Driven Development (nicht für LLMs)**: Tests werden vor der eigentlichen Implementierung geschrieben. Der Code wird nur dann geschrieben, wenn ein Test fehlschlägt, und der Prozess wiederholt sich, bis alle Tests bestehen.
- **Refactoring**: Kontinuierliche Verbesserung des bestehenden Codes, um seine Struktur zu optimieren, ohne das externe Verhalten zu ändern. 
- **Code Reviews**: Jeder Pull-Request wird von einem oder mehreren Teammitgliedern überprüft, bevor er genehmigt wird
- **Inkrementelle Entwicklung**: Das Projekt wird schrittweise entwickelt, indem wir die Anwendungsfällen in der bestimmten Reihenfolge implementieren. 
- **Anwendungsfälle/User Stories**: Das Projekt ist in Anwendungsfälle gegliedert (siehe use_cases.md). Außerdem schreiben wir kürzere User Stories, die die Funktionen erfüllen müsse
- **Comment Style**: Um die Wartung und die Erweiterung des Codes zu erleichtern, benutzen wir einen für alle gültigen Kommentarstil: NumPy-Dokumentationsstil. Hier ist ein Beispiel für diesen Stil: 

def compute_statistics(data):
    
    """
    
    Compute the mean, median, and standard deviation of a dataset.

    Parameters
    ----------
    data : array_like
        Input array or object that can be converted to an array.

    Returns
    -------
    mean : float
        The mean of the dataset.
    median : float
        The median of the dataset.
    std_dev : float
        The standard deviation of the dataset.

    Raises
    ------
    ValueError
        If the input data is empty.

    Notes
    -----
    This function assumes that the input data is one-dimensional. If the input
    data is multidimensional, the function will raise a ValueError.

    Examples
    --------
    >>> import numpy as np
    >>> data = [1, 2, 3, 4, 5]
    >>> mean, median, std_dev = compute_statistics(data)
    >>> mean
    3.0
    >>> median
    3.0
    >>> std_dev
    1.4142135623730951
    """
    data = np.asarray(data)

    if data.size == 0:
        raise ValueError("Input data must not be empty")

    mean = np.mean(data)
    median = np.median(data)
    std_dev = np.std(data)

    return mean, median, std_dev
