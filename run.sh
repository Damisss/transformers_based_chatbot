#!/bin/bash

while getopts ":habdptc" opt; do
  case ${opt} in
    h )
      printf -- "USAGE: ./run.sh [OPTION]... \n\n" 
      printf -- "-h for HELP, -a building api docker images, for -c for copying trained checkpoints, -b for building docker images of training, -d for running api docker containers, -p for running docker containers of training, or -t for TEARDOWN \n\n"  
      exit 1
      ;;
    a )
      # build docker images
      docker-compose -f docker-compose-api.yml build --no-cache
      exit 1
      ;;
    
    b )
      # build docker images
      docker-compose -f docker-compose-train.yml build --no-cache
      exit 1
      ;;

    d )
      # build docker images
      docker-compose -f docker-compose-api.yml up
      exit 1
      ;;

    
    p )
      # Spin up containers
      docker-compose -f docker-compose-train.yml up
      exit 1
      ;;

    c )
      DIRECTORY=./intent_recognition/registered_models_checkpoints
      if [ -d "$DIRECTORY" ]; then
        rm -r "$DIRECTORY"
      fi
      docker cp intent-recognition-image:/app/intent_recognition/registered_models_checkpoints ./intent_recognition
      exit 1
      ;;

    t )
      # Turn off intent-recognition-image container is running.
      running_app_container=`docker ps | grep intent-recognition-image | wc -l`
      if [ $running_app_container -gt "0" ]
      then
        docker kill intent-recognition-image
      fi
      # If intent-recognition-image container is off then remove it.
      existing_app_container=`docker ps -a | grep intent-recognition-image | grep Exit | wc -l`
      if [ $existing_app_container -gt "0" ]
      then
        docker rm intent-recognition-image
      fi
      # Turn off mlflow-image container is running.
      running_app_container=`docker ps | grep mlflow-image | wc -l`
      if [ $running_app_container -gt "0" ]
      then
        docker kill mlflow-image
      fi
      # If mlflow-image container is off then remove it.
      existing_app_container=`docker ps -a | grep mlflow-image | grep Exit | wc -l`
      if [ $existing_app_container -gt "0" ]
      then
        docker rm mlflow-image
      fi
       # Turn off api-image container is running.
      running_app_container=`docker ps | grep api-image | wc -l`
      if [ $running_app_container -gt "0" ]
      then
        docker kill api-image
      fi
      # If api-image container is off then remove it.
      existing_app_container=`docker ps -a | grep api-image | grep Exit | wc -l`
      if [ $existing_app_container -gt "0" ]
      then
        docker rm api-image
      fi
      exit 1
      ;;
    \? )
      printf "Invalid option: %s" "$OPTARG" 1>&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

printf -- "USAGE: ./run.sh [OPTION]... \n\n" 
printf -- "-h for HELP, -a building api docker images, for -c for copying trained checkpoints, -b for building docker images of training, -d for running api docker containers, -p for running docker containers of training, or -t for TEARDOWN \n\n"
exit 1
;;