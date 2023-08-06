# Telestream Cloud Flip Python SDK

This library provides a low-level interface to the REST API of Telestream Cloud, the online video encoding service.

## Requirements.

Python 2.7 and 3.4+

## Getting Started
### Initialize client

```python
import time
import telestream_cloud_flip
from telestream_cloud_flip.rest import ApiException
from pprint import pprint

api_instance = telestream_cloud_flip.FlipApi()
api_instance.api_client.configuration.api_key['X-Api-Key'] = '[API KEY]'

factory_id = '[FACTORY ID]'
```

### Upload video to flip service
```python
# Upload video
file_path = '/Users/rafalrozak/Downloads/panda.mp4'
profiles = 'h264'

extra_file_path = '/Users/rafalrozak/Downloads/sample.srt.txt'
extra_files = {
    'subtitles': [extra_file_path]
}

uploader = telestream_cloud_flip.Uploader(factory_id, api_instance, file_path, profiles, extra_files)
uploader.setup()
uploader.start()
pprint(uploader.status)
pprint(uploader.video_id)
```

### Create video from source URL
```python
# POST videos
createVideoBody = telestream_cloud_qc.CreateVideoBody(
    source_url="https://example.com/video.mp4", profiles="h264",
    subtitle_files=["https://example.com/subtitle.srt"]
)

try:
    video = api_instance.create_video(factoryId, createVideoBody)
    pprint(video)
except ApiException as e:
    print("Exception when calling FlipApi->create_video: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://api.cloud.telestream.net/flip/3.1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*FlipApi* | [**cancel_encoding**](docs/FlipApi.md#cancel_encoding) | **POST** /encodings/{encoding_id}/cancel.json | Cancels an Encoding.
*FlipApi* | [**cancel_video**](docs/FlipApi.md#cancel_video) | **POST** /videos/{video_id}/cancel.json | Cancel video and all encodings
*FlipApi* | [**copy_profile**](docs/FlipApi.md#copy_profile) | **POST** /profiles/{profile_id}/copy.json | Copies a given Profile
*FlipApi* | [**create_encoding**](docs/FlipApi.md#create_encoding) | **POST** /encodings.json | Creates an Encoding
*FlipApi* | [**create_factory**](docs/FlipApi.md#create_factory) | **POST** /factories.json | Creates a new factory
*FlipApi* | [**create_profile**](docs/FlipApi.md#create_profile) | **POST** /profiles.json | Creates a Profile
*FlipApi* | [**create_video**](docs/FlipApi.md#create_video) | **POST** /videos.json | Creates a Video from a provided source_url.
*FlipApi* | [**delete_encoding**](docs/FlipApi.md#delete_encoding) | **DELETE** /encodings/{encoding_id}.json | Deletes an Encoding from both Telestream Cloud and your storage. Returns an information whether the operation was successful.
*FlipApi* | [**delete_profile**](docs/FlipApi.md#delete_profile) | **DELETE** /profiles/{profile_id}.json | Deletes a given Profile
*FlipApi* | [**delete_video**](docs/FlipApi.md#delete_video) | **DELETE** /videos/{video_id}.json | Deletes a Video object.
*FlipApi* | [**delete_video_source**](docs/FlipApi.md#delete_video_source) | **DELETE** /videos/{video_id}/source.json | Delete a video&#39;s source file.
*FlipApi* | [**encodings_count**](docs/FlipApi.md#encodings_count) | **GET** /encodings/count.json | Returns a number of Encoding objects created using a given factory.
*FlipApi* | [**get_encoding**](docs/FlipApi.md#get_encoding) | **GET** /encodings/{encoding_id}.json | Returns an Encoding object.
*FlipApi* | [**get_factory**](docs/FlipApi.md#get_factory) | **GET** /factories/{id}.json | Returns a Factory object.
*FlipApi* | [**get_profile**](docs/FlipApi.md#get_profile) | **GET** /profiles/{profile_id}.json | Returns a Profile object.
*FlipApi* | [**get_video**](docs/FlipApi.md#get_video) | **GET** /videos/{video_id}.json | Returns a Video object.
*FlipApi* | [**list_encodings**](docs/FlipApi.md#list_encodings) | **GET** /encodings.json | Returns a list of Encoding objects
*FlipApi* | [**list_factories**](docs/FlipApi.md#list_factories) | **GET** /factories.json | Returns a collection of Factory objects.
*FlipApi* | [**list_profiles**](docs/FlipApi.md#list_profiles) | **GET** /profiles.json | Returns a collection of Profile objects.
*FlipApi* | [**list_video_encodings**](docs/FlipApi.md#list_video_encodings) | **GET** /videos/{video_id}/encodings.json | Returns a list of Encodings that belong to a Video.
*FlipApi* | [**list_videos**](docs/FlipApi.md#list_videos) | **GET** /videos.json | Returns a collection of Video objects.
*FlipApi* | [**list_workflows**](docs/FlipApi.md#list_workflows) | **GET** /workflows.json | Returns a collection of Workflows that belong to a Factory.
*FlipApi* | [**profile_encodings**](docs/FlipApi.md#profile_encodings) | **GET** /profiles/{id_or_name}/encodings.json | Returns a list of Encodings that belong to a Profile.
*FlipApi* | [**queued_videos**](docs/FlipApi.md#queued_videos) | **GET** /videos/queued.json | Returns a collection of Video objects queued for encoding.
*FlipApi* | [**resubmit_video**](docs/FlipApi.md#resubmit_video) | **POST** /videos/resubmit.json | Resubmits a video to encode.
*FlipApi* | [**retry_encoding**](docs/FlipApi.md#retry_encoding) | **POST** /encodings/{encoding_id}/retry.json | Retries a failed encoding.
*FlipApi* | [**signed_encoding_url**](docs/FlipApi.md#signed_encoding_url) | **GET** /encodings/{encoding_id}/signed-url.json | Returns a signed url pointing to an Encoding.
*FlipApi* | [**signed_encoding_urls**](docs/FlipApi.md#signed_encoding_urls) | **GET** /encodings/{encoding_id}/signed-urls.json | Returns a list of signed urls pointing to an Encoding&#39;s outputs.
*FlipApi* | [**signed_video_url**](docs/FlipApi.md#signed_video_url) | **GET** /videos/{video_id}/signed-url.json | Returns a signed url pointing to a Video.
*FlipApi* | [**update_encoding**](docs/FlipApi.md#update_encoding) | **PUT** /encodings/{encoding_id}.json | Updates an Encoding
*FlipApi* | [**update_factory**](docs/FlipApi.md#update_factory) | **PATCH** /factories/{id}.json | Updates a Factory&#39;s settings. Returns a Factory object.
*FlipApi* | [**update_profile**](docs/FlipApi.md#update_profile) | **PUT** /profiles/{profile_id}.json | Updates a given Profile
*FlipApi* | [**video_metadata**](docs/FlipApi.md#video_metadata) | **GET** /videos/{video_id}/metadata.json | Returns a Video&#39;s metadata


## Documentation For Models

 - [CanceledResponse](docs/CanceledResponse.md)
 - [CopyProfileBody](docs/CopyProfileBody.md)
 - [CountResponse](docs/CountResponse.md)
 - [CreateEncodingBody](docs/CreateEncodingBody.md)
 - [CreateVideoBody](docs/CreateVideoBody.md)
 - [DeletedResponse](docs/DeletedResponse.md)
 - [Encoding](docs/Encoding.md)
 - [EncodingSignedUrl](docs/EncodingSignedUrl.md)
 - [EncodingSignedUrls](docs/EncodingSignedUrls.md)
 - [Error](docs/Error.md)
 - [ExtraFile](docs/ExtraFile.md)
 - [Factory](docs/Factory.md)
 - [PaginatedEncodingsCollection](docs/PaginatedEncodingsCollection.md)
 - [PaginatedFactoryCollection](docs/PaginatedFactoryCollection.md)
 - [PaginatedProfilesCollection](docs/PaginatedProfilesCollection.md)
 - [PaginatedVideoCollection](docs/PaginatedVideoCollection.md)
 - [PaginatedWorkflowsCollection](docs/PaginatedWorkflowsCollection.md)
 - [Profile](docs/Profile.md)
 - [ResubmitVideoBody](docs/ResubmitVideoBody.md)
 - [RetriedResponse](docs/RetriedResponse.md)
 - [SignedVideoUrl](docs/SignedVideoUrl.md)
 - [UpdateEncodingBody](docs/UpdateEncodingBody.md)
 - [Video](docs/Video.md)


## Documentation For Authorization


## apiKey

- **Type**: API key
- **API key parameter name**: X-Api-Key
- **Location**: HTTP header


## Author

cloudsupport@telestream.net


