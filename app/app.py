from pathlib import Path
import sys
import time
import json

from termcolor import colored
sys.path.append(str(Path(__file__).absolute().parent.parent))
from agent_graph.graph import create_graph, compile_workflow
from states.state import AgentGraphState, get_agent_graph_state
from langchain_core.messages import HumanMessage

#from dotenv import load_dotenv
#load_dotenv()

# server = 'ollama'
# model = 'llama3:instruct'
# model_endpoint = None

server = 'openai'
model = 'gpt-4o'
model_endpoint = "https://poc-who-ai-openai-0001.openai.azure.com"

# server = 'vllm'
# model = 'meta-llama/Meta-Llama-3-70B-Instruct' # full HF path
# model_endpoint = 'https://kcpqoqtjz0ufjw-8000.proxy.runpod.net/' 
# #model_endpoint = runpod_endpoint + 'v1/chat/completions'
# stop = "<|end_of_text|>"

iterations = 100

print ("Creating graph and compiling workflow...")
graph = create_graph(server=server, model=model, model_endpoint=model_endpoint)
workflow = compile_workflow(graph)
print ("Graph and workflow created.")


if __name__ == "__main__":

    verbose = False
    state = AgentGraphState({"questionaire_tool_response":[HumanMessage(content='{"currentPrimaryQuestion": "Thanks for joining us today. Are you ready for the interview?", "followupQuestion": "", "followupCount": 0}')]})
    #print(state)

    while True:
        # import ipdb; ipdb.set_trace()
        questionaire_tool_response = json.loads(get_agent_graph_state(state, 'questionaire_tool_response_latest').content)
        print(colored(f"\n{questionaire_tool_response}\n", 'cyan'))
        next_question = questionaire_tool_response.get('followupQuestion') or questionaire_tool_response.get('currentPrimaryQuestion')
        print(colored(f"\n{next_question}", "yellow"))
        query = input("\nYou: ")
        start = time.time()
        if query.lower() == "exit":
            break
        if state.get("user_response"):
            state["user_response"].append(query)
        else:
            state.update({"user_response": [query]})
        dict_inputs = dict(state)
        #print(dict_inputs)
        #dict_inputs = {"user_response": query, "questionaire_tool_response":"Thanks for joining us today. Are you ready for the interview?"}
        # thread = {"configurable": {"thread_id": "4"}}
        limit = {"recursion_limit": iterations}
        '''
        for event in workflow.stream(
            dict_inputs, limit
            ):
            #import ipdb; ipdb.set_trace()
            if verbose:
                print("\nState Dictionary:", event)
            else:
                print(event)
        '''
        state = workflow.invoke(dict_inputs, limit)
        print(f' Time Taken: {time.time() - start}') 
        #import ipdb; ipdb.set_trace()
        #print(state)
