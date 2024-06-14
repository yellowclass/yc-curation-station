import requests
from starlette.responses import JSONResponse


def postRequest(url, headers, payload):
    """
    Send a POST request to the specified URL with the provided headers and payload.

    Parameters:
        url (str): The URL to send the POST request to.
        headers (dict): The headers to include in the POST request.
        payload (dict): The payload to send in the POST request.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If there is an error during the request.
    """
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Return the JSON response

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

    return None


def getRequest(url, headers, params=None):
    """
    Send a GET request to the specified URL with the provided headers and parameters.

    Parameters:
        url (str): The URL to send the GET request to.
        headers (dict): The headers to include in the GET request.
        params (dict, optional): The query parameters to include in the GET request.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If there is an error during the request.
    """
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Return the JSON response

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

    return None


# Example usage
if __name__ == "__main__":
    # Define the URL and the bearer token
    post_url = "https://api.openai.com/v1/embeddings"
    bearer_token = "your_bearer_token_here"

    # Define the headers
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Define the payload
    post_payload = {"model": "text-embedding-ada-002", "input": "your input text here"}

    # Send a POST request
    post_response = postRequest(post_url, headers, post_payload)
    if post_response is not None:
        print("POST Response JSON:", post_response)

    # Define the GET URL (example URL)
    get_url = "https://api.openai.com/v1/some_endpoint"

    # Define the GET parameters (if any)
    get_params = {"param1": "value1", "param2": "value2"}

    # Send a GET request
    get_response = getRequest(get_url, headers, get_params)
    if get_response is not None:
        print("GET Response JSON:", get_response)


async def ping(request):
    return JSONResponse({"status": 200, "message": "success", "data": "pong"})
