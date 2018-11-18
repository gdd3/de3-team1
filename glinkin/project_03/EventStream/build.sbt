name := "EventStream"
version := "1.0"
scalaVersion := "2.11.12"

exportJars := true
assemblyJarName in assembly := s"${name.value}-${version.value}.jar"

resolvers += "Maven Central" at "http://central.maven.org/maven2/"

libraryDependencies ++= {
  val sparkVersion = "2.3.1"
  val kafkaVersion = "1.0.1"
  val confluentVersion = "3.1.1"
  Seq(
    "org.apache.spark" %% "spark-core" % sparkVersion,
    "org.apache.spark" %% "spark-sql" % sparkVersion,
    "org.apache.spark" %% "spark-streaming" % sparkVersion,
    "org.apache.spark" %% "spark-sql-kafka-0-10" % sparkVersion,
    "org.apache.spark" %% "spark-streaming-kafka-0-10" % sparkVersion,
    "org.apache.spark" %% "spark-streaming-kafka-0-10-assembly" % sparkVersion,
    "org.apache.kafka" % "kafka-clients" % kafkaVersion,
    "com.databricks" %% "spark-avro" % "4.0.0",
    "com.typesafe" % "config" % "1.3.2"
  )
}

mainClass in (Compile, run) :=  Some("Main")
mainClass in assembly := Some("Main")

assemblyMergeStrategy in assembly := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case _ => MergeStrategy.first
}
