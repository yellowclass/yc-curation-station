from utils.http import postRequest
from dotenv import dotenv_values
from starlette.responses import JSONResponse

config = dotenv_values(".env")


async def getEmbeddingOfString(string: str):
    """
    Send a POST request to the OpenAI API to get the embedding of a string.

    Parameters:
        string (str): The string to get the embedding for.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If there is an error during the request.
    """
    try:
        post_response = postRequest(
            "https://api.openai.com/v1/embeddings", {"Authorization": f"Bearer {config['OPENAI_API_KEY']}", "Content-Type": "application/json"}, {"model": "text-embedding-ada-002", "input": string}
        )

        if post_response is not None:
            return post_response.get("data")[0].get("embedding")
        else:
            print("Failed to get a response for the embedding request.")
            return None

    except Exception as e:
        print(f"An error occurred in getEmbeddingOfString: {e}")
        return None
