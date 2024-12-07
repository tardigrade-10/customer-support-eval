import pandas as pd
import json
import dotenv
import os
from openai import OpenAI, AsyncOpenAI
import asyncio
from prompt import DEFAULT_SYSTEM_PROMPT, UNBIASED_SYSTEM_PROMPT
import argparse

dotenv.load_dotenv()

client = AsyncOpenAI(
    #   organization='YOUR_ORG_ID',
    project=os.environ.get("PROJECT_ID"),
    api_key=os.environ.get("OPENAI_API_KEY"),
)

unequal_dict = json.load(open("cleaned_non_equal.json"))
ids_list = list(unequal_dict.keys())


async def calculateAccuracy(prev_context, response, agent_response):

    COMPLETE_CHAT = f"""PREV_CONTEXT: {prev_context}

AI_RESPONSE: {response} 

HUMAN_RESPONSE: {agent_response}"""

    response = await get_evaluation(COMPLETE_CHAT)

    result = response.to_dict()
    usage = result["usage"]
    print("Token Usage:", usage)

    scores = json.loads(result["choices"][0]["message"]["content"])

    total_score = 0
    for metric, value in scores.items():

        if metric == "summary":
            summary = value
        else:
            total_score += value
        # print(metric, value)

    final_score = total_score / (len(scores) - 1)

    # returns computed score
    return scores, final_score, summary


async def get_evaluation(chat):
    system_message = {
        "role": "system",
        "content": DEFAULT_SYSTEM_PROMPT.replace(">>chat<<", chat),
    }

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[system_message],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=300,
    )
    return response


async def main():
    parser = argparse.ArgumentParser(description="Process chat ID")
    parser.add_argument("--id", type=str, help="ID of the chat")
    parser.add_argument("--full", type=bool, default=False, help="Full evaluation")
    parser.add_argument(
        "--export", type=bool, default=False, help="Export results to json"
    )

    args = parser.parse_args()

    document = unequal_dict[args.id]
    scores, average_score, summary = await calculateAccuracy(
        document["prev_context"],
        document["response"],
        document["agent_response"]
    )

    if args.full:
        print(f"FULL_SCORES: {scores} SCORE: {average_score}, SUMMARY: {summary}")
    if not args.full:
        print(f"SCORE: {average_score}")
    if args.export:
        with open(f"{args.id}_eval.json", "w") as f:
            json.dump(scores, f)

    return average_score

if __name__ == "__main__":
    asyncio.run(main())


# CHATS = []
# for idx, key in enumerate(keys_list):
#     part = unequal_dict[key]
#     COMPLETE_CHAT = (
#         r"""PREV_CONTEXT: {}
#             AI_RESPONSE: {}
#             HUMAN_RESPONSE: {}"""
#             .format(
#             part["prev_context"], part["response"], part["agent_response"]
#         )
#     )
#     CHATS.append({"id": key, "COMPLETE_CHAT": COMPLETE_CHAT})

# print("got chats")

# async def get_unbiased_response(chat):
#     system_message = {
#         "role": "system",
#         "content": UNBIASED_SYSTEM_PROMPT.replace(">>chat<<", chat["COMPLETE_CHAT"]),
#     }

#     response = await client.chat.completions.create(
#         model="gpt-4o",
#         messages=[system_message],
#         response_format={"type": "json_object"},
#     )
#     return response, chat

# async def main():

#     for chat in CHATS[101:106]:
#         response_tasks.append(unbiased_response(chat))

#     results = await asyncio.gather(*response_tasks)
#     return results

# Run the main function
# results = asyncio.run(main())
# final = []
# scores = {}
# for result, chat in results:
#     result = result.to_dict()
#     scores[chat['id']] = json.loads(result["choices"][0]["message"]["content"])

# with open("scores_unequal_100_105_4o_1.json", "w") as f:
#     json.dump({'scores': scores}, f)
