import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
  WebsiteSearchTool
)

llm = LLM(
  model="gemini/gemini-1.5-flash", 
  temperature=0,
  api_key=os.getenv("GEMINI_API_KEY"),
  provider="google"
)

@CrewBase
class SubCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    web_rag_tool = WebsiteSearchTool()

    @agent
    def sub(self) -> Agent:
        return Agent(
            config=self.agents_config["sub"], # type: ignore[index]
            verbose=True,
            llm=llm,
        )

    @agent
    def answering_questions_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["answering_questions_specialist"], # type: ignore[index]
            tools=[self.web_rag_tool],
            verbose=True,
            llm=llm,
        )
    
    @task
    def question_in_context(self) -> Task:
        return Task(
            config=self.tasks_config["question_in_context"], # type: ignore[index]
        )
    
    @task
    def question_definition(self) -> Task:
        return Task(
            config=self.tasks_config["question_definition"], # type: ignore[index]
        )
    
    @task
    def contextual_response(self) -> Task:
        return Task(
            config=self.tasks_config["contextual_response"], # type: ignore[index]
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.answering_questions_specialist()],
            tasks=[
                self.question_in_context(),
                self.question_definition(),
                self.contextual_response()
            ],
            process=Process.hierarchical,
            manager_agent=self.sub(),
            verbose=True,
            llm=llm
        )