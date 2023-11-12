**1 Introduction:**

In this project, I have undertaken the task of building a TikTok scrapper with a specific focus on fashion-related posts. The project can be broadly divided into 2 key steps:

1. scraping TikTok posts,
2. assigning relevance scores to the posts And filtering fashion-related content

**1.1 How to Run:**

To run the system, follow these steps:

1. Ensure you have Docker and Docker Compose installed on your system.
2. Clone the project repository.
3. Navigate to the project directory.
4. Run the following command to launch the containers:
**docker-compose up -d**

This command will start a container for the web server, providing APIs to execute tasks and storing data in a dedicated MongoDB cluster. It will also lauch standalone headless chrome browser that is used by webster functions to scrape data.

1. Configure your own MongoDB cluster and update the MongoDB URL in src/configs/mongodb\_config.py.

**1.2 Deployment:**

The project has been deployed on an AWS t2.micro server instance, hosting the web server and project code. Additionally, a MongoDB cluster has been deployed on the M0 Atlas cloud, utilizing the free tier for cost-effective storage and scalability. This setup allows for efficient data processing and storage while remaining within budget constraints.

**2 Technology Stack:**

**2.1 Used now:**

**Python** : Python was the natural choice for this project due to its versatility and proficiency in handling machine learning-related tasks, a part of this challenge. In real scenarios where multithreading is needed, choice can be languages like Java for ceratin tasks, or we can use pyspark that runs c++ code to lauch threads.

**Selenium** : I used Selenium, a popular web scraping framework for scrapping, as it is one of the most used frameworks in python to scrape and test code on browsers. Its widespread usage and robust support community made it the ideal choice for navigating TikTok's web interface, even in the face of anti-scraping measures.

**MongoDB** : For data storage, I opted for MongoDB, a NoSQL database that offers flexibility in handling unstructured data, a crucial requirement when dealing with TikTok posts. Furthermore, I leveraged the MongoDB Atlas free-tier cluster to ensure seamless data management throughout the project.

**2.2 Unlimited Time Vision:**

In an ideal scenario, unburdened by time constraints, several enhancements and optimizations could be woven into this project's fabric:

**Kafka** : I envision transitioning from MongoDB to Apache Kafka, a distributed streaming platform. Kafka's robust message-queueing system would facilitate efficient data transmission and processing.

**Selenium Grid** : The deployment of Selenium Grid would enable the concurrent execution of multiple browser instances across different nodes. This would dramatically increase throughput and scalability.

**Message Queues** : In lieu of MongoDB as the storage backend, I would migrate to a message-queuing system like Kafka. Data would be pushed to different topics within Kafka, ensuring seamless data distribution and processing. Additionally, Kafka Streams could be harnessed for real-time data transformation.

**Airflow** : Apache Airflow could be introduced to schedule and manage periodic tasks, such as consumer instances responsible for scraping comments. This orchestration tool would optimize resource utilization and enhance task scheduling.

These adaptations would not only improve scalability but also enrich the project's architecture, paving the way for a more robust and sustainable solution.

**3 Scraping TikTok Posts:**

**3.1. Collecting Posts Data:**

To start, I needed to collect data from TikTok. My choice of tool for this task was Selenium, a popular web scraping framework in Python.

One of the initial challenges was TikTok's anti-scraping measures, which could detect automation behavior. To work around this, I sought out available APIs. TikTok itself uses these APIs for fetching trending posts. I identified two relevant APIs:

