# Clustering
Tópicos Especiales en Telemática - Proyecto 3

Realizado por:

* Andrés Felipe García Granados
* Cristian David Suaza Cárdenas
* Jeniffer María Palacio Sandoval

# Descripción

Algoritmo que permite agrupar documentos similares en un número de k clusters. Ésto se realiza utilizando el algoritmo [k-means](https://es.wikipedia.org/wiki/K-means) y la [distancia euclidiana](https://es.wikipedia.org/wiki/Distancia_euclidiana) como métrica de similitud entre los documentos.

# Recursos utilizados

  - Ubuntu 16.04.1
  - PyCharm Edu 4.0.2
  - Python 2.7
  - mpi4py 2.0.0
  - Dataset [Gutenberg](https://goo.gl/LL4CgA)
  
# Desarrollo

Se halla la distancia entre documentos por medio de la **distancia euclidiana**, la cual nos arroja un número que se interpreta asi: entre más cercano a cero significa que los documentos son más parecidos, y por el contrario, entre más alejado sea el resultado de cero quiere decir que los documentos son menos similares.

Luego se emplea el algoritmo **k-means**, el cual permite agrupar documentos similares en un grupo de *k* clusters.

Para paralelizar el código se utiliza la librería **mpi**, la cual nos ofrece varias funciones para el paso de mensajes entre diferentes procesadores.

# Ejecución

Por efectos en tiempo de ejecución, se utilizan como máximo 100 documentos del dataset de Gutenberg, sin embargo, puede encontrar el dataset completo en la referencia que se dejó anteriormente en el apartado de *Recursos utilizados*.

Para ver la soluciones a los problemas planteados debe ejecutar cada archivo por separado asi:

* Ejecutar el *subproblema1.py* para ver sólamente el resultado de la distancia euclidiana.

* Ejecutar el *subproblema2.py* para ver el resultado de **k-means** de forma serial.

* Ejecutar el *executor.sh* para ver el resultado de **k-means** de forma paralela.

En el [reporte técnico](https://github.com/PipeGarcia/st0263_clustering/tree/master/reporte_tecnico) puede encontrar una explicación más detallada en formato pdf de la implementación del algoritmo.