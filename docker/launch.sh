tag=ros
docker build . --tag $tag
docker run --rm -it -v $(pwd)/../volume_map:/root/Desktop/volume_map -p 6080:6080 $tag
