# AYCD AutoSolve Python Client

Client for connecting to the AYCD AutoSolve network

## Getting Started

For an example instantiation, take a look at testclient.py.

### Dependencies

pip modules auto-installed with autosolveclient:

```
pika
requests
logzero
```

### Initialization

Integrate in a few simple steps. First, install the module with:

```
pip install autosolveclient
```

Then, import the module into your application:
```
from autosolveclient import AutoSolve
```

Next, instantiate the autosolve module. It will throw a string containing 
AuthException or InputValueException if user credentials are incorrect:

```
try:
    auto_solve = AutoSolve(
        access_token="30144-4a843021-bb26-4a13-b442-f7ce4824da14",
        api_key="2164d024-51a9-4401-a8f6-23a08e46d314",
        client_key="test",
        receiver_function=receiver_function,
        debug=True)

    finished = auto_solve.initialized()
except Exception as s:
    print(s)
```

Where:
- access_token is the user's access token
- api_key is the user's api key generated for your program
- client_key is the unique client identifier given to you by AYCD
- receiver_function is your specified callback function for messages received
- debug enables more thorough console logging for actions occuring

The AutoSolve module instantiates and consumes messages asynchronously 
(connections in RabbitMQ for python are blocking). 
The connections are created in the constructor, so we need to wait for everything to be established,
detailed in the above try/except block:

```
finished = auto_solve.initialized()
```

This function is blocking, and will result in True if everything is correct,
 and False if something went wrong in connecting.

### Request Data

You must send requests in the following format:

```
{
    //An ID for the task requesting captcha. This can be whatever.
    "taskId" : "task1", 

    //Url of the site which the captcha was received
    "url" : "https://recaptcha.autosolve.io/version/1", 

    //Public ReCaptcha key for a given site
    "siteKey" : "6Ld_LMAUAAAAAOIqLSy5XY9-DUKLkAgiDpqtTJ9b", 

    //Api Key your customer needs from AYCD Autosolve
    "apiKey" : autoSolve.apiKey, 

    //Map object for parameters for ReCaptcha v2, in the grecaptcha.render method
    "renderParameters" : renderMap

    //Version of ReCaptcha
    //Options:
    /**
        V2_CHECKBOX is 0
        V2_INVISIBLE is 1
        V3_SCORE is 2
        */
    "version" : "0", 

    //Only required for ReCaptcha V3. Site-specific value. More info:
    //https://developers.google.com/recaptcha/docs/v3#actions
    "action" : "", 

    //Minimum score required to pass the recaptcha
    "minScore" : 0, 

    //Proxy used in the task which got the captcha
    "proxy" : "", 

    //Is proxy required, some captcha services don't support use of proxies
    //and will not be used if a proxy is necessary for captcha processing.
    //Default is false
    "proxyRequired" : false,

    //User agent used in the request (optional)
    "userAgent" : "",

    //Cookies in the request (optional)
    "cookies" : ""
}
```

### Handling Responses

You will receive responses in the following format, as a stringified JSON object:

```
{
    taskId
    siteKey
    token
    createdAt
    version
    action
}

```

The receiver function specified in your constructor will receive and handle all responses.

An example receiver function: 

```
def receiver_function(json_message):
    print("Task ID :: " + json_message['taskId'])
    print("Site Key :: " + json_message['siteKey'])
    print("Token :: " + json_message['token'])
    print("Created At :: " + json_message['createdAt'])
    print("Version :: " + json_message['version'])
    print("Action :: " + json_message['action'])
```


### Sending Requests

Lastly, to send a request, use the following function, where message is a json object:

```  
message = {"message" : "message to send"}
auto_solve.send_token(message)
```

This will return true if successful, or false if unsuccessful. It is blocking and should be handled
on another thread if possible. In the case that it is unsuccessful, use the following which will
wait, attempt resend, and if failed push the message to a backlog to resend upon reconnection:

### Error Handling

AutoSolve Python has automatic error handling and recovery, but will throw an exception if:

- Client Key is invalid
- API Key is invalid
- Access Token is invalid
- Connection error occurs AND recovery is not possible

Errors thrown will be strings. to switch/case on error, expect the following strings using
auto_solve.ERROR format to be contained by the error string:

- auto_solve.INVALID_CLIENT_ID
- auto_solve.INVALID_API_KEY_OR_ACCESS_TOKEN
- auto_solve.INPUT_VALUE_ERROR

## License

This project is licensed under the MIT License
