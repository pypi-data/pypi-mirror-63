# agilicus_api.WhoamiApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**post_whoami**](WhoamiApi.md#post_whoami) | **POST** /v1/whoami | login through whoami


# **post_whoami**
> UserLoginInfo post_whoami(x_request_id, body)

login through whoami

### Example

```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.WhoamiApi(api_client)
    x_request_id = '73WakrfVbNJBaAmhQtEeDv' # str | a unique shortuuid
body = 'body_example' # str | 

    try:
        # login through whoami
        api_response = api_instance.post_whoami(x_request_id, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WhoamiApi->post_whoami: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_request_id** | **str**| a unique shortuuid | 
 **body** | **str**|  | 

### Return type

[**UserLoginInfo**](UserLoginInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | user logged in |  -  |
**403** | Unauthorized user |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

