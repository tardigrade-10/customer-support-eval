import json
import asyncio
from utils import get_embedding_async, cosine_similarity
import argparse

def get_tag(sim):
    match sim:
        case x if x < 0.5:
            return 'D'
        case x if x < 0.8:
            return 'C'
        case x if x < 0.95:
            return 'B'
        case _:
            return 'A'
        

async def main():

    parser = argparse.ArgumentParser(description="Process start and end indexes")

    parser.add_argument("--file", type=str, default='cleaned_non_equal.json', help="Start Index")
    parser.add_argument("--start", type=int, default=0, help="Start Index")
    parser.add_argument("--end", type=int, default=10, help="End index")

    args = parser.parse_args()

    unequal_dict = json.load(open(args.file))
    keys_list = list(unequal_dict.keys())

    start = args.start
    end = args.end
    ai_response_embeds = [get_embedding_async(value['response']) for value in list(unequal_dict.values())[start:end]]
    ai_response_embeds = await asyncio.gather(*ai_response_embeds)
    agent_response_embeds = [get_embedding_async(value['agent_response']) for value in list(unequal_dict.values())[start:end]]
    agent_response_embeds = await asyncio.gather(*agent_response_embeds)

    similarities = []
    for idx, i in zip(range(start, end), range(len(ai_response_embeds))):
        similarity = cosine_similarity(ai_response_embeds[i], agent_response_embeds[i])
        tag = get_tag(similarity)
        similarities.append({keys_list[idx]: {'similarity': similarity, 'tag': tag}})

    final = {'similarties': similarities}

    with open(f'similarties_{start}_{end}.json', 'w') as f:
        json.dump(final, f)

asyncio.run(main())