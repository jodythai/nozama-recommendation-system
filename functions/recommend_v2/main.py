import re
import os
import base64
import time
import sys
import numpy as np
import uuid
import json
import tensorflow as tf
import requests
from tensorflow.keras.models import Model
from flask import Blueprint, request, jsonify
from google.cloud import storage
from annoy import AnnoyIndex

BUCKET = os.environ.get('GSC_BUCKET')
USER_UPLOAD_FOLDER = 'uploads'
storage_client = storage.Client()

FILENAME_TEMPLATE = '{}.jpg'
IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

model = None
feature_extractor = None
ann_index = []
ann_metadata = []
MODEL = 'xception_ep12_tl_ep26_224x224_data_5000.h5'
MAX_TOP_K = 30 # the number of nearest neighbors returns from Annoy calculation

labels = ['Cell_Phones_and_Accessories', 'Clothing_Men', 'Clothing_Women', 'Electronics', 'Home_and_Kitchen', 'Pet_Supplies', 'Shoes', 'Watches']
# labels = ['Cell_Phones_and_Accessories', 'Clothing_Men', 'Clothing_Women']

if not os.path.exists('/tmp/models'):
    os.makedirs('/tmp/models')

if not os.path.exists('/tmp/ann_index'):
    os.makedirs('/tmp/ann_index')
    
def load_model():
    global model, feature_extractor
    
    if not os.path.exists('/tmp/models/' + MODEL):
        download_blob(BUCKET, 'models/' + MODEL, '/tmp/models/' + MODEL)

    path = '/tmp/models/' + MODEL
    model = tf.keras.models.load_model(path)

    # create feature extractor from the model by using the last fully connected layer
    layer_name = 'global_average_pooling2d'
    feature_extractor = Model(inputs=model.input, outputs=model.get_layer(layer_name).output)

def load_ann_index():

    global ann_index, ann_metadata

    for i in range(len(labels)):
        ann_index_name = 'index_xception_ep12_tl_ep26_224x224_data_5000_label_{}.ann'.format(i)
        ann_metadata_name = 'metadata_xception_ep12_tl_ep26_224x224_data_5000_label_{}.json'.format(i)

        if not os.path.exists('/tmp/ann_index/' + ann_index_name):
            download_blob(BUCKET, 'ann_index/label_separated/' + ann_index_name, '/tmp/ann_index/' + ann_index_name)
        
        if not os.path.exists('/tmp/ann_index/' + ann_metadata_name):
            download_blob(BUCKET, 'ann_index/label_separated/' + ann_metadata_name, '/tmp/ann_index/' + ann_metadata_name)

        path_ann_index = '/tmp/ann_index/' + ann_index_name
        path_ann_metadata = '/tmp/ann_index/' + ann_metadata_name

        with open(path_ann_metadata) as f:
            ann_metadata_data = json.load(f)
            ann_metadata.append(ann_metadata_data)

        ann_index_obj = AnnoyIndex(ann_metadata_data['features_length'], metric='angular')
        ann_index_obj.load(path_ann_index)
        ann_index.append(ann_index_obj)

def download_blob(bucket_name, src_blob_name, dst_file_name):
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(src_blob_name)

    blob.download_to_filename(dst_file_name)

    print('Blob {} downloaded to {}.'.format(
        src_blob_name,
        dst_file_name))

def upload_blob(bucket_name, src_file, dst_file_name):
    """Upload a file to the bucket"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob('uploads/'+dst_file_name)

    blob.upload_from_string(src_file, content_type='image/jpg')

    print('File uploaded to uploads/{}.'.format(dst_file_name))

def get_neighbors(label, input_feature_vectors, max_neighbors=14):
    results = []
    
    # get the nearest neighbors of that first nearest neighbor
    ann_index_obj = ann_index[label]
    

    for item_id in ann_index_obj.get_nns_by_vector(input_feature_vectors, max_neighbors):
        # if item_id != top_1:
        results.append({
        'id': item_id,
        'asin': ann_metadata[label]['list_asin'][item_id]
        })

    print('get_neighbors label', label)

    return results
    
def preprocess_image(img_raw):
    predict_img_width = IMAGE_WIDTH
    predict_img_height = IMAGE_HEIGHT

    img_str = re.search(b"base64,(.*)", img_raw).group(1)
    img_decode = base64.decodebytes(img_str)

    image = tf.image.decode_jpeg(img_decode, channels=3)
    image = tf.image.resize(image, [predict_img_width, predict_img_height])
    image = (255 - image) / 255.0  # normalize to [0,1] range
    image = tf.reshape(image, (1, predict_img_width, predict_img_height, 3))

    return image, img_decode

def recommend_v2(request):  
    global model, feature_extractor, ann_index, ann_metadata
    
    top_k = ''
    
    # Set up CORS to allow requests from arbitrary origins.
    # See https://cloud.google.com/functions/docs/writing/http#handling_cors_requests
    # for more information.
    # For maxiumum security, set Access-Control-Allow-Origin to the domain
    # of your own.
    if request.method == 'OPTIONS':
        headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'  
    }

    if feature_extractor is None or model is None:
        load_model()

    if len(ann_index) == 0 or len(ann_metadata) == 0:
        load_ann_index()

    if request.method == 'POST':
        
        request_time = time.time()
        
        data = request.get_json()
        img_raw = data['data-uri'].encode()

        image, img_decode = preprocess_image(img_raw)

        # upload file to storage
        id = uuid.uuid4().hex
        created_on = time.time()
        filename = FILENAME_TEMPLATE.format(str(created_on) + '_' + str(id))
        upload_blob(BUCKET, img_decode, USER_UPLOAD_FOLDER + '/' + filename)

        # predict the label
        t1 = time.time()
        prediction_probs = model.predict(image)
        predicted_label = np.argmax(prediction_probs, axis=1)[0]
        t2 = time.time()
        prediction_runtime = t2 - t1
        print('prediction_probs', prediction_probs)
        print('predicted_label', predicted_label)
        print('prediction_runtime', prediction_runtime)
        
        # get feature vector of uploaded photo
        t1 = time.time()
        input_feature_vectors = feature_extractor.predict(image)
        input_feature_vectors = input_feature_vectors.flatten()
        t2 = time.time()
        feature_extraction_runtime = t2 - t1
        print('feature_extraction_runtime', feature_extraction_runtime)
        
        t1 = time.time()
        # normalize to [0, 1] range for faster computing
        input_feature_vectors = input_feature_vectors / input_feature_vectors.max()
        # get top k from input
        top_k = get_neighbors(predicted_label, input_feature_vectors, MAX_TOP_K)
        t2 = time.time()
        get_neighbors_runtime = t2 - t1
        print('get_neighbors_runtime', get_neighbors_runtime)
        
    return (jsonify({'top_k': top_k, 
                     'predicted_label': str(predicted_label), 
                     'request_time': str(request_time), 
                     'prediction_probs': str(prediction_probs), 
                     'uploaded_filename': filename, 
                     'prediction_runtime': str(prediction_runtime),
                     'feature_extraction_runtime': str(feature_extraction_runtime),
                     'get_neighbors_runtime': str(get_neighbors_runtime)}), 200, headers)