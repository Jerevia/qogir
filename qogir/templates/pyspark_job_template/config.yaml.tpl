job-type:
 pyspark

entry:
 job:main

app-name:
 app

log-level:
 INFO

python:
 <python-version>

command-params:
 HADOOP_CONF_DIR:
  /etc/hadoop
 MASTER:
  yarn
 SUBMIT_PARAMS:
  --driver-memory 6G
  --conf spark.default.parallelism=200
  --conf spark.driver.maxResultSize=2G
  --num-executors 20
  --executor-memory 4G
  --executor-cores 2

include_paths:
 /path/to/project
