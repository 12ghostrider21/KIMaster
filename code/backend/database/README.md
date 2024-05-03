
## Building image
```docker build -t clientdb-img .```


## running the container
```docker run -d -p 5432:5432 --name clientdb-con -v clientdb-data:/var/lib/postgresql/data --rm clientdb-img```


## stopping the container
```docker stop clientdb-con``` 

## connect to database via terminal
### Step 1
Connect to db via psql

```psql -h localhost -U dbuser -d clientdb```

now the terminal should ask you for your password

### Step 2
type password `dbpassword`

### further helpful instructions in psql

`\l` see all databases

`\c <db-name>` select a database

`\dt` display all tables in selected db

### How to run SQL 

Just type the SQL commands as usual into the psql terminal. Remember to write ; at the end of your query.  

`SELECT * FROM <table>;` 