# Hadoop

Las nuevas tecnologías como *Hadoop* y *Spark* facilitan el trabajo y la gestión de un cluster de ordenadores. *Hadoop* puede escalar hasta miles de ordenadores creando un cluster con un almacenamiento con un orden de *petabytes* de información.

Estas tecnologías son las que realmente catalizan el *Big Data*.

*Apache Hadoop* (<http://hadoop.apache.org/>) es un *framework* que facilita el trabajo con un cluster de ordenadores. Sus características son:

* Confiable: crea múltiples copias de los datos de manera automática y, en caso de fallo, vuelve a desplegar la lógica de procesamiento.
* Tolerante a fallos: tras detectar un fallo aplica una recuperación automática.
* Escalable: los datos y su procesamiento se distribuyen sobre un cluster de ordenadores (escalado horizontal)
* Portable: se puede instalar en todo tipos de *hardware* y sistemas operativos.

## Componentes

El núcleo se compone de:

* un sistema de ficheros distribuidos (*HDFS*).
* un gestor de recursos para el manejo del cluster (*YARN*)
* un sistema para ejecutar programas distribuidos a gran escala (*MapReduce*)

Estos elementos permiten trabajar de casi la misma forma que si tuviéramos un sistema de fichero locales en nuestro ordenador personal, pero realmente los datos están repartidos entre miles de servidores.

Sobre este conjunto de herramientas existe un ecosistema "infinito" con tecnologías que facilitan el acceso, gestión y extensión del propio Hadoop.

![Ecosistema Hadoop](../imagenes/31hadoop-ecosystem01.jpg)

## MapReduce

Es el algoritmo que utiliza Hadoop para paralelizar las tareas. Un algoritmo MapReduce divide los datos, los procesa en paralelo, los reordena, combina y agrega de vuelta los resultados.

Sin embargo, este algoritmo no casa bien con el análisis interactivo o programas iterativos, ya que persiste los datos en disco entre cada uno de los pasos del mismo, lo que con grandes *datasets* conlleva una penalización en el rendimiento.

El siguiente gráfico muestra un ejemplo de una empresa de juguete que fabrica juguetes de colores. Cuando un cliente compra un juguete desde la página web, el pedido se almacena como un fichero en *Hadoop* con los colores de los juguetes adquiridos. Para averiguar cuantas unidades de cada color ha de preparar la fábrica, se emplea un algoritmo MapReduce para contar los colores:

![Ejemplo simplificado MapReduce](../imagenes/31map-reduce01.png)

Como sugiere el nombre, el proceso se divide principalmente en dos fases:

* Fase de mapeo (*Map*) — Los documentos se parten en pares de clave/valor. Hasta que no se reduzca, podemos tener muchos duplicados.
* Fase de reducción (*Reduce*) — Es en cierta medida similar a un *"group by"* de SQL. Las ocurrencias similares se agrupan, y dependiendo de la función de reducción, se puede crear un resultado diferente. En nuestro ejemplo queremos contar los colores, y eso es lo que devuelve nuestra función.

Realmente, es un proceso más complicado:

![Ejemplo fase a fase de conteo de colores](../imagenes/31map-reduce02.png)

1. Lectura de los ficheros de entrada.
2. Pasar cada linea de forma separada al mapeador.
3. El mapeador parsea los colores (claves) de cada fichero y produce un nuevo fichero para cada color con el número de ocurrencias encontradas (valor), es decir, mapea una clave (color) con un valor (número de ocurrencias).
4. Para facilitar la agregación, se ordenan las claves.
5. La fase de reducción suma las ocurrencias de cada color y genera un fichero por clave con el total de cada color.
6. Las claves se unen en un único fichero de salida.

!!! note "No es oro todo lo que reluce"
    Hadoop facilita el trabajo con grandes volúmenes de datos, pero montar un cluster funcional no es una cosa trivial. Existen gestores de clusters que hacen las cosas un poco menos incomódas (como son YARN o Apache Mesos), aunque la tendencia es utilizar una solución cloud que nos evita toda la instalación y configuración.

Tal como comentamos al inicio, uno de los puntos débiles de Hadoop es el trabajo con algoritmos iterativos, los cuales son fundamentales en la parte de IA. La solución es el uso del framework Spark, que mejora el rendimiento por una orden de magnitud.

## Referencias

* aaa