1. for top trending recommended posts -
  1. [https://www.tiktok.com/api/recommend/item\_list/](https://www.tiktok.com/api/recommend/item_list/)
2. For trending fashion posts
  1. `[https://www.tiktok.com/browse/api/get-video-list](https://www.tiktok.com/browse/api/get-video-list)


Since these APIs are typically called by TikTok from a browser, I mimicked real behavior by calling these APIs from a Selenium browser.

**3.2. Collecting Comments:**

When it came to collecting comments for each TikTok post, the task presented several challenges due to TikTok's stringent measures to prevent direct API access to comments. Initially, I explored the possibility of using TikTok's API endpoint [https://www.tiktok.com/api/comment/list/](https://www.tiktok.com/api/comment/list/), which is designed to fetch comments. However, TikTok has implemented security measures to ensure that this API can only be accessed from genuine browsers.

I attempted to access the API in multiple ways:

1. **Without Using a Browser:** Initially, I tried to access the API directly without involving a browser. This approach was met with resistance from TikTok's security mechanisms, preventing me from retrieving comments.
2. **Using a Selenium Headless Browser:** In another attempt, I employed a Selenium headless browser to mimic human behavior and access the comments API. Unfortunately, TikTok's safeguards still posed a challenge, and I was unable to retrieve comments directly.

Given these limitations, I had to explore alternative methods to obtain comments for each post. Ultimately, I decided to resort to web scraping techniques to retrieve comments from the webpages of individual TikTok posts.

**3.2.2 Captcha Solver and Popup Handling:**

While web scraping offered a viable solution for collecting comments, TikTok introduced additional challenges in the form of captcha challenges. To overcome this, I used a captcha solver that I found on another github repo, a tool capable of deciphering and responding to TikTok's captcha challenges.

Additionally, TikTok often presents login pop-up boxes, which can disrupt the scraping workflow. To address this issue, I crafted a function that effectively closes these pop-up boxes, allowing for uninterrupted data collection.

I also assigned various configs to selenium driver like user-agent, devide\_id etc to mimic real browser.

**3.2.2.1 Potential Improvements:**

While the project meets the current requirements, there is scope for further enhancement if time permits:

Generating random configurations for different browser sessions could make the scraping process even more human-like. Improving the captcha solver's capabilities would be beneficial to handle a wider range of challenges.

**3.4. Scalability/Throughput/System Design:**

**3.4.1 Current Implementation:** To handle scalability, parallelism and throughput challenges, I employed several strategies

**1. Browser Choice:**

I use a standalone headless browser Docker instance for launching Selenium browser sessions. Although a scalable solution like Selenium Grid is ideal, given our time constraints, I opted for a standalone approach.

**2. Asynchronous Processing:**

Python's asynchronous capabilities were utilized to process multiple posts concurrently, enhancing efficiency.

**3. Post Processing:**

I process a maximum of 50 posts at a time from the MongoDB collection 'scraped\_posts' where comments have not been fetched yet. After processing, the data is stored in another table/collection named 'scraped\_posts\_with\_comments,' and the 'processed' field of the original posts is updated to 'true.'

**3.4.2 Unlimited Time Implementation:** While the project meets the current requirements, there is scope for further enhancement if time permits:

1. **Human-Like Browser Behavior:**
 Generating random configurations for different browser sessions could make the scraping process even more human-like. Improving the captcha solver's capabilities would be beneficial to handle a wider range of challenges.

1. **Selenium Grid Implementation:**
 For scaling purposes, I would consider switching to Selenium Grid. By launching multiple browser instances across multiple Selenium Grid nodes, I could process requests efficiently. For every 50 posts, we can assign request one of many browser instance on one of the grid nodes. For requests going to same browser instance, we can assign a new session to request, which would then process requests in different processes.

2. **Scaling Processor Nodes with Kafka Partitions:**
For scalability and efficient data processing, I will use the power of Apache Kafka while redesigning our system architecture. Kafka offers a robust solution for handling data streams and facilitating seamless scaling, without the need for intricate explanations about its underlying mechanics.


  1. **Partitioning for Parallelism:** Each Kafka topic, whether for scraped posts or posts with comments, will be divided into multiple partitions. These partitions act as processing units, enabling parallelism. We can dynamically adjust the number of partitions based on our processing needs. More partitions mean more parallelism, ensuring efficient data processing.
  2. **Processor Nodes:** Our processor nodes, responsible for analyzing and scoring TikTok data, will be horizontally scalable. We can add or remove these nodes as required to match the number of partitions. Each processor node will be assigned to handle specific partitions, optimizing resource utilization and processing speed.
  3. **Fault Tolerance:** Ensuring system reliability is paramount. To achieve this, I will set up a Kafka cluster with at least three broker nodes. This configuration enhances fault tolerance, as the system can continue functioning even if one broker node encounters issues.
  4. **Retention Policies:** To manage data storage efficiently, I will implement retention policies. Data in Kafka topics will be retained for a defined period, such as seven days. This approach prevents the storage from becoming unwieldy while allowing us to focus on processing the most recent TikTok posts. The retention period can be adjusted based on our processing requirements and the time frame within which we want to analyze data.
  5. **Real-Time Processing:** Leveraging Kafka Streams for real-time data processing and using Apache Airflow to schedule periodic tasks, such as comment scraping, could further optimize the system.

**3.5 API's**

1. **PUT API: scrape\_tiktok\_posts**?posts\_to\_scrape=1&cursor=1000


  1. **Description:** Used to scrape posts (without comments) from TikTok and store them in MongoDB. Returns the response.
  2. **Parameters:** posts\_to\_scrape (number of posts to scrape), cursor (cursor for pagination).


1. **GET API: get\_scraped\_fashion\_posts**
  1. **Description:** Returns posts without comments that have been fetched from TikTok.

1. **PUT API: fetch\_comments\_for\_scraped\_posts**?max\_posts\_to\_process=1
  1. **Description:** Gets posts from MongoDB table and scrapes comments for them one by one, storing them in a new MongoDB table. Returns the response.
  2. **Parameters** : max\_posts\_to\_process (number of posts to process).

2. **GET API: get\_scraped\_posts\_with\_comments**
  1. **Description:** Returns posts with comments that have been processed.

**4 Relevance scores and fashion posts filtering:**

**4.1 Assigning Relevance Scores and Filtering Fashion Posts:**

In our TikTok scraping and analysis project, I adopted a unique approach to assign relevance scores to the collected posts and subsequently filter posts based on their fashion-related content. Let's delve into the details of how I accomplished this:

**4.2 Relevance Score Calculation:**

Rather than first filtering posts and then assigning relevance scores, I decided to assign different relevance scores to all scraped posts and then filter out posts with lower fashion relevance scores. The relevance score calculation involves three main aspects:

**4.2.1. Post Statistical Relevance Score:**

This score is calculated based on the statistical attributes of each post, such as likes count, comment count, share count, and play count. I assign higher scores to posts with more interactions, as virality often indicates relevance. However, I also consider the age of the post by dampening the score for older posts. This is achieved by dividing the score by the number of days passed since the post was created.

**4.2.2. Fashion-Related Relevance Scores:**

I further break down relevance into two distinct scores

**4.2.2.1 Relevance Score Using Processed Dataset:**

I leveraged an Instagram posts dataset related to fashion brands ([https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/K7AW6F](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/K7AW6F)). I processed the dataset to identify:

i) Brands,

ii) The most frequently used hashtags (top 50), and

iii) The most important keywords in these posts.

**Approach:**

I created a corpus for each instagram post in the dataset by combining captions and comments, applying stop-word removal, lemmatization, and filtering out non-English words and short words (length \< 3). I then used LDA topic modeling, to identify top 10 topics and their associated top 10 words for each topic. These top words, along with the top 50 hashtags and brand names, form a common list.

To calculate the relevance score for our scraped TikTok post, I compare the frequency of words in our post's corpus against the common list.

**4.2.2.2 Post Relevance Score for Fashion Labels :**

To assess how closely a post is related to fashion, I employ a pre-trained text classification model, specifically Hugging Face's **facebook/bart-large-mnli**. This model classifies text against the keyword "fashion," assigning a score between 0 and 1. This score is our post\_relevance\_score\_fashion\_labels.

**4.3 Fashion Posts Filtering:**

Once we have calculated these relevance scores, filtering fashion-related posts becomes straightforward:

I consider any post that has a **post\_relevance\_score\_fashion\_labels**** \> 0.5**(indicating a classification confidence of more than 50%)**or ****relevance\_score\_using\_processed\_dataset \>** 1 (Indicating hat the post contains at least 2 keywords from the top 50 hashtags, top 100 words, or brand names extracted from the fashion-related data)

I mark such posts as 'is\_fashion\_post = true,' allowing us to easily filter and analyze fashion-related content from our scraped TikTok dataset.

This approach ensures that I only retain posts with a high likelihood of being fashion-related, optimizing our analysis efforts and delivering targeted insights into the fashion content within the TikTok platform.

**4.4 Scalability/Throughput/System Design:**

**4.4.1 Current Implementation:** In our current system, I have two main jobs

**1. Preprocessing Job for Instagram Data:** This job is responsible for preprocessing Instagram data and identifying the most important fashion keywords, as detailed earlier. It plays a critical role in enhancing the fashion-related content analysis.

**2. Relevance Score Assignment Job:** This job handles multiple tasks, including preprocessing post data for ML model inputs, applying text classification to calculate post\_relevance\_score\_fashion\_labels, and generating statistical scores for posts. It performs these tasks on-the-fly for a set of posts.

**4.4.2 Unlimited Time Implementation:** However, if I had unlimited time and resources, I would further refine our system for enhanced scalability and efficiency:

**1. Batch Processing Jobs:** To increase throughput and scalability, I would transition to batch processing. Spark, a powerful distributed processing framework, would be instrumental in handling large volumes of data efficiently.

1.1 **Kafka to HDFS Job:** I would introduce a dedicated job that consumes data from a Kafka topic containing posts with comments. This job would focus on preprocessing post data and generating essential features required as inputs for ML models. The processed data would be stored in a distributed storage system like HDFS.

1.2 **Text Classification with Spark** : In our refined architecture, I would introduce a separate job that leverages Spark to apply text classification on the preprocessed data. This job would calculate the **post\_relevance\_score\_fashion\_labels** for each post. By distributing the workload across multiple Spark nodes, I can significantly enhance processing speed and scalability.

1.3 **Statistical Score Calculation with Spark** : Another job would be responsible for calculating **static statistical scores** for posts. This task would involve the use of Spark and vectorization techniques to apply ML models at scale. Once again, this approach would optimize performance and scalability.

**2. Data Formats:** I would store our preprocessed data in a columnar or optimized file format like Parquet or ORC. These formats are designed to minimize storage space and improve query performance. By using columnar storage, I would efficiently read only the columns required for processing, reducing I/O overhead.

**3. Data Partitioning:** Data partitioning plays a crucial role in our system's scalability and performance. I would choose to partition our data based on post\_ids. Since our current design doesn't assume dependencies among posts, partitioning data by post\_ids aligns perfectly with our processing needs. Each partition represents a subset of posts, and this partitioning strategy enables Spark to process data in parallel without the need for joins or complex dependencies between partitions. This approach significantly improves the speed and throughput of our Spark jobs, as each partition can be processed independently.

**5. Scaling Processor Nodes:** Our processor nodes, responsible for analyzing and scoring TikTok data, would be designed for horizontal scalability. Each processor node would be assigned specific partitions to handle, optimizing resource utilization and processing speed. Since current design doesnt assume dependencies among posts, processing wont require joins, further improving speed and throughput of out spark jobs (Note: data is partitioned on POST\_IDS)

**6. Optimizing Accuracy (Unlimited Time):** We can improve efficiency of our ML tasks by taking pretrained models and training them on our own fashion data. Since training even single layers on top of LLM's require huge data, I choose to use pretrained models in current implementation.

1. We can train entity lining model on our own knowledge dataset so that it can detect entities specific to fashion
2. To better use text classifier, we can use multiple fashion labels instead of just using 1 "fasion" to improve scoring
3. train our text classification on our own knowledge base so that it can classify if text is fashion related or not with better accuracy

**4.5 API's**

1. **PUT Api:**  **process\_instagram\_post\_data**?num\_topics=10&words\_per\_topic=20


  1. **Description** : Preprocesses Instagram data with different parameters before processing on TikTok is started. Preprocessed data is available on GitHub.
  2. **Parameters** : num\_topics (number of topics), words\_per\_topic (words per topic).

2. **PUT API: filter\_fashion\_posts\_with\_relevance\_scores**?max\_posts\_to\_process=1


  1. Description: Assigns relevance scores to posts from a MongoDB table that stores posts with comments. Returns the response.
  2. Parameters: max\_posts\_to\_process (number of posts to process).

3. **GET API: get\_scraped\_fashion\_posts**


  1. Description: Retrieves fashion-filtered posts with relevance scores.

4. **PUT API: download\_scraped\_fashion\_posts\_csv**


  1. Description: Creates a CSV file for fashion posts and downloads it to the root GitHub folder.
