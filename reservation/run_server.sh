DB_DIRECTORY=/home/hdd/mysql # Change this directory to suit your needs

if [ -z "$1" ]; then
        echo
        echo "Starts reservation-app."
        echo
        echo "Usage: $0 [path]"
	echo "Media files and logs are saved under [path]."
        echo
        docker ps -a | grep bps | grep Exited
        echo
        exit
fi


cd $1

#  Start mysql if not started already
docker run --name mysql -v $DB_DIRECTORY:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=1x1ac0m.c0m -d mysql:5.7

# If this the first time you are using this 
#docker run -ti --link mysql:mysql reservation-app:debug bash -c "/app/init_mysqldb.sh"


mkdir -p logs
mkdir -p media

# Run reservation-app
docker run -d -p 9000:9000 -v $(pwd)/logs:/app/logs -v $(pwd)/media:/app/media --link mysql:mysql --name reservation-app reservation-app

