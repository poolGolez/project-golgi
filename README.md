<!--
title: 'AWS Python Example'
description: 'This template demonstrates how to deploy a Python function running on AWS Lambda using the traditional Serverless Framework.'
layout: Doc
framework: v3
platform: AWS
language: python
priority: 2
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->


# Thumbnail Generator Example

Once the client uploads an image into an S3 bucket, a lambda function is invoked which resizes the image into a thumbnail, and creates a record on a DynamoDB table link the source S3 object and the generated S3 thumbnail object.

A REST API endpoint exists which allows the client to retrieve the records that were saved in the DynamoDB table.

![Architecture](docs/resources/AWS%20Diagrams.png)
