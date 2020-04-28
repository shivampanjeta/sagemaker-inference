Train and deploy model (draft)
==

This package contains a working version of model that can be packaged to a docker image and deployed as a sakemaker endpoint
## Steps
Prerequisite: "docker login" and "aws configure"

```
./build_and_push.sh [IMAGE_NAME]  # build image and push it to Amazon ECR
```

Test locally.
```
docker build  -t [IMAGE_NAME] .
docker run -p 80:80 -it [IMAGE_NAME]

```