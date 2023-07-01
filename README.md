# Good Will Solutions Corp. Serverless Project

It's a project for Serverless Cloud demo purpose. The code can either
be deployed at Amazon Web Services, Microsoft Azure and Google Cloud
Console.

This project includes an imaginary scenario for an imaginary company
**Good Will Solutions Corp.**.

It should analyze incomming forms as `.jpg` files by using an ocr, 
store the extracted information and send data to support channels in
Discord or Email.

This is a project by [JangasCodingplace](https://jangascodingplace.com)
Feel free to follow the full guide in the project section.


## Project Structure

This project follows a pure functional approach. Which means that 
methods should rather be expressions than statements and methods 
should always depends only on their inputs and outputs. Side effects
are the root of all evil - they won't be used as well.

- `gwsf`: _Good Will Solutions Framework_ includes common methods 
  which are shared through every cloud provider. It includes logical
  workflows, common classes and helper methods.
- `aws`: includes Code for AWS Lambda Functions. Resources which will
  be used as well: S3, Textract, DynamoDB, SQS, Cloud9 (recommended)
- `azure`: includes Code for Microsoft Azure Functions. Resources 
  which will be used as well: BlobStorage, FormRecognizer, CosmosDB,
  Service Bus
- `gcp`: includes Code for Google Cloud Functions. Resources which 
  will be used as well: Cloud Storage, DocumentAI, Firestore, Pub/Sub


Just for making it more obvious, we can bring solutions by each cloud
provider in relation:

| Usecase                   | AWS              | Azure           | GCP             |
| ------------------------- | ---------------- | --------------- | --------------- |
| Serverless Function       | Lambda Functions | Azure Functions | Cloud Functions |
| File Storage              | S3               | Blob Storage    | Cloud Storage   |
| OCR                       | Textract         | FormRecognizer  | DocumentAI      |
| Cloud Native (Document)DB | DynamoDB         | CosmosDB        | Firestore       |
| Message Broker            | SQS              | Service Bus     | Pub/Sub         |

## Setup & Requirements

This project is not made for local execution. You can execute the 
project only through it's implemented Unit Tests.


**Requirements**

- Python 3.10 or higher
- poetry

Access to a cloud provider is not required for local development. 
It's only required for deployment.


**Setup**

Install dependencies by using `poetry install`.
If you want to install AWS, Azure or GCP relevant packages, reference
to the corresponding group: `poetry install -G {{CLOUD_PROVIDER}}`

Install pre-commit by using `poetry run pre-commit install`

## Local Development Manual

If new packages should be added, use one of the following commands:
- `poetry add {{PACKAGE_NAME}}` - will add a package to the project
- `poetry add -D {{PACKAGE_NAME}}` - will add a package as dev 
   dependency
- `poetry add -G {{CLOUD_PROVIDER}} {{PACKAGE_NAME}}` - will add a 
   package as group dependency

Pre-commit can be very annoying. If you want to commit without 
getting verified by the added pre-commit hooks: 
`git commit -m {{YOUR_MESSAGE}} --no-verify`
