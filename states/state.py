from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# Define the state object for the agent graph
class AgentGraphState(TypedDict):
    user_response: Annotated[list, add_messages]
    questionaire_tool_response: Annotated[list, add_messages]
    interviewer_response: Annotated[list, add_messages]
    answer_evaluator_response: Annotated[list, add_messages]
    guard_rails_response: Annotated[list, add_messages]
    end_chain: Annotated[list, add_messages]

# Define the nodes in the agent graph
def get_agent_graph_state(state:AgentGraphState, state_key:str):
    if state_key == "user_response_all":
        return state["user_response"]
    elif state_key == "user_response_latest":
        if state["user_response"]:
            return state["user_response"][-1]
        else:
            return state["user_response"]
    if state_key == "question_asked_all":
        return state["questionaire_tool_response"]
    elif state_key == "question_asked_latest":
        if state["questionaire_tool_response"]:
            return state["questionaire_tool_response"][-1]
        else:
            return state["questionaire_tool_response"]
    if state_key == "interviewer_all":
        return state["interviewer_response"]
    elif state_key == "interviewer_latest":
        if state["interviewer_response"]:
            return state["interviewer_response"][-1]
        else:
            return state["interviewer_response"]
    
    elif state_key == "answer_evaluator_all":
        return state["answer_evaluator_response"]
    elif state_key == "answer_evaluator_latest":
        if state["answer_evaluator_response"]:
            return state["answer_evaluator_response"][-1]
        else:
            return state["answer_evaluator_response"]
    
    elif state_key == "guard_rails_all":
        return state["guard_rails_response"]
    elif state_key == "guard_rails_latest":
        if state["guard_rails_response"]:
            return state["guard_rails_response"][-1]
        else:
            return state["guard_rails_response"]
    else:
        return None
    
state = {
    "interview_current_question":"",
    "interviewer_response": [],
    "answer_evaluator_response": [],
    "guard_rails_response": [],
    "end_chain": []
}