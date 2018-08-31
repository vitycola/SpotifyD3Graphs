SpotifyD3Graphs

El script crawler.py obtiene las canciones de una playlist de la API de Spotify y vuelca el contenido en data/data.json

El script graphAnalysis.py recibe como entrada el json anterior y calcula sus métricas del grafo (closeness, betweeness etc..). Vuelca el resultado del grafo en data/graph_analyzed.json

d3Rock.html realiza una visualizacióninteractiva del grafo plasmado en data/graph_analyzed.json apoyándose en la librería D3.js