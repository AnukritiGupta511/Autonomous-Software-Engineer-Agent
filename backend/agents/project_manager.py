from typing import Any, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from agents.base_agent import BaseAgent
import json

class ProjectManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Project Manager",
            description="You are the lead architect and project manager. Your job is to analyze user requests, break them down into tasks, and decide which specialized agents should execute them."
        )

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_request = input_data.get("user_request", "")
        available_context = input_data.get("available_context", {})

        system_prompt = self.get_system_prompt() + """
        Analyze the request and return a JSON object with:
        1. 'understanding': A brief summary of what the user wants.
        2. 'workflow_type': One of ['repo_analysis', 'bug_resolution', 'feature_development', 'question_answering']
        3. 'execution_plan': A list of steps for the agents to follow.
        4. 'required_agents': A list of agent names needed (e.g. ['Repository Analyzer', 'Code Reviewer', 'Bug Fixer', 'Feature Generator', 'Documentation Generator']).
        
        Return ONLY raw JSON, no markdown blocks.
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User Request: {user_request}\n\nContext: {json.dumps(available_context)}")
        ]

        response = await self.llm.ainvoke(messages)
        
        try:
            # Parse JSON out of the response
            plan_data = json.loads(response.content.strip('`').strip('json').strip())
            return {
                "status": "success",
                "plan": plan_data
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to parse LLM output: {str(e)}",
                "raw_output": response.content
            }
