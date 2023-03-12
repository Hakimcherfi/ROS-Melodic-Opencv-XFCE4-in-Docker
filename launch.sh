tag=ros
volume=volume_map
mkdir $volume
docker build . --tag $tag
docker run --rm -it -v $(pwd)/$volume:/root/Desktop/$volume -p 6080:6080 $tag
