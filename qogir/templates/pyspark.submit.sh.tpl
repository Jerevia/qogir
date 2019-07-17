WD={job_path}
MASTER='{MASTER}'

{{
    set -e
    while [ -f .env.tmp ]
    do
        sleep 1
    done

    [ ! -e "$WD/.venv.zip" ] && cd $WD && touch .env.tmp && cd {env_path} && echo 'Zipping python environment...' && zip -q -r $WD/.venv.zip ./ && cd $WD && rm -f .env.tmp
    echo "Using PYSPARK_PYTHON: $PYSPARK_PYTHON"
    HADOOP_CONF_DIR={HADOOP_CONF_DIR} \
        {submit_exec_path} \
        --master {MASTER} \
        {SUBMIT_PARAMS} \
        --conf spark.yarn.dist.archives $WD/.venv.zip#VENV \
        --conf spark.pyspark.driver.python={spark_python_path}\
        --conf spark.pyspark.python=./VENV/bin/python \
        {runner_path} {job_path} '{params}'
}} || {{
    set +e
    cd $WD && rm -f .env.tmp
}}
