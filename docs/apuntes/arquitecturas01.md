# Arquitecturas Big Data

Ya sabemos en qué consiste Big Data, y que dentro de sus 5V, dos de las más importantes son el *volumen* y la *velocidad*. Para cumplir con estas necesidades, necesitamos una infraestructura que dote a nuestras aplicaciones de toda la potencia y robustez necesarias.

En esta sesión no vamos a entrar al detalle de ninguna tecnología, ya que el stack de herramientas es muy amplio y en constante crecimiento. A lo largo del curso iremos conociendo las distintas herramientas y aprenderemos cómo y cuándo utilizarlas.

## Características

Todas las arquitecturas que diseñemos / utilicemos deben cumplir las siguientes características:

* *Escalabilidad*: permite aumentar fácilmente las capacidades de procesamiento y almacenamiento de datos.
* *Tolerancia a fallos*: garantiza la disponibilidad del sistema, aunque se produzcan fallos en algunas de las máquinas, evitando la pérdida de datos.
* *Datos distribuidos*: los datos deben estar almacenados entre diferentes máquinas evitando así el problema de almacenar grandes volúmenes de datos en un único nodo central.
* *Procesamiento distribuido*: el tratamiento de los datos se realiza entre diferentes máquinas para mejorar los tiempos de ejecución y dotar al sistema de escalabilidad.
* *Localidad del dato*: los datos a trabajar y los procesos que los tratan deben estar cerca, para evitar las transmisiones por red que añaden latencias y aumentan los tiempos de ejecución.

Antes de conocer las arquitecturas más empleados, es conveniente tener presente siempre cuál es el objetivo que debe cumplir nuestra solución. Es muy fácil caer en la sobreingeniería y montar una arquitectura con una amalgama de productos que luego son difíciles de configurar y mantener.

## Tipos de arquitecturas

Debido a que las empresas disponen de un volumen de datos cada vez mayor y la necesidad de analizarlos y obtener valor de ellos lo antes posible, surge la necesidad de definir nuevas arquitecturas para cubrir casos de uso distintos a los que había hasta el momento.

Las arquitecturas más comunes en estos proyectos son principalmente dos: *Lambda* y *Kappa*. La principal diferencia entre ambas son los flujos de tratamiento de datos que intervienen.

Un par de conceptos que tenemos que definir antes de ver las características de ambas, son el procesamiento batch y el procesamiento en streaming.

### Procesamiento Batch

Batch hace referencia a un proceso en el que intervienen un conjunto de datos y que tiene un inicio y un fin en el tiempo. También se le conoce como procesamiento por lotes y se ejecuta sin control directo del usuario.

Por ejemplo, si tenemos una aplicación que muestra el total de casos COVID que hay en cada ciudad, en vez de realizar el cálculo sobre el conjunto completo de los datos, podemos realizar una serie de operaciones que hagan esos cálculos y los almacenen en tablas temporales (por ejemplo, mediante `INSERT ... SELECT`), de manera que si queremos volver a realzar la consulta sobre todos los datos, accederíamos a los datos ya calculados de la tabla temporal. El problema es que este cálculo necesita actualizarse, por ejemplo, de manera diaria, y de ahí que haya que rehacer todas las tablas temporales.

Es el procesamiento que se ha realizado desde los inicios del trabajo con datos, tanto a nivel de bases de datos como con *Data Warehouses*.

De la mano del procesamiento *batch* se ha implantado el ecosistema Hadoop con todas las herramientas que abarcan un proceso ETL (extración, transformación y carga de los datos). Estos conceptos los trabajaremos más adelante.

### Procesamiento en Streaming

Un procesamiento es de tipo *streaming* cuando está continuamente recibiendo y tratando nueva información según va llegando sin tener un fin en lo referente al apartado temporal.

Este procesamiento se relaciona con el análisis en tiempo real.

!!! warning
    No confundir tiempo real con inmediatez.
    En informática, un sistema de tiempo real es aquel que responde en un periodo de tiempo finito, normalmente muy pequeño, pero no tiene por qué ser instantaneo.

