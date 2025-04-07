# me - this DAT.
# webServerDAT - the connected Web Server DAT
# request - A dictionary of the request fields. The dictionary will always contain the below entries, plus any additional entries dependent on the contents of the request
# 		'method' - The HTTP method of the request (ie. 'GET', 'PUT').
# 		'uri' - The client's requested URI path. If there are parameters in the URI then they will be located under the 'pars' key in the request dictionary.
#		'pars' - The query parameters.
# 		'clientAddress' - The client's address.
# 		'serverAddress' - The server's address.
# 		'data' - The data of the HTTP request.
# response - A dictionary defining the response, to be filled in during the request method. Additional fields not specified below can be added (eg. response['content-type'] = 'application/json').
# 		'statusCode' - A valid HTTP status code integer (ie. 200, 401, 404). Default is 404.
# 		'statusReason' - The reason for the above status code being returned (ie. 'Not Found.').
# 		'data' - The data to send back to the client. If displaying a web-page, any HTML would be put here.

# Global variable for trigger state
var_trigger = False

# return the response dictionary
def onHTTPRequest(webServerDAT, request, response):
    global var_trigger
    
    # Set CORS headers
    response['Access-Control-Allow-Origin'] = '*'  # Allow all origins (change to specific domain if needed)
    response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'

    # Handle preflight request (CORS preflight request uses the OPTIONS method)
    if request['method'] == 'OPTIONS':
        response['statusCode'] = 200
        response['statusReason'] = 'OK'
        response['data'] = ''
        return response
    
    response['statusCode'] = 200 # OK
    response['statusReason'] = 'OK'
    
    # Route to set trigger to true
    if request['method'] == 'GET' and request['uri'] == '/trigger':
        var_trigger = True
        response['data'] = 'Trigger set to True'
        return response
        
    elif request['method'] == 'GET' and request['uri'] == '/UNtrigger':
        var_trigger = False
        response['data'] = 'Trigger set to False'
        return response
        
    # Route to get current trigger status
    elif request['method'] == 'GET' and request['uri'] == '/status':
        response['data'] = str(var_trigger)
        return response
    
    # Default route
    else:
        response['data'] = '<html><head></head><body><b>TouchDesigner: </b>' + webServerDAT.name + '<button onclick="simulateAnchorClick(1)">trigger stone BOOM</button><button onclick="simulateAnchorClick(0)">UNtrigger stone BOOM</button><script>function simulateAnchorClick(tf) {const a = document.createElement("a");a.href = tf ? "/trigger" : "/UNtrigger";a.click();}</script></body></html>'
        return response

def onWebSocketOpen(webServerDAT, client, uri):
    return

def onWebSocketClose(webServerDAT, client):
    return

def onWebSocketReceiveText(webServerDAT, client, data):
    webServerDAT.webSocketSendText(client, data)
    return

def onWebSocketReceiveBinary(webServerDAT, client, data):
    webServerDAT.webSocketSendBinary(client, data)
    return

def onWebSocketReceivePing(webServerDAT, client, data):
    webServerDAT.webSocketSendPong(client, data=data);
    return

def onWebSocketReceivePong(webServerDAT, client, data):
    return

def onServerStart(webServerDAT):
    global var_trigger
    var_trigger = False  # Initialize trigger to False on server start
    return

def onServerStop(webServerDAT):
    return