
# **Photo Album**
 
Implement a photo album web application that can be searched using natural language
through both text and voice. Use Lex, OpenSearch, and
Rekognition to create an intelligent search layer to query your photos for people,
objects, actions, landmarks and more.


# Table of contents
* [Description](#description)
* [Workflow](#workflow)


## Description

The photo album is a scalable web application designed and deployed using AWS services like S3, Lex and ElasticSearch. CI/CD DevOps pipeline is used to automate the build, test and deploy phases. The application allows users to make search requests, display the search results resulting from the query as well as upload new photos. The user is also given a choice to use either voice or text to perform the search queries.



## Workflow

* The frontend for the application is hosted in an S3 bucket as a static website.
* Using the AWS ElasticSearch service a domain is set up so that when a photo gets uploaded to the bucket, the lambda funciton LF1 is triggered to index it.
* Labels are detected in the image using Rekognition. A JSON object with a reference to each object in the S3 is stored in an ElasticSearch index, for every label detected by the Rekognition service.
* The lambda function LF2 is used as a code hook for the Lex service in order to detect the search keywords.
* Amazon Lex bot is created to handle search queries for which an intent called 'SearchIntent' is created and training utterances are added to the intent.

The following is the architecture for this project: 
<img width="729" alt="11" src="https://user-images.githubusercontent.com/68399465/228391248-526c1437-05d8-4d3b-b964-e0fe2e09a5f8.png">

