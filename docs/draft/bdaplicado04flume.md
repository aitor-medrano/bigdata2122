# Flume / Sqoop

## Flume

Allá por el año 2010 se Cloudera presentó Flume, programa para tratamiento e ingesta de datos masivo. Esto daba la posibilidad de crear desarrollos complejos que permitieran el tratamiento de datos masivos creados en Tiempo Real.

En Real Time se utiliza en la etapa de Obtención de Datos (para conectarnos a fuentes de datos Online).

Su arquitectura es sencilla, pues tiene tres componentes principales, muy configurables:

Source: Fuente de origen de los datos
Channel: la vía por donde se tratarán los datos
Sink: persistencia/movimiento de los datos

Flume es sencillito apriori, el problema es cuando quieres utilizarlo para obtener datos de manera paralela (o multiplexada) y además te ves en la necesidad de crear tus propios Sinks, o tus propios interceptores. Entonces la cosa cambia y hay que dedicarle algo más de tiempo.

Muy recomendada como ayuda|compañero|alternativa a herramientas como Kettle.



## Sqoop

https://www.geeksforgeeks.org/overview-of-sqoop-in-hadoop/

## Referencias

* aaa
