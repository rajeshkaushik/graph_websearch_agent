import os
import json
from states.state import AgentGraphState, get_agent_graph_state
from utils.helper_functions import check_for_content
from config.questions import QUESTIONS_MAPPING_CONFIG

def get_whoai_mehodology_next_question(state:AgentGraphState):
    question_asked_latest = get_agent_graph_state(state, 'question_asked_latest')
    valid_response = get_agent_graph_state(state, 'answer_evaluator_latest')
    valid_response = check_for_content(valid_response)

    if '"valid": "True"'.lower() in valid_response.lower():
        response = {"questionaire_tool_response": QUESTIONS_MAPPING_CONFIG.get(question_asked_latest.content).get('question')}
    else:
        response = {"questionaire_tool_response": get_agent_graph_state(state, 'question_asked_latest')}
    #print(response)
    return response