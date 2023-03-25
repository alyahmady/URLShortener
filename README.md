System Design reference: [Link](https://dev.to/karanpratapsingh/system-design-url-shortener-10i5)

Hints
- Designing a separate KGS service to be distributed via Zookeeper was out of this tasks scope, I guess. 
So I preferred to skip this part of design with a simple Random String generation (which will causes Unique Violation within 1/10,000,000 that is handled)
- Sharding in SQL is challenging and increases the system complexity (need to use consistent hashing). So I decided to choose MongoDB as the main database, as it increases complexity less than a RDBMS, in scaling.

Another (better) way to implement a scalable system (time-consuming for this test): [Link](https://www.enjoyalgorithms.com/blog/design-a-url-shortening-service-like-tiny-url)