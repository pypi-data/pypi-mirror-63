# agilicus_api.TokensApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**introspect_token**](TokensApi.md#introspect_token) | **POST** /v1/tokens/introspect | Introspect a token
[**post_creator**](TokensApi.md#post_creator) | **POST** /v1/tokens | Create a token
[**query_tokens**](TokensApi.md#query_tokens) | **GET** /v1/tokens | Query tokens
[**revoke_token**](TokensApi.md#revoke_token) | **POST** /v1/tokens/revoke | Revoke a token


# **introspect_token**
> Token introspect_token(raw_token)

Introspect a token

Introspect a token

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.TokensApi(api_client)
    raw_token = agilicus_api.RawToken() # RawToken | Token to introspect

    try:
        # Introspect a token
        api_response = api_instance.introspect_token(raw_token)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->introspect_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **raw_token** | [**RawToken**](RawToken.md)| Token to introspect | 

### Return type

[**Token**](Token.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Traffic token |  -  |
**410** | Token has been revoked |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_creator**
> RawToken post_creator(token_request)

Create a token

Create a token

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.TokensApi(api_client)
    token_request = agilicus_api.TokenRequest() # TokenRequest | Rule to sign

    try:
        # Create a token
        api_response = api_instance.post_creator(token_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->post_creator: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_request** | [**TokenRequest**](TokenRequest.md)| Rule to sign | 

### Return type

[**RawToken**](RawToken.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully signed assertion |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **query_tokens**
> Token query_tokens(limit=limit, sub=sub, exp_from=exp_from, exp_to=exp_to, iat_from=iat_from, iat_to=iat_to, jti=jti, org=org, revoked=revoked)

Query tokens

Query tokens

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.TokensApi(api_client)
    limit = 56 # int | limit the number of rows in the response (optional)
sub = 'sub_example' # str | search criteria sub (optional)
exp_from = 'exp_from_example' # str | search criteria expired from using dateparser (optional)
exp_to = 'exp_to_example' # str | search criteria expired to using dateparser (optional)
iat_from = 'iat_from_example' # str | search criteria issued from using dateparser (optional)
iat_to = 'iat_to_example' # str | search criteria issued to using dateparser (optional)
jti = 'jti_example' # str | search criteria using jti (optional)
org = 'org_example' # str | search criteria using org (optional)
revoked = True # bool | search criteria for revoked tokens (optional)

    try:
        # Query tokens
        api_response = api_instance.query_tokens(limit=limit, sub=sub, exp_from=exp_from, exp_to=exp_to, iat_from=iat_from, iat_to=iat_to, jti=jti, org=org, revoked=revoked)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->query_tokens: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] 
 **sub** | **str**| search criteria sub | [optional] 
 **exp_from** | **str**| search criteria expired from using dateparser | [optional] 
 **exp_to** | **str**| search criteria expired to using dateparser | [optional] 
 **iat_from** | **str**| search criteria issued from using dateparser | [optional] 
 **iat_to** | **str**| search criteria issued to using dateparser | [optional] 
 **jti** | **str**| search criteria using jti | [optional] 
 **org** | **str**| search criteria using org | [optional] 
 **revoked** | **bool**| search criteria for revoked tokens | [optional] 

### Return type

[**Token**](Token.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return traffic tokens list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **revoke_token**
> object revoke_token(token_revoke)

Revoke a token

Revoke a token

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.TokensApi(api_client)
    token_revoke = agilicus_api.TokenRevoke() # TokenRevoke | Token to revoke

    try:
        # Revoke a token
        api_response = api_instance.revoke_token(token_revoke)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->revoke_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_revoke** | [**TokenRevoke**](TokenRevoke.md)| Token to revoke | 

### Return type

**object**

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | token has been revoked |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

