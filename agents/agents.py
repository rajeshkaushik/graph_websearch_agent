# import json
# import yaml
# import os
import json
from termcolor import colored
from models.openai_models import get_open_ai, get_open_ai_json
from models.ollama_models import OllamaModel, OllamaJSONModel

from prompts.prompts import (
    interviewer_prompt_template,
    answer_evaluator_prompt_template,
    guard_rails_prompt_template
)
from utils.helper_functions import get_current_utc_datetime, check_for_content
from states.state import AgentGraphState, get_agent_graph_state

class Agent:
    def __init__(self, state: AgentGraphState, model=None, server=None, temperature=0, model_endpoint=None, stop=None, guided_json=None):
        self.state = state
        self.model = model
        self.server = server
        self.temperature = temperature
        self.model_endpoint = model_endpoint
        self.stop = stop
        self.guided_json = guided_json

    def get_llm(self, json_model=True):
        if self.server == 'openai':
            return get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(model=self.model, temperature=self.temperature)
        if self.server == 'ollama':
            return OllamaJSONModel(model=self.model, temperature=self.temperature) if json_model else OllamaModel(model=self.model, temperature=self.temperature)     

    def update_state(self, key, value):
        self.state = {**self.state, key: value}

class InterviewerAgent(Agent):
    def invoke(self, user_response, prompt=interviewer_prompt_template):
        interviewer_prompt = prompt.format(
            datetime=get_current_utc_datetime()
        )

        messages = [
            {"role": "system", "content": interviewer_prompt},
            {"role": "user", "content": f"User Response: {user_response}"}
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        self.update_state("interviewer_response", response)
        print(colored(f"Interviewer 👩🏿‍💻: {response}", 'cyan'))
        return self.state

class AnswerEvaluatorAgent(Agent):
    def invoke(self, prompt=answer_evaluator_prompt_template):

        questionaire_tool_response_latest = get_agent_graph_state(self.state, 'questionaire_tool_response_latest')
        questionaire_tool_response_latest = questionaire_tool_response_latest() if callable(questionaire_tool_response_latest) else questionaire_tool_response_latest
        questionaire_tool_response_latest = check_for_content(questionaire_tool_response_latest)
        questionaire_tool_response_latest = json.loads(questionaire_tool_response_latest)
        #import ipdb; ipdb.set_trace()
        current_primary_question = questionaire_tool_response_latest.get("currentPrimaryQuestion")
        user_response = get_agent_graph_state(self.state, 'user_response_latest')
        user_response = check_for_content(user_response)

        answer_evaluator_prompt = prompt.format(
            current_primary_question=current_primary_question
        )
        
        messages = [
            {"role": "system", "content": answer_evaluator_prompt},
            {"role": "user", "content": f"user_response: {user_response}"}
        ]
        #print(messages)

        llm = self.get_llm()
        
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        
        print(colored(f"answer_evaluator 🧑🏼‍💻: {response}", 'green'))
        self.update_state("answer_evaluator_response", response)
        return self.state

class GuardRailsAgent(Agent):
    def invoke(self, user_response, prompt=guard_rails_prompt_template):
        
        guard_rails_prompt = prompt.format(
            datetime=get_current_utc_datetime(),
        )

        messages = [
            {"role": "system", "content": guard_rails_prompt},
            {"role": "user", "content": f"user_response: {user_response}"}
        ]

        llm = self.get_llm(json_model=False)
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        print(colored(f"GuardRails 👨‍💻: {response}", 'yellow'))
        self.update_state("guard_rails_response", response)
        return self.state

class EndNodeAgent(Agent):
    def invoke(self):
        self.update_state("end_chain", "end_chain")
        return self.state