# js-chatroom
##Build the needed docker images 
        sudo docker-compose run django
##Break the execution
        ctrl + c 
##Apply migration to the database
        sudo docker-compose run django python3 manage.py migrate
##Run the docker container
        docker-compose up

# enjoy
