# Spark

*Spark* es un framework de computación en cluster similar a *MapReduce*, pero que en vez de almacenar los datos en un sistema de ficheros distribuidos o utilizar un sistema de gestión de recursos, lo hace en memoria. 

En el caso de tener la necesidad de almacenar los datos o gestionar los recursos, se apoya en sistemas ya existentes como *HDFS*, *YARN* o *Apache Mesos*. Por lo tanto, *Hadoop* y *Spark* son sistemas complementarios.

HOW DOES SPARK SOLVE THE PROBLEMS OF MAPREDUCE?
While we oversimplify things a bit for the sake of clarity, Spark creates a kind of shared
RAM memory between the computers of your cluster. This allows the different workers
to share variables (and their state) and thus eliminates the need to write the intermediate
results to disk. More technically and more correctly if you’re into that: Spark
uses Resilient Distributed Datasets (RDD), which are a distributed memory abstraction
that lets programmers perform in-memory computations on large clusters in a faulttolerant
way.1 Because it’s an in-memory system, it avoids costly disk operations.
THE DIFFERENT COMPONENTS OF THE SPARK ECOSYSTEM

Spark core provides a NoSQL environment well suited for interactive, exploratory
analysis. Spark can be run in batch and interactive mode and supports Python.
Spark has four other large components, as listed below and depicted in figure 5.5.
1 Spark streaming is a tool for real-time analysis.
2 Spark SQL provides a SQL interface to work with Spark.
3 MLLib is a tool for machine learning inside the Spark framework.
4 GraphX is a graph database for Spark. We’ll go deeper into graph databases in
chapter 7.

## Referencias

https://courses.cs.ut.ee/2021/cloud/spring/Main/Practice9

* aaa