## Arquitectura Lambda

Representada mediante la letra griega, apareció en el año 2012 y se atribuye a *Nathan Marz*.

!!! note "Nathan Marz"
    La definió en base a su experiencia en sistemas de tratamiento de datos distribuidos durante su etapa como empleado en las empresas Backtype y Twitter, y está inspirada en su artículo *How to beat the CAP theorem*.

Su objetivo era tener un sistema robusto tolerante a fallos, tanto humanos como de hardware, que fuera linealmente escalable y que permitiese realizar escrituras y lecturas con baja latencia. Para ello, se 
compone de tres capas:

* Capa *batch*: se encarga de (a) gestionar los datos históricos y (b) recalcular los resultados, por ejemplo, de los modelos de *machine learning*. De manera específica, la capa *batch* recibe los datos, los combina con el historico existente y recalcula los resultados iterando sobre todo el conjunto de datos combinado. Así pues, este capa opera sobre el conjunto completo y permite que el sistema produzca los resultados más precisos. Sin embargo, esto conlleva un coste de alta latencia debido a los requisitos de tiempo de computación.
* Capa de *streaming* / *speed*: sirve para ofrecer resultados con muy baja latencia, cercano al tiempo real. Este capa recibe los datos y realizar modificaciones incrementales sobre los resultados de la capa *batch*. Gracias a los algoritmos incrementales implementados en esta capa, se consigue reducir el coste computacional de manera considerable.
* Capa de *serving*: permite la consulta de los resultados enviados desde las dos capas anteriores.

Podemos ver un esquema de la arquitectura en el siguiente gráfico:

<https://www.paradigmadigital.com/techbiz/de-lambda-a-kappa-evolucion-de-las-arquitecturas-big-data/>

![Arquitectura Lambda](../imagenes/arq/01lambda.png)

El flujo de trabajo es el siguiente:

1. La nueva información recogida por el sistema se envía tanto a la capa *batch* como a la capa de *streaming* (*Speed Layer* en la imagen anterior).
2. En la capa *batch* (*Batch Layer*) se gestiona la información en crudo, es decir, sin modificar. Los datos nuevos se añaden a los ya existentes. Seguidamente se hace un tratamiento mediante un proceso *batch* cuyo resultado serán las *Batch Views*, que se usarán en la capa que sirve los datos para ofrecer la información ya transformada al exterior.
3. La capa que sirve los datos (*Serving Layer*) indexa las *Batch Views* generadas en el paso anterior de forma que puedan ser consultadas con tiempos de respuesta muy bajos.
4. La capa de *streaming* compensa la alta latencia de las escrituras que ocurre en la *serving layer* y solo tiene en cuenta los datos nuevos (incrementos entre los procesos batch y el momento actual).
5. Finalmente, combinando los resultados de las *Batch Views* y de las vistas en tiempo real (*Real-time Views*), se construye la respuesta a las consultas realizadas.

<https://www.ericsson.com/en/blog/2015/11/data-processing-architectures--lambda-and-kappa>

## Arquitectura Kappa

<https://www.treelogic.com/es/Arquitectura_Kappa.html>

