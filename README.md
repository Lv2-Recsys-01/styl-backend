# styl-backend

```bash
conda create -n backend python=3.10.4
conda activate backend
pip install -r requirements.txt
pre-commit install
```

## docker

```bash
docker build --platform=linux/amd64 -t stylback .
docker run -it -p 8000:8000 stylback
```
