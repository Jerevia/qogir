## QOGIR

*一个任务执行框架*

* 安装

```sh
pip install qogir
```

* 创建任务

```sh
qogir createjob <job-name> --type <job-type>[default|pyspark]
```

 当前目录下会生成如下文件：

```
./job-name
    ├── config.yaml
    ├── __init__.py
    ├── job.py
    └── requirements.txt
```

其中，`requirements.txt`是任务执行的python依赖，`config.yaml`定义了任务执行的一些基础参数，在job-type是default时，初始化为

```yaml
job-type:
 default

entry:
 job:main   # Entry function of job

python:
 <python-version> # python version, must be set before running

include_paths:  # Directory to insert to PYTHONPATH
 - /path/to/include_dir1
 - /path/to/include_dir2
```

其中，`include_paths`参数将会将指定路径插入PYTHONPATH。基于这个特性，你可以调用不属于Qogir任务本身的模块、类和方法。

在job-type是pyspark时，初始化为

```yaml
job-type:
 pyspark

entry:
 job:main   # Entry function of job

app-name:
 app        # Spark app name

log-level:
 INFO

python:
 <python-version> # python version, must be set before running

command-params: # Parameters of command `spark-commit`
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

include_paths:  # Directory to insert to PYTHONPATH
 - /path/to/include_dir1
 - /path/to/include_dir2
```

`job.py`定义了基础的任务入口

```python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals

def main(cls):
    cls.spark   # spark session
    cls.sc      # spark context
    cls.configs # configurations from config.yaml
    cls.params
```



* 准备就绪，执行任务:

通过bash命令行方式：

```sh
qogir runjob <job-name> -P/--params <params-json>
```

`-P/--params`选项支持任务执行时的参数传递，格式为Json，被解析为dict注入到`cls.params`。

Qogir支持通过Python脚本动态地执行任务，你可以将Qogir任务集成到你的Web服务、定时任务或单元测试中:

```python
# -*- coding: utf-8 -*-
from qogir.core.runner import JobRunner

job = JobRunner('/path/to/job')

job.run(params={'k1': 'v1'})
```

如果你使用Python3.6或以上版本，你可以使用Qogir提供的异步任务执行器`AsyncJobRunner`来高效的执行你的任务:

```python
from qogir.core.arunner import AsyncJobRunner
import asyncio


loop = asyncio.get_event_loop()

async def run_qogir_job():
    job = await AsyncJobRunner('/path/to/job')
    await job.run()

loop.run_until_complete(run_qogir_job())
```
