# Almacenamiento en AWS

El almacenamiento en la nube, por lo general, es más confiable, escalable y seguro que los sistemas de almacenamiento tradicionales en las instalaciones.

El análisis de *Big Data*, el almacenamiento de datos, el Internet de las cosas (IoT), las bases de datos y las aplicaciones de copias de seguridad y archivo dependen de algún tipo de arquitectura de almacenamiento de datos.

El almacenamiento más básico es el que incluyen las propias instancias, también conocido como el **almacén de instancias**, o almacenamiento efímero, es un almacenamiento temporal que se agrega a la instancia de AmazonEC2.

!!! info "Almacenamiento de bloque o de objeto"
    AWS permite almacenar los datos en bloques o como objetos. Si el almacenamiento es en bloques, los datos se almacenan por trozos (bloques), de manera si se modifica una parte de los datos, solo se ha de modificar el bloque que lo contiene. En cambio, si el almacenamiento es a nivel de objeto, una modificación implica tener que volver a actualizar el objeto entero.  
    Esto provoca que el almacenamiento por bloque sea más rápido. En cambio, el almacenamiento de objetos es más sencillo y por tanto más barato.

AWS ofrece múltiples soluciones que vamos a revisar.

## Amazon EBS

*Amazon Elastic Block Store* (<https://aws.amazon.com/es/ebs/>) ofrece volúmenes de almacenamiento a nivel de bloque para utilizarlos con instancias de Amazon EC2.

Los beneficios adicionales incluyen la replicación en la misma zona de disponibilidad, el cifrado fácil y transparente, los volúmenes elásticos y las copias de seguridad mediante instantáneas.

!!! tip "Importante"
    AmazonEBS se puede montar en una instancia de AmazonEC2 solamente dentro de la misma zona de disponibilidad.

### Volúmenes

Los volúmenes de EBS proporcionan almacenamiento fuera de las instancias que persiste independientemente de la vida de la instancia. Son similares a discos virtuales en la nube. *AmazonEBS* ofrece tres tipos de volúmenes: SSD de uso general, SSD de IOPS provisionadas y magnéticos (HDD).

Los tres tipos de volúmenes difieren en características de rendimiento y coste, para ofrecer diferentes posibilidades según las necesidades de las aplicaciones.

FIXME: Completar

Para crear o configurar un volumen, dentro de las instancias EC2, en el menú lateral podemos ver las opciones de .....

![Volumenes](../imagenes/cloud/04volumen.png)

Los volúmenes de Amazon EBS están asociados a la red, y su duración es independiente a la vida de una instancia. Los volúmenes de Amazon EBS tienen un alto nivel de disponibilidad y de confianza, y pueden aprovecharse como particiones de arranque de instancias de Amazon EC2 o asociarse a una instancia de Amazon EC2 en ejecución como dispositivos de bloques estándar.

Cuando se utilizan como particiones de arranque, las instancias de Amazon EC2 pueden detenerse y, posteriormente, reiniciarse, lo que le permite pagar solo por los recursos de almacenamiento utilizados al mismo tiempo que conserva el estado de la instancia. Los volúmenes de Amazon EBS tienen durabilidad mucho mayor que los almacenes de instancias de Amazon EC2 locales porque los volúmenes de Amazon EBS se replican automáticamente en el backend (en una única zona de disponibilidad).

Los volúmenes de Amazon EBS ofrecen las siguientes características:

* Almacenamiento persistente: el tiempo de vida de los volúmenes es independiente de cualquier instancia de Amazon EC2.
* De uso general: los volúmenes de Amazon EBS son dispositivos de bloques sin formato que se pueden utilizar en cualquier sistema operativo.
* Alto rendimiento: los volúmenes de Amazon EBS son iguales que las unidades de Amazon EC2 locales o mejores que ellas.
* Nivel de fiabilidad alto: los volúmenes de Amazon EBS tienen redundancia integrada dentro de una zona de disponibilidad.
* Diseñados para ofrecer resiliencia: la AFR (tasa anual de errores) de Amazon EBS oscila entre 0,1 % y 1 %.
* Tamaño variable: los tamaños de los volúmenes varían entre 1 GB y 16 TB.
* Fáciles de usar: los volúmenes de Amazon EBS se pueden crear, asociar, almacenar en copias de seguridad, restaurar y eliminar fácilmente.

Solo una instancia de AmazonEC2 a la vez puede montarse en un volumen de Amazon EBS.

### Instantáneas

Sin embargo, para los que quieran aún más durabilidad, con Amazon EBS es posible crear instantáneas uniformes puntuales de los volúmenes, que luego se almacenan en Amazon Simple Storage Service (Amazon S3) y se replican automáticamente en varias zonas de disponibilidad. Estas instantáneas se pueden utilizar como punto de partida para nuevos volúmenes de Amazon EBS y permiten proteger la durabilidad de sus datos a largo plazo. También puede compartirlas fácilmente con colegas y otros desarrolladores de AWS.

Cuando lo desee, podrá crear una cantidad ilimitada de instantáneas uniformes de un momento específico de los volúmenes de Amazon EBS. Las instantáneas de Amazon EBS se almacenan en Amazon S3 con un alto nivel de durabilidad. Se pueden crear volúmenes de Amazon EBS nuevos a partir de instantáneas para clonar o restaurar copias de seguridad. Las instantáneas de Amazon EBS también pueden compartirse fácilmente entre usuarios de AWS o copiarse entre regiones de AWS.

## Amazon S3

AmazonS3 es una forma de almacenamiento persistente en la cual cada archivo se convierte en un objeto y está disponible a través de un localizador uniforme de recursos (URL). Además, se puede acceder a este servicio desde cualquier lugar.

AmazonS3 (<https://aws.amazon.com/es/s3/>) es un servicio de almacenamiento de objetos creado para almacenar y recuperar cualquier cantidad de datos desde cualquier ubicación: sitios web y aplicaciones móviles, aplicaciones corporativas y datos de sensores o dispositivos de Internet de las cosas (IoT).

## Amazon EFS

AmazonEFS (<https://aws.amazon.com/es/efs/>) implementa almacenamiento para las instancias EC2 a las que pueden acceder varias máquinas virtuales de forma simultánea. Se ha implementado como un sistema de archivos de uso compartido que utiliza el protocolo de sistemas de archivos de red (NFS).

AmazonEFS es un sistema de archivos de uso compartido que varias instancias de AmazonEC2 pueden montar al mismo tiempo.

Amazon Elastic File System (AmazonEFS) proporciona un almacenamiento de archivos simple, escalable y elástico para utilizarlo con los servicios de AWS y los recursos disponibles en las instalaciones. Ofrece una interfaz sencilla que le permite crear y configurar sistemas de archivos de forma rápida y simple. AmazonEFS está diseñado para escalar de manera dinámica bajo demanda sin interrumpir las aplicaciones, por lo que se ampliará y reducirá de forma automática a medida que agregue o elimine archivos. Está diseñado para que sus aplicaciones dispongan del almacenamiento que necesiten, cuando lo necesiten.

AmazonEFS proporciona almacenamiento de archivos en la nube que resulta ideal para bigdata y análisis, flujos de trabajo de procesamiento multimedia, administración de contenido, servidores web y directorios principales.

AmazonEFS escala de manera ascendente o descendente a medida que se agregan o eliminan archivos y solo requiere pago por lo que se utiliza.

AmazonEFS es un servicio completamente administrado al que se puede acceder desde la consola, una API o la CLI de AWS.

## Amazon S3 Glacier

AmazonS3 Glacier sirve para el almacenamiento en frío de datos a los que no se accede con frecuencia (por ejemplo, cuando necesita almacenamiento de datos a largo plazo por motivos de archivo o conformidad).

Amazon S3 Glacier (<https://aws.amazon.com/es/s3/glacier/>) es un servicio de almacenamiento en la nube seguro, duradero y de muy bajo costo para archivar datos y realizar copias de seguridad a largo plaz

## Amazon Elastic File System (Amazon EFS)

## Arquitecturas en la nube

Módulo 9 Introducción
Sección 1: Principios de diseño del marco de buena arquitectura de AWS
External Tool
Sección 1: Principios de diseño del marco de buena arquitectura de AWS
Sección 2: Excelencia operativa
External Tool
Sección 2: Excelencia operativa
Sección 3: Seguridad
External Tool
Sección 3: Seguridad
Sección 4: Fiabilidad
External Tool
Sección 4: Fiabilidad
Sección 5: Eficiencia del rendimiento
External Tool
Sección 5: Eficiencia del rendimiento
Sección 6: Optimización de costos
External Tool
Sección 6: Optimización de costos
Sección 7: Fiabilidad y disponibilidad
External Tool
Sección 7: Fiabilidad y disponibilidad
Sección 8: AWS Trusted Advisor
External Tool
Sección 8: AWS Trusted Advisor
Módulo 2 Conclusión
External Tool
Módulo 2 Conclusión
Student Guide
External Tool
Student Guide
Módulo 9 Evaluación de conocimientos
Assignment
Módulo 9 Evaluación de conocimientos

## Actividades

1. Realizar los módulo 7 (Almacenamiento) y del curso [ACF de AWS](https://awsacademy.instructure.com/courses/2243/).

## Referencias

* aaa
