Run locally: 
´´´
python file-scanner/scanner.py
´´´
Make sur eyou have a .env file or define the needed environment variables. 

Build docker image: 
´´´
docker build -t file-scanner .
´´´

Run locally in a Docker container: 
´´´
docker run -it --privileged \
  -v /:/data \
  -e SCAN_ROOT=/data/mnt/f/tv_series/ \
  -e SCAN_OUTPUT=/data/root/dev/adk-projects/storage/files.json \
  -e SCAN_CHECKPOINT=/data/root/dev/adk-projects/storage/scanner_checkpoint.json \
  -e SCAN_BATCH_SIZE=1000 \
  -e SCAN_INTERVAL=600 \
  file-scanner
´´´