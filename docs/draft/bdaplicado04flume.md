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

Es un sistema confiable y distribuido para recopilar, agregar y mover datos masivos.
Algunas de sus características son:
Diseño flexible basado en flujos de datos de transmisión.
Resistente a fallos y robusto con múltiples conmutaciones por error y  mecanismos de recuperación.
Lleva datos desde origen a destino: incluidos HDFS y HBASE

Componentes:
Evento:  Son las unidades de datos transportadas por el agente flume (array de bytes).
Agente: Contenedor para alojar subcomponentes que permiten mover los eventos
Source: Receptor de eventos
Interceptor: Transformador de eventos
Channel: Buffer de eventos
Sink: Toma eventos del canal y los transmite hacia el siguiente componente

## Sqoop

Permite transferir grandes volumenes de datos de manera eficiente entre Hadoop y gestores de datos estructurados, como Bases de datos relacionales 

Sqoop ofrece conectores para integrar Hadoop con otros sistemas, como por ejemplo Oracle o SqlServer

https://www.geeksforgeeks.org/overview-of-sqoop-in-hadoop/

## Referencias

* aaa
