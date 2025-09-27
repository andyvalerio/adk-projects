Build docker image: 
docker build -t file-scanner .

Run it locally: 
docker run -it --privileged -v /:/data file-scanner