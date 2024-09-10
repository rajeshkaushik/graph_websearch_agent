import copy
import os
import json
from states.state import AgentGraphState, get_agent_graph_state
from utils.helper_functions import check_for_content
from config.questions import QUESTIONS_MAPPING_CONFIG

def get_whoai_mehodology_next_question(state:AgentGraphState):
    questionaire_tool_response_old = get_agent_graph_state(state, 'questionaire_tool_response_latest')
    questionaire_tool_response_old = questionaire_tool_response_old() if callable(questionaire_tool_response_old) else questionaire_tool_response_old
    questionaire_tool_response_old = check_for_content(questionaire_tool_response_old)
    questionaire_tool_response_old = json.loads(questionaire_tool_response_old)
    previous_primary_question = questionaire_tool_response_old.get("currentPrimaryQuestion")
    valid_response = get_agent_graph_state(state, 'answer_evaluator_latest')
    valid_response = check_for_content(valid_response)
    valid_response = json.loads(valid_response)
    #import ipdb; ipdb.set_trace()
    if valid_response.get('valid').lower() == 'true':
        questionaire_tool_response = {"currentPrimaryQuestion": QUESTIONS_MAPPING_CONFIG.get(previous_primary_question).get('question'), "followupQuestion": valid_response.get('followup_question'), "followupCount": 0}
        response = {"questionaire_tool_response": json.dumps(questionaire_tool_response)}
    else:
        questionaire_tool_response = copy.deepcopy(questionaire_tool_response_old)
        questionaire_tool_response.update({"followupQuestion": valid_response.get('followup_question')})
        response = {"questionaire_tool_response": json.dumps(questionaire_tool_response)}
    #print(response)
    return response