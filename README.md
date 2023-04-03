# AlberBlanc

## Instructions: 
1. Check your Docker  ```brew install docker```
2. If everything is good, you can run

```
docker build  -t alber_test .
docker run -i -t alber_test  /bin/sh
```
In Ubuntu just run 

```
pytest -v -s --junitxml=out_report.xml tester
```

