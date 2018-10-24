# Notes on Airflow

## Installation

I'm trying to just get away with a simple basic installation for the purposes
of this presentation, here's what I did:

```bash
mkvirtualenv -p `which python3` airflow
export SLUGIFY_USES_TEXT_UNIDECODE=yes
pip3 install apache-airflow[mysql,redis,slack,crypto,password,ssh]
airflow initdb
# set host to 127.0.0.1 and use SSH tunneling for access
sed -i 's/^web_server_host.*$/web_server_host = 127.0.0.1/' airflow.cfg
airflow webserver -p 8080
# in another terminal
workon airflow
airflow scheduler
```


```
mkvirtualenv mpl -p `which python3`
pip install pandas matplotlib
which python # /srv/airflow/.virtualenvs/mpl/bin/python
```
