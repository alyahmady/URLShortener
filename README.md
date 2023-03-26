TODO:

- Asynchronous task to remove expired URLs from MongoDB
- Don't create a duplicate record for Long URL, if it's already in MongoDB records (need index on `origianl_url` field)
- Return full Shortened URL in `CreateShortURL` response
- ...

---

System Design reference: [Link](https://dev.to/karanpratapsingh/system-design-url-shortener-10i5)

Hints
- Designing a separate KGS service to be distributed via Zookeeper was out of this tasks scope, I guess. 
So I preferred to skip this part of design with a simple Random String generation (which will causes Unique Violation within 1/10,000,000 that is handled)
- Sharding in SQL is challenging and increases the system complexity (need to use consistent hashing). So I decided to choose MongoDB as the main database, as it increases complexity less than a RDBMS, in scaling.

Another (better) way to implement a scalable system (time-consuming for this test): [Link](https://www.enjoyalgorithms.com/blog/design-a-url-shortening-service-like-tiny-url)

---

To initialize project on local:

1- Need to create a database and its owner user in MongoDB:
```shell
$ mongosh

> use DB_NAME
> db.createUser({user: "USER_NAME", pwd: "USER_PASS", roles: [{role: "readWrite", db: "DB_NAME"}]})

# Insert a sample (e.g. test) collection and a document to commit database changes
> db.test.insert({test: "test"})
```
* You should replace your desired values with `USER_NAME` and `USER_PASS` and `DB_NAME`.
And also fill variables in `deploy/envs/mongodb.env` according to these values.