tag=ros
docker build . --tag $tag
docker run -it -p 6080:6080 $tag