El término Arquitectura Kappa, representada por la letra , fue introducido en 2014 por Jay Kreps en su artículo [Questioning the Lambda Architecture](https://www.oreilly.com/radar/questioning-the-lambda-architecture/).

En él señala los posibles puntos “débiles” de la Arquitectura Lambda y cómo solucionarlos mediante una evolución. Su propuesta consiste en eliminar la capa batch dejando solamente la capa de streaming.

Esta capa, a diferencia de la de tipo batch, no tiene un comienzo ni un fin desde un punto de vista temporal y está continuamente procesando nuevos datos a medida que van llegando.

Como un proceso batch se puede entender como un stream acotado, podríamos decir que el procesamiento batch es un subconjunto del procesamiento en streaming.

Esta evolución consiste en una simplificación de la Arquitectura Lambda, en la que se elimina la capa batch y todo el procesamiento se realiza en una sola capa denominada de tiempo real o Real-time Layer, dando soporte a procesamientos tanto batch como en tiempo real.

![Arquitectura Kappa](../imagenes/arq/01kappa.png)

Podemos decir que sus cuatro pilares principales son los siguientes:

* Todo es un stream: las operaciones batch son un subconjunto de las operaciones de streaming, por lo que todo puede ser tratado como un stream.
* Los datos de partida no se modifican: los datos son almacenados sin ser transformados y las vistas se derivan de ellos. Un estado concreto puede ser recalculado puesto que la información de origen no se modifica.
* Solo existe un flujo de procesamiento: puesto que mantenemos un solo flujo, el código, el mantenimiento y la actualización del sistema se ven reducidos considerablemente.
* Posibilidad de volver a lanzar un procesamiento: se puede modificar un procesamiento concreto y su configuración para variar los resultados obtenidos partiendo de los mismos datos de entrada.

Como requisito previo a cumplir, se tiene que garantizar que los eventos se leen y almacenan en el orden en el que se han generado. De esta forma, podremos variar un procesamiento concreto partiendo de una misma versión de los datos.

## Casos de uso

¿Qué arquitectura se adapta mejor a nuestro problema? ¿Cúal encaja mejor en nuestro modelo de negocio?.

<https://www.ericsson.com/en/blog/2015/11/data-processing-architectures--lambda-and-kappa-examples>

Por lo general, no existe una única respuesta. La arquitectura *Lambda* es más versátil y es capaz de cubrir un mayor número de casos, muchos de ellos que requieren incluso procesamiento en tiempo real.

Una pregunta que debemos plantearnos para poder decidir es, ¿el análisis y el procesamiento que vamos a realizar en las capas batch y streaming es el mismo? En ese caso la opción más acertada sería la Arquitectura Kappa.

Como ejemplo real de esta arquitectura podríamos poner un sistema de geolocalización de usuarios por la cercanía a una antena de telefonía móvil. Cada vez que se aproximase a una antena que le diese cobertura se generaría un evento. Este evento se procesaría en la capa de streaming y serviría para pintar sobre un mapa su desplazamiento respecto a su posición anterior.

Sin embargo, en otras ocasiones necesitaremos acceder a todo el conjunto de datos sin penalizar el rendimiento por lo que la Arquitectura Lambda puede ser más apropiada e incluso más fácil de implementar.

También nos inclinaremos hacia una Arquitectura Lambda si nuestros algoritmos de batch y streaming generan resultados muy distintos, como puede suceder con operaciones de procesamiento pesado o en modelos de *Machine Learning*.

Un caso de uso real para una arquitectura Lambda podría ser un sistema que recomiende libros en función de los gustos de los usuarios. Por un lado, tendría una capa batch encargada de entrenar el modelo e ir mejorando las predicciones; y por otro, una capa streaming capaz de encargarse de las valoraciones en tiempo real.

Para finalizar, hay que destacar lo rápido que evolucionan los casos de uso que queremos cubrir con nuestras soluciones Big Data, y eso supone que hay que adaptarse a ellos lo antes posible.

Cada problema a resolver tiene unos condicionantes particulares y en muchos casos habrá que evolucionar la arquitectura que estábamos utilizando hasta el momento, o como se suele decir: “renovarse o morir”.

## Buenas prácticas

* En la ingesta de datos: evalúa los tipos de fuentes de datos, no todas las herramientas sirven para cualquier fuente, y en algún caso te encontrarás que lo mejor es combinar varias herramientas para cubrir todos tus casos.
* En el procesamiento: evalúa si tu sistema tiene que ser streaming o batch. Algunos sistemas que no se definen como puramente streaming utilizan lo que denominan micro-batch que suele dar respuesta a problemas que en el uso cotidiano del lenguaje se denomina como streaming.
* En la monitorización: ten en cuenta que estamos hablando de multitud de herramientas y que su monitorización, control y gestión puede llegar a ser muy tedioso, por lo que independientemente de que te decidas por instalar un stack completo o por instalar herramientas independientes y generar tu propia arquitectura combusto, te recomiendo además que utilices herramientas para controlar, monitorizar y gestionar tu arquitectura, esto te facilitará y centralizará todo este tipo de tareas.
* Algunas decisiones que tenemos que tomar a la hora de elegir la arquitectura son:
    * Enfoca tus casos de uso, cuando tengas tus objetivos claros sabrás que debes potenciar en tu arquitectura. ¿Volumen, variedad, velocidad?
    * Define tu arquitectura: ¿batch o streaming? ¿Realmente necesitas que tu arquitectura soporte streaming?
    * Evalúa tus fuentes de datos: ¿Cómo de heterogéneas son tus fuentes de datos? ¿soportan las herramientas elegidas todos los tipos de fuentes de datos que tienes?

## Arquitectura en la nube



### Marco de buena arquitectura (WAF)

El marco de buena arquitectura ([*Well-Architected Framework*](<https://docs.aws.amazon.com/es_es/wellarchitected/latest/framework/the-five-pillars-of-the-framework.html>) - WAF) es una guía diseñada para ayudarnos a crear la infraestructura con más seguridad, alto rendimiento, resiliencia y eficacia posibles para nuestras aplicaciones y cargas de trabajo en la nube. Proporciona un conjunto de preguntas y prácticas recomendadas que facilitan la evaluación e implementación de nuestras arquitecturas en la nube.

AWS desarrolló el Marco de Buena Arquitectura después de revisar miles de arquitecturas de clientes en AWS.

Se organiza en cinco pilares que estudiaremos a continuación: excelencia operativa, seguridad, fiabilidad, eficacia del rendimiento y optimización de costes.

Cada pilar incluye un conjunto de principios de diseño y áreas de prácticas recomendadas. Dentro de cada área de prácticas recomendadas, hay un conjunto de preguntas básicas. Para cada pregunta se proporciona un poco de contexto y una lista de prácticas recomendadas.

#### Excelencia operativa

Se centra en la habilidad de ejecutar y monitorizar sistemas para proporcionar valor de negocio y mejorar los procesos y procedimientos de soporte de manera continua. Entre los temas clave se incluyen la administración y automatización de los cambios, la respuesta a eventos y la definición de estándares para administrar correctamente las operaciones diarias.

Comprende la capacidad para dar soporte al desarrollo y ejecutar cargas de trabajo de manera eficaz, obtener información acerca de las operaciones y mejorar continuamente el soporte a los procesos y los procedimientos para ofrecer valor de negocio.

Realizar operaciones como código: en la nube, puede aplicar la misma disciplina de ingeniería que utiliza para el código de aplicaciones en todo el entorno. Puede definir toda la carga de trabajo (aplicaciones, infraestructura) como código y actualizarla con código. Puede implementar sus procedimientos operativos como código y automatizar la ejecución si los activa en respuesta a eventos. Si realiza operaciones como código, limita la posibilidad de error humano y habilita respuestas coherentes a los eventos.

Realizar cambios pequeños, reversibles y frecuentes: diseñe cargas de trabajo para permitir que los componentes se actualicen de forma regular. Realice cambios en incrementos pequeños que puedan revertirse si se producen errores (sin afectar a los clientes cuando sea posible).

Mejorar los procedimientos operativos con frecuencia: a medida que utilice los procedimientos operativos, busque oportunidades para mejorarlos. Mientras su carga de trabajo evoluciona, haga que sus procedimientos también lo hagan de forma adecuada. Configure días de práctica regulares para revisar todos los procedimientos y validar que sean efectivos y que los equipos los conozcan.

Anticipar los errores: realice ejercicios “premortem” para identificar los posibles orígenes de errores de manera que se puedan eliminar o mitigar. Pruebe las situaciones de error y compruebe que entiende sus efectos. Pruebe los procedimientos de respuesta para asegurarse de que sean efectivos y que los equipos conozcan su ejecución. Configure días de práctica con regularidad para probar las respuestas de la carga de trabajo y del equipo a eventos simulados.

Aprender de todos los errores operativos: impulse las mejoras a partir de las lecciones aprendidas de todos los eventos y los errores operativos. Comparta lo aprendido con los equipos y toda la organización.

#### Seguridad

#### Fiabilidad

#### Eficiencia del rendimiento

#### Optimización de costes


#### Fiabilidad y disponibilidad

### AWS Trusted Advisor


## Gestión del escalado y la monitorización

### Monitorización

Al operar en la nube, es importante llevar un seguimiento de las actividades, porque probablemente haya un coste asociado a cada una de ellas. AWS ayuda a monitorizar, registrar e informar sobre el uso de sus servicios proporcionando herramientas para hacerlo.

Así pues, AWS ofrece los siguientes servicios relacionados con la monitorización:

* [Amazon *CloudTrail*](https://aws.amazon.com/es/cloudtrail/): Servicio que registra cada acción que se lleva a cabo en la cuenta de AWS por motivos de seguridad. Esto significa que CloudTrail registra cada vez que alguien carga datos, ejecuta un código, crea una instancia de EC2 o realiza cualquier otra acción.
* [Amazon *Cloudwatch*](https://aws.amazon.com/es/cloudwatch/): Servicio de monitorización de los recursos de AWS y las aplicaciones que ejecuta en AWS. *CloudTrail* registra actividades, mientras que *CloudWatch* las monitoriza. Así pues, *CloudWatch* vigila que los servicios *cloud* se ejecutan si problema y ayuda a no utilizar ni más ni menos recursos de lo esperado, lo que es importante para el seguimiento del presupuesto.
* [AWS *Config*](https://aws.amazon.com/es/config/): Servicio que permite analizar, auditar y evaluar las configuraciones de los recursos de AWS. AWS Config monitoriza y registra de manera continua las configuraciones de recursos de AWS y permite automatizar la evaluación de las configuraciones registradas con respecto a las deseadas.
* [Amazon SNS (*Amazon Simple Notification Service*)](https://aws.amazon.com/es/sns/): herramienta que permite enviar textos, correos electrónicos y mensajes a otros servicios en la nube y enviar notificaciones al cliente de varias formas desde la nube.

### Ejemplo Cloudwatch

En el siguiente ejemplo vamos a crear una alarma de *Cloudwatch* para enviar una notificación con la cuenta haya gastado una cierta cantidad de dinero. La alarma envía un mensaje a Amazon SNS para posteriormente enviar un correo electrónico.

El primer paso es crear y subscribirse a un tema (*topic*) SNS. Un tema actúa como un canal de comunicación donde se recibes los mensajes de las alertas y eventos.

Para ello, dentro del servicio SNS, crearemos un tema al que llamaremos `AlertaSaldo`.

<figure style="align: center;">
    <img src="../imagenes/arq/01cloudwatch1.png">
    <figcaption>Cloudwatch - Creación del tema</figcaption>
</figure>

A continuación, vamos a crear una subscripción a ese tema para que cuando se recibe una mensje, lo redirijamos a nuestro teléfono o correo electrónico.

Para ello, dentro de la sección de subscripciones, crearemos una subscripción. En el ARN pondremos el tema `AlertaSaldo` que acabamos de crear, y en el protocolo, vamos a seleccionar *Correo electrónico*. Finalmente, en el punto de enlace, definimos el email que recibirá la alerta. En este momento, Amazon enviará un email a la cuenta que hayamos indicado para confirmar los datos.

<figure style="align: center;">
    <img src="../imagenes/arq/01cloudwatch2.png">
    <figcaption>Cloudwatch - Creación de la subscripción</figcaption>
</figure>

El siguiente paso es crear la alarma en *Cloudwatch*. Para ello, una vez dentro de *Cloudwatch*, dentro de la opción de Alarmas, al crear una nueva, tendremos que elegir la métrica, que en nuestro caso seleccionaremos Facturación -> Cargo total estimado.
En la siguiente pantalla, en la sección de *Condiciones* ..... estático, e indicamos la condición que queremos que se active cuando es superior a 100.

<figure style="align: center;">
    <img src="../imagenes/arq/01cloudwatch3.png">
    <figcaption>Cloudwatch - Condiciones de la alarma</figcaption>
</figure>

En la sección de *Notificación*, tras elegir en modo alarma seleccionamos el tema SNS existente (en nuestro caso `AlertaSaldo`).

<figure style="align: center;">
    <img src="../imagenes/arq/01cloudwatch4.png">
    <figcaption>Cloudwatch - Notificaciones de la alarma</figcaption>
</figure>

Finalmente, le asignamos el nombre de `AlertaSaldoAlarma` y tras ver un resumen de todo los configurado, creamos la alarma.

De esta manera, cuando se supere el gasto de 100$, automáticamente nos enviará un email a la dirección que le hemos configurado.

## Escalado y Balanceo de carga

*Elastic Load Balancing* distribuye automáticamente el tráfico entrante de las aplicaciones entre varias instancias de Amazon EC2 Además, le permite obtener tolerancia a errores en las aplicaciones, ya que proporciona de forma constante la capacidad de balanceo de carga necesaria para dirigir el tráfico de estas.

Auto Scaling permite mantener la disponibilidad de las aplicaciones y aumentar o reducir automáticamente la capacidad de Amazon EC2 según las condiciones que se definan. Puede utilizar Auto Scaling para asegurarse de que se ejecuta la cantidad deseada de instancias de Amazon EC2. Con Auto Scaling, también se puede aumentar automáticamente la cantidad de instancias de Amazon EC2 durante los picos de demanda para mantener el rendimiento y reducir la capacidad durante los períodos de baja demanda con el objeto de minimizar los costos. Auto Scaling es adecuado para aplicaciones con patrones de demanda estables o para aquellas cuyo uso varía cada hora, día o semana.

### Elastic Load Balancing

### Amazon EC2 Auto Scaling

## Actividades

1. Si nos basamos en una arquitectura Lambda, clasifica los siguientes elementos:
2. Si nos basamos en una arquitectura Kappa, clasifica los siguientes elementos:
3. Realizar los módulos 9 (Arquitectura en la nube) y 10 (Monitoreo y escalado automático) del curso [ACF de AWS](https://awsacademy.instructure.com/courses/2243/).
4. (opcional) Cloudwatch_
    
Siga estos pasos para crear una ruta en su bucket de Amazon Simple Storage Service (Amazon S3).
https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-a-trail-using-the-console-first-time.html
Esto llevará un seguimiento de todas las acciones que se realizan con ese bucket de S3.

## Referencias

* [Arquitectura Big Data: ¿en qué consiste y para qué se utiliza?](https://www.unir.net/ingenieria/revista/arquitectura-big-data/)
* [Big Data Lambda Architecture - Nathan Marz](http://www.databasetube.com/database/big-data-lambda-architecture/)
* [What Is Lambda Architecture?](https://hazelcast.com/glossary/lambda-architecture/)
* [Arquitectura Lambda vs Arquitectura Kappa](http://i2ds.org/wp-content/uploads/2020/03/arquitecturalambdavsarquitecturakappa.pdf)
* [Laboratorios de Amazon sobre AWF](https://www.wellarchitectedlabs.com/)

<https://luminousmen.com/post/modern-big-data-architectures-lambda-kappa/>

<https://medium.com/dataprophet/4-big-data-architectures-data-streaming-lambda-architecture-kappa-architecture-and-unifield-d9bcbf711eb9>


* <https://docs.aws.amazon.com/es_es/whitepapers/latest/big-data-analytics-options/welcome.html>
