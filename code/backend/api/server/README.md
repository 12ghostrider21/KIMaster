# How do start Server in docker 

## 1. Go to docker environment
navigate with `cd` into `code/backend/api/server`

``` cd code/backend/api/server/ ```

## 2. Build code changes (every time when code changed)
```docker build -t ki-api-img .```

## 3. run container
```docker run -p 8000:8000 --rm --name main-api -it server-api```