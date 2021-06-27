# Spark

WHAT IS SPARK?
Spark is a cluster computing framework similar to MapReduce. Spark, however,
doesn’t handle the storage of files on the (distributed) file system itself, nor does it
handle the resource management. For this it relies on systems such as the Hadoop
File System, YARN, or Apache Mesos. Hadoop and Spark are thus complementary systems.
For testing and development, you can even run Spark on your local system.
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

* aaa
