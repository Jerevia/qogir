WD={job_path}
MASTER="{MASTER}"
HADOOP_USER_NAME="{HADOOP_USER_NAME}"
SPARK_HOME=$({spark_python_path} -c "import pyspark; print(pyspark.__path__[0])")

{{
    set -e
    while [ -f .env.tmp ]
    do
        sleep 1
    done

    [ ! -e "$WD/.venv.zip" ] && cd $WD && touch .env.tmp && cd {env_path} && echo 'Zipping python environment...' && zip -q -r $WD/.venv.zip ./ && cd $WD && rm -f .env.tmp
    [[ "$MASTER" = *"local"* ]] && PYSPARK_PYTHON={spark_python_path} || PYSPARK_PYTHON=VENV/bin/python
    echo "Using PYSPARK_PYTHON: $PYSPARK_PYTHON"
    HADOOP_USER_NAME=$HADOOP_USER_NAME SPARK_HOME=$SPARK_HOME HADOOP_CONF_DIR={HADOOP_CONF_DIR} PYSPARK_PYTHON=$PYSPARK_PYTHON PYSPARK_DRIVER_PYTHON={spark_python_path} \
        {submit_exec_path} \
        --master {MASTER} \
        {SUBMIT_PARAMS} \
        --archives $WD/.venv.zip#VENV \
        {runner_path} {job_path} '{params}'
}} || {{
    set +e
    cd $WD && rm -f .env.tmp
    exit 1
}}
