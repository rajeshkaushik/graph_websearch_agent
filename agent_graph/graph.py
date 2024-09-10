from langgraph.graph import StateGraph
from models.openai_models import get_open_ai_json
from agents.agents import (
    InterviewerAgent,
    AnswerEvaluatorAgent,
    GuardRailsAgent,
    EndNodeAgent
)
from prompts.prompts import (
    interviewer_prompt_template,
    answer_evaluator_prompt_template,
    guard_rails_prompt_template,
    interviewer_guided_json,
    answer_evaluator_guided_json
)

from tools.whoai_interviewer import get_whoai_mehodology_next_question
from states.state import AgentGraphState, get_agent_graph_state

def create_graph(server=None, model=None, stop=None, model_endpoint=None, temperature=0):
    graph = StateGraph(AgentGraphState)

    '''graph.add_node(
        "interviewer", 
        lambda state: InterviewerAgent(
            state=state,
            model=model,
            server=server,
            guided_json=interviewer_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            user_response=lambda: get_agent_graph_state(state=state, state_key="user_response"),
            prompt=interviewer_prompt_template
        )
    )'''

    graph.add_node(
        "answer_evaluator",
        lambda state: AnswerEvaluatorAgent(
            state=state,
            model=model,
            server=server,
            guided_json=answer_evaluator_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            prompt=answer_evaluator_prompt_template,
        )
    )

    '''graph.add_node(
        "guard_rails", 
        lambda state: GuardRailsAgent(
            state=state,
            model=model,
            server=server,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            user_response='TBD',
            prompt=guard_rails_prompt_template
        )
    )'''

    graph.add_node(
        "whoi_ai_questionaire_tool",
        lambda state: get_whoai_mehodology_next_question(
            state=state
        )
    )

    #graph.add_node("end", lambda state: EndNodeAgent(state).invoke())

    # Add edges to the graph
    graph.set_entry_point("answer_evaluator")
    #graph.add_edge("interviewer", "answer_evaluator")
    #graph.add_edge("answer_evaluator", "interviewer")
    graph.add_edge("answer_evaluator", "whoi_ai_questionaire_tool")
    #graph.add_edge("whoi_ai_questionaire_tool", "interviewer")
    #graph.add_edge("interviewer", "guard_rails")
    #graph.add_edge("whoi_ai_questionaire_tool", "end")
    graph.set_finish_point("whoi_ai_questionaire_tool")

    return graph

def compile_workflow(graph):
    workflow = graph.compile()
    return workflow