
## Ambari

[Ambari](https://ambari.apache.org) es un producto que simplifica la gestión de Hadoop y permite configurar, instalar y monitorizar un cluster Hadoop.

La instalación que tenemos no nos sirve, ya que Ambari crea un nueva instalación tanto de Hadoop y YARN. Para su instalación desde cero, es recomendable seguir las indicaciones de su [página oficial](https://cwiki.apache.org/confluence/display/AMBARI/Installation+Guide+for+Ambari+2.7.5).

Nosotros vamos a resumir los pasos recomendados. Para instalar en Ubuntu el servidor Amabari únicamente deberíamos ejecutar el siguiente comando (también va a instalar PostgreSQL donde almacenará todos los metadados sobre la configuración de Ambari):

``` bash
apt-get install ./ambari-server*.deb   # Instalará también PostgreSQL
```

Una vez instalado, solo queda configurarlo (como usuario con permisos *root*):

``` bash
ambari-server setup
```

Y finalmente arrancarlo:

``` bash
ambari-server start
```

Ahora tocaría instalar los agentes en cada uno de los nodos, así como configurarlo. Como vamos a trabajar con un modelo pseudodistribuido, en nuestro caso no vamos a hacer ese paso.

Finalmente, accederemos al interfaz gráfico con el usuario `admin/admin` y acceder http://localhost:8080.

FIXME: captura

Al crear un cluster, Ambari se basa en los stacks de HortonWorks HDP para realizar la instalación de Hadoop.

FIXME: captura

Revisar nodos

Instalar SSH en usuario root