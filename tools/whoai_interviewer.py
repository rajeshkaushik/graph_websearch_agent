import os
import json
from states.state import AgentGraphState, get_agent_graph_state
from utils.helper_functions import check_for_content

questions_config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'questions.json')

fp = open(questions_config_file)
questions = json.loads(fp.read())
next_question_mapping = {}
for i in range(len(questions)-1):
    if i == 0:
        next_question_mapping['Thanks for joining us today. Are you ready for the interview?'] = questions[i]['question']
    next_question_mapping[questions[i]['question']] = questions[i+1]['question']

def get_whoai_mehodology_next_question(state:AgentGraphState):
    question_asked_latest = get_agent_graph_state(state, 'question_asked_latest')
    valid_response = get_agent_graph_state(state, 'answer_evaluator_latest')
    valid_response = check_for_content(valid_response)

    if '"valid": "True"'.lower() in valid_response.lower():
        response = {"questionaire_tool_response": next_question_mapping.get(question_asked_latest.content)}
    else:
        response = {"questionaire_tool_response": get_agent_graph_state(state, 'question_asked_latest')}
    #print(response)
    return response