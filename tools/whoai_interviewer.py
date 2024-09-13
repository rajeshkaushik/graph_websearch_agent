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
    next_primary_question_config = QUESTIONS_MAPPING_CONFIG.get(previous_primary_question)
    #import ipdb; ipdb.set_trace()
    if valid_response.get('valid').lower() == 'true' \
            and questionaire_tool_response_old["followupCount"] >= questionaire_tool_response_old["min_follow_up"] \
                or questionaire_tool_response_old["followupCount"] >= questionaire_tool_response_old["max_follow_up"]:
        questionaire_tool_response = {
            "currentPrimaryQuestion": next_primary_question_config.get('question'),
            "min_follow_up": next_primary_question_config.get("min_follow_up"),
            "max_follow_up": next_primary_question_config.get("max_follow_up"),
            "followupQuestion": "",
            "followupCount": 0}
        response = {"questionaire_tool_response": json.dumps(questionaire_tool_response)}
    else:
        questionaire_tool_response = copy.deepcopy(questionaire_tool_response_old)
        questionaire_tool_response["followupQuestion"] = valid_response.get('followup_question')
        questionaire_tool_response["followupCount"] = questionaire_tool_response.get("followupCount", 0) + 1
        response = {"questionaire_tool_response": json.dumps(questionaire_tool_response)}
    #print(response)
    return response