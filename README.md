# Nozama: Image-based Product Recommendation System

![](https://i.imgur.com/Ch8DTva.png)

Online shopping is becoming more and more popular nowadays due to its convenience. However, finding a product is still a time-consuming and less interesting part of the online shopping journey because users are still required to type keywords describing the products as well as getting mismatched results due to the difference between users' keywords and products' description from the sellers. 

One of the solutions to solve this problem is to provide to users a more intuitive way to find relevant products using image-based instead of keyword-based approach. This project will demonstrate a website application using machine learning model to recommends a list of similar products based on a given image.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Make sure you have python 3 and Anaconda installed on your environment.

The installing process is demonstrated in Linux and Macos environments.

This project is deployed using Google Cloud Platform (GCP). GCP provides free tier service to host a small web application without paying any fee so feel free to use it to test my project.

GCP also gives you $300 free credits to use within 1 year. That's a lot of money to use for machine learning and professional application deployment service.

[Google Cloud Platform](https://cloud.google.com/)


#### The dataset

If you want to train your own model using my datasets, you can download my datasets from here: [Link](https://Link)

The datasets contains 8 labels with 5,000 images each.

The datasets are provided by Standford University at [this link](https://http://jmcauley.ucsd.edu/data/amazon/index.html). Please cite the following if you use the data:

Ups and downs: Modeling the visual evolution of fashion trends with one-class collaborative filtering
R. He, J. McAuley
WWW, 2016
[pdf](http://cseweb.ucsd.edu/~jmcauley/pdfs/www16a.pdf)

Image-based recommendations on styles and substitutes
J. McAuley, C. Targett, J. Shi, A. van den Hengel
SIGIR, 2015
[pdf](http://cseweb.ucsd.edu/~jmcauley/pdfs/sigir15.pdf)

#### The metadata CSV

In order to retrieve information of the products, you need to add the product's metadata to your database service. I use Google Firestore as the database service. Please refer to the notebook `notebook/csv_to_firestore.ipynb` to import the metadata to Google Firestore.

Download the metadata CSV here: (https://Link)

[Google FireStore Documentation](https://https://firebase.google.com/docs/firestore/)

### Project structure

`app`: contains source codes of the web application.
=>`blueprints`: contains source codes of Flask modules
=>`middlewares`: contains source codes of the authentication service. As this feature is not mandatory, you can ignore this folder.
=>`models`: contains source codes of the models using to communicate with Firestore to store and get data.
=>`static`: contains all front-ends files and the trained models
=>`templates`: contains the HTML template files
=>`uploads`: used to store uploaded photo from the front-end

`functions`: contains source codes of the recommendation engine to be used as a standalone service.

`notebooks`: contains Jupyter notebooks for data preprocessing and machine learning tasks.

### Installing

#### Virtualenv

`pip install virtualenv`

`cd <git cloned folder>`

`virtualenv -p python3 env`

`source env/bin/activate`

#### Install required libraries for the web application

`cd app`

`pip install -r requirements.txt`


## Deployment

### Create a GCP project

1.  Sign into  [Google Cloud Console](https://console.cloud.google.com/)  with your Google Account.
2.  Click  **Select a project**  or the name of your existing project at the top of the page.
3.  Click  **New project**  and follow the prompts on screen.

-   Enable Billing. Google Cloud Platform provides $300 credit for new customers, and your usage may be eligible for Google Cloud Platform free-tier. For more information, see  [GCP Free Tier](https://cloud.google.com/free/).
-   [Install Google Cloud SDK](https://cloud.google.com/sdk/).

### Authentication to GCP API

Authentication refers to the process of determining a client's identity. Authorization refers to the process of determining what permissions an authenticated client has for a set of resources. That is, authentication refers to who you are, and authorization refers to what you can do.

1.  In the GCP Console, go to the  **Create service account key**  page.
    
    [GO TO THE CREATE SERVICE ACCOUNT KEY PAGE](https://console.cloud.google.com/apis/credentials/serviceaccountkey)
2.  From the  **Service account**  list, select **New service account**.
3.  In the  **Service account name**  field, enter a name.
4.  From the  **Role**  list, select  **Project**  >  **Owner**.
    
    **Note**: The  **Role**  field authorizes your service account to access resources. You can view and change this field later by using the  [GCP Console](https://console.cloud.google.com/). If you are developing a production app, specify more granular permissions than  **Project > Owner**. For more information, see  [granting roles to service accounts](https://cloud.google.com/iam/docs/granting-roles-to-service-accounts).
    
5.  Click  **Create**. A JSON file that contains your key downloads to your computer.

#### Setting the environment variable

If you plan to use a service account, you need to set an environment variable.

Provide authentication credentials to your application code by setting the environment variable  GOOGLE_APPLICATION_CREDENTIALS. Replace  `[PATH]`  with the file path of the JSON file that contains your service account key, and  `[FILE_NAME]`  with the filename. **This variable only applies to your current shell session, so if you open a new session, set the variable again.**

```
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```
For example:
```
export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/[FILE_NAME].json"
```

### Create a bucket on Cloud Storage

Google Cloud Storage is a unified storage for objects with global caching; you will use it to store product images. The API is enabled by default when you create the Google Cloud Platform; follow the steps below to upload an image to Cloud Storage, which we will use in later steps:

-   Open  [Cloud Storage Browser](https://console.cloud.google.com/storage/browser)  in Google Cloud Console.
-   Click  **Create Bucket**.
-   Type in the name of the bucket. Write down this name; it uniquely identifies the bucket in Google Cloud.
-   Click  **Create**.


### Cloud Firestore

Cloud Firestore is a NoSQL database. If you are not familiar with the concept, think of Cloud Firestore as a large-scale dictionary where data is stored in key-value pairs. The solution provides cheap, blazing fast storage for structured data, though it lacks the flexibility of traditional SQL databases. In Fansipan Store you will use it to store structured data, such as product details and order information.

To set up Firestore:

-   Open the  [Firestore page](https://console.cloud.google.com/firestore/)  in Google Cloud Console.
-   In the Welcome page, Select  **Cloud Firestore in Native Mode**.
-   Select a location, such as  `asia-east2(Hong Kong)`.
-   Click  **Create Database**.

Document is the  [unit of data storage](https://cloud.google.com/firestore/docs/data-model)  in Firestore, which can be grouped into collections. It is schemaless, which means that you do not have to specify the structure of data beforehand. The steps below create a document in the Products collection, which we will use later:

-   Open the  [Firestore Data page](https://console.cloud.google.com/firestore/data?)  in Google Cloud Console.
-   Click  **Start Collection**.
-   Type in  `products_amazon`  as the collection ID.
-   Leave the Document ID field empty. Cloud Firestore will automatically generate one for your document. The ID is the unique identifier of your document in the collection.
-   Click  **Save**.

### FireBase SDK

[Firebase](https://firebase.google.com/)  is a Google developed mobile/web app development platform that solves common app development challenges, such as authentication, analytics, storage, etc. You need to setup Firebase SDK in order to make the web application work with Firestore.

To set up the Firebase SDK:

-   Open  [Firebase Console](https://console.firebase.google.com/)  and sign in with your Google account.
-   Click  **Add project**. In the  **Project Name**  drop-down menu, select your Google Cloud Platform project. This adds Firebase to your Google Cloud Platform project.
-   Read the terms, and click  **Add Firebase**.
-   Click  **Add app**. Pick  **Web Platform**  (</>). The configuration for your Firebase project will show up in a pop-up window.

Create `app/static/js/initFirebase.js` with following codes. Replace YOUR-API-KEY, YOUR-AUTH-DOMAIN, YOUR-DATABASE-URL, YOUR-PROJECT-ID, YOUR-STORAGE-BUCKET, and YOUR-MESSAGING-SENDER-ID with values of your Firebase configuration. This is the Firebase configuration for the HTML javascripts.

```javascript
// Script for configuring Firebase.
// See https://firebase.google.com/docs/web/setup for more information.

var config = {
    apiKey: "YOUR-API-KEY",
    authDomain: "YOUR-AUTH-DOMAIN",
    databaseURL: "YOUR-DATABASE-URL",
    projectId: "YOUR-PROJECT-ID",
    storageBucket: "YOUR-STORAGE-BUCKET",
    messagingSenderId: "YOUR-MESSAGING-SENDER-ID"
};

firebase.initializeApp(config);
```

Create `app/firebase_config.json`** with following codes. Similarly, replace the placeholders with values of your Firebase configuration. This is the Firebase configuration for Firebase Admin SDK.

```javascript
{
    "apiKey": "YOUR-API-KEY",
    "authDomain": "YOUR-AUTH-DOMAIN",
    "databaseURL": "YOUR-DATABASE-URL",
    "projectId": "YOUR-PROJECT-ID",
    "storageBucket": "YOUR-STORAGE-BUCKET",
    "messagingSenderId": "YOUR-MESSAGING-SENDER-ID"
}
```

### Deployment to GCP AppEngine

#### app.yaml
Create `app/app.yaml` with following codes. Edit GCP_PROJECT, GCS_BUCKET, and FIREBASE_CONFIG.

```yaml
runtime: python37
instance_class: F4_1G

env_variables:
  GCP_PROJECT: "YOUR-PROJECT"
  GCS_BUCKET: "YOUR-GCS-BUCKET"
  FIREBASE_CONFIG: "firebase_config.json"

handlers:
  - url: /static
    static_dir: static
  
  - url: /.*
    script: auto
    secure: always
    redirect_http_response_code: 301
```

#### Deploy to GCP AppEngine
`cd app`
`gcloud app deploy`


### Deploy the Recommendation Engine
In order to make recommendation engine to work, you need to deploy the recommendation engine to GCP Cloud Functions.


#### upload trained model and Annoy index files to GCP Bucket
-   Download trained model and Annoy index files here: [Link](https://link)
-   Open  [Cloud Storage Browser](https://console.cloud.google.com/storage/browser)  in Google Cloud Console.
-   Access the Bucket you created above
-   Create 3 folders `models`, `ann_index`, and `ann_index/label_separated`
-   Upload the .h5 file to `models`
-   Upload the .ann and .json files to `ann_index/label_separated`

#### deploy cloud function

`cd <your git cloned project>`

`cd functions`

`cd recommend_v2`

`gcloud functions deploy recommend_v2 --runtime python37 --trigger-http --set-env-vars GSC_BUCKET=my_bucket-1 --region asia-east2 --memory 2048`

After that, open `app/blueprints/recommend/blueprint.py` and add your Cloud Functions address to this code.
```python
CLOUD_FUNC_RECOMMEND_URL = ''
```
[Cloud Function Documentation](https://cloud.google.com/functions/)


#### Notes for importing products data to Firestore
Please refer to the notebook `notebook/csv_to_firestore.ipynb` to import the metadata to Google Firestore.

## Authors

* **Binh Duong Thai** - [github](https://github.com/jodythai)

## Acknowledgments

This project made possible by the following amazing library:
* [Python Flask](https://github.com/pallets/flask/)  
* [Bootstrap](https://getbootstrap.com)
* [jQuery](https://jquery.com/)
* [CropperJs](https://fengyuanchen.github.io/cropperjs/)
* [TensorFlow](https://www.tensorflow.org/)
* [Annoy](https://github.com/spotify/annoy)

Reference for Machine Learning solution:



Ups and downs: Modeling the visual evolution of fashion trends with one-class collaborative filtering
R. He, J. McAuley
WWW, 2016
[pdf](http://cseweb.ucsd.edu/~jmcauley/pdfs/www16a.pdf)

Image-based recommendations on styles and substitutes
J. McAuley, C. Targett, J. Shi, A. van den Hengel
SIGIR, 2015
[pdf](http://cseweb.ucsd.edu/~jmcauley/pdfs/sigir15.pdf)

Image-based Product Recommendation System with Convolutional Neural Networks
Luyang Chen, Fan Yang, Heqing Yang
CS231n, 2017
[pdf](http://cs231n.stanford.edu/reports/2017/pdfs/105.pdf)
