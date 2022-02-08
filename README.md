## A service to normalize chemical compounds names with PubChem

### How to run:

##### First build the docker
docker image build -t biox_docker:1.0 .

##### run docker first time
docker container run --name biox biox_docker:1.0 python main.py

##### start it again
docker start -a biox

## NOTE
in Dickerfile the sorse code now can also be cloned from github, not copied from local


 

