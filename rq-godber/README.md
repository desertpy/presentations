# Running Examples

* Install Docker
* Create Python 2.7 Virtual Environment
* pip install -r requirements.txt
* Start all the docker containers with: `docker-compose up`

You should now have three docker containers running:

* rqredis - Redis 2.8 server
* rqdashboard - The RQ Web Dashboard
* rqqorker - A single rq worker

The following ports will be exposed on your local machine (PUBLICLY
exposed):

* http://localhost:9181/ - The RQ Web Dashboard
* redis://localhost:6379/ - Redis server

You can now queue the simple test RQ job by running

  python ./rq1.py http://uberhip.com

Note to OS X users, your docker container won't be running on localhost,
docker is running in a linux virtual machine and needs to be accessed
using that virtual machines IP address.  The IP address can be obtained
by running the following command:

  boot2docker ip

So RQ commands will need to be called with the properl redis URL, for
example:

  rqinfo -u redis://192.168.59.103:6379/

# Notes on RQ

Running Redis Docker instance

[Docker Hub](https://registry.hub.docker.com/_/redis/)

When linking Docker containers, the other containers can be accessed
over a private internal network and the alias used when linking ends up
being set as the hostname in /etc/hosts
