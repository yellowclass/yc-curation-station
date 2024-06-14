import pprint
from dotenv import dotenv_values
from chatBot.utils import getEmbeddingOfString
from dbConfig import mongo_connection
from starlette.responses import JSONResponse
import json
from bson import json_util
import traceback
from utils.utils import convertToJson
from datetime import datetime
from openai import OpenAI

config = dotenv_values(".env")

db = mongo_connection.get_database()

"""
Single message schema

{
    userId: <string>,
    botId: <string>,
    timestamp: <datetime>,
    message: <string>,
    gptReply: <string>
    # sender: < "USER" | "BOT" >
    embedding: <vector>,

}

"""


async def send_message(request) -> str:
    try:
        # extract required arguments
        body = await request.json()
        message = body.get("message")
        user_id = body.get("userId")
        botId = body.get("botId")

        print(message, user_id)
        # validation
        if message is None or len(message.strip()) == 0:
            return JSONResponse({"status": 200, "message": "Send valid message"})
        # logic

        # create embedding of the message
        embedding = await getEmbeddingOfString(message)

        # fetch matching older messages
        oldMessages = await retrieve_nearest_documents(
            message=message,
            user_id=user_id,
            bot_id=botId,
            embedding=embedding,
        )

        old_messages = [{"user": message.get("message"), "gpt_reply": message.get("gptReply")} for message in oldMessages]
        bot_personal_info = await get_bot_personal_info(botId)

        system_prompt = create_combined_message_prompt(old_messages=old_messages, botPersonalDetails=bot_personal_info, message=message)

        print(system_prompt)

        gptResponse = getResponseFromGPT(system_prompt, message)

        # build the document to insert
        document = {"userId": user_id, "botId": botId, "timestamp": datetime.now(), "message": message, "gptReply": gptResponse, "sender": "USER", "embedding": embedding}
        db.messages.insert_one(document)

        return JSONResponse(
            {
                "status": 200,
                "message": "success",
                "data": convertToJson(
                    {
                        "gptResponse": gptResponse,
                        "oldReferredMessages": old_messages,
                    }
                ),
            }
        )

    except Exception as e:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        return JSONResponse(
            {
                "status": 500,
                "message": "Failure",
                "error": "Internal Server Error",
                "data": {},
            },
            status_code=500,
        )


def create_combined_message_prompt(*, old_messages=[], botPersonalDetails={}, message=""):
    nl = "\n"

    template = """You're a professional in the field of {designation}. Your name is {name} and you're known for {profession}. In your personal life, you're {personalLife}. Your interests include {Interests}. You're usually {Availability}.
                Write a message tailored to your expertise and personality. You could offer advice, share a personal anecdote related to your profession, or respond to a hypothetical scenario within your field."""

    filled_template = template.format(
        designation=botPersonalDetails["designation"],
        name=botPersonalDetails["name"],
        profession=botPersonalDetails["profession"],
        personalLife=botPersonalDetails["personalLife"],
        Interests=botPersonalDetails["Interests"],
        Availability=botPersonalDetails["Availability"],
    )

    filled_template = (
        filled_template
        + nl
        + f"""
    given are following older messages as list of conversation
    
    {nl.join([f"- User: {message.get('user')}, GPT Reply: {message.get('gpt_reply')}" for message in old_messages])}
    
    you have to reply in 20-40 words
    """
    )

    return filled_template


async def retrieve_nearest_documents(*, message, user_id, bot_id, embedding=None) -> str:
    try:
        # extract required arguments
        # body = await request.json()
        # message = body.get("message")
        # user_id = body.get("user_id")

        # validation
        if message is None or len(message.strip()) == 0:
            return JSONResponse({"status": 200, "message": "Send valid message"})
        if user_id is None:
            return JSONResponse({"status": 200, "message": "Send user Id"})

        # # create embedding of message
        embedding = embedding if embedding is not None else await getEmbeddingOfString(message)

        # query
        result = db.messages.aggregate(
            [
                {
                    "$vectorSearch": {
                        "queryVector": embedding,
                        "path": "embedding",
                        "index": "vector_index",
                        "limit": 5,
                        "numCandidates": 15,
                        "filter": {
                            "userId": user_id,
                            "botId": bot_id,
                            # "sender": "USER",
                        },
                    }
                },
                {
                    "$project": {
                        "timestamp": 1,
                        "message": 1,
                        "gptReply": 1,
                    }
                },
            ]
        )

        return list(result)
        return JSONResponse({"status": 200, "message": "success", "data": convertToJson(list(result))})

    except Exception as e:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        return JSONResponse(
            {
                "status": 500,
                "message": "Failure",
                "error": "Internal Server Error",
                "data": {},
            },
            status_code=500,
        )


def getResponseFromGPT(system_prompt, user_prompt, model="gpt-4-turbo-preview", top_p=0.7, temperature=0.7):
    response = OpenAI(api_key=config["OPENAI_API_KEY"]).chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        top_p=top_p,
        temperature=temperature,
    )
    return response.choices[0].message.content


async def get_full_chat(request):
    try:
        body = await request.json()
        userId = body.get("userId")
        botId = body.get("botId")

        result = db.messages.aggregate(
            [
                {
                    "$match": {
                        "userId": userId,
                        "botId": botId,
                    }
                },
                {"$project": {"message": 1, "gptReply": 1, "timestamp": 1}},
                # {
                #     "sort": {
                #         "timestamp": -1,
                #     }
                # },
            ]
        )

        return JSONResponse({"status": 200, "message": "success", "data": convertToJson(list(result))})
    except Exception as e:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        return JSONResponse(
            {
                "status": 500,
                "message": "Failure",
                "error": "Internal Server Error",
                "data": {},
            },
            status_code=500,
        )


async def get_bot_personal_info(botId):
    result = db.bots.aggregate(
        [
            {
                "$match": {
                    "botId": botId,
                }
            },
        ]
    )

    return list(result)[0]


async def get_bot_info(request):
    try:
        body = await request.json()
        botId = body.get("botId")

        result = await get_bot_personal_info(botId)

        return JSONResponse({"status": 200, "message": "success", "data": convertToJson(result)})
    except Exception as e:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        return JSONResponse(
            {
                "status": 500,
                "message": "Failure",
                "error": "Internal Server Error",
                "data": {},
            },
            status_code=500,
        )
