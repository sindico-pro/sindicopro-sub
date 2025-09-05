#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from sub_crew.crew import SubCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run(question: str = None):
    """
    Run the crew with a specific question or use default.
    
    Args:
        question: The question to ask the chatbot. If None, uses default question.
    """
    try:
        # Use provided question or default
        if question is None:
            question = "Eu preciso contratar um contador?"
        
        inputs = {
            "question": question,
            'current_year': str(datetime.now().year)
        }
        
        crew_instance = SubCrew()
        result = crew_instance.crew().kickoff(inputs=inputs)

        return result
    except Exception as e:
        raise RuntimeError(f"An error occurred while running the crew: {e}") from e


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        SubCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise RuntimeError(f"An error occurred while training the crew: {e}") from e

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SubCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise RuntimeError(f"An error occurred while replaying the crew: {e}") from e

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        SubCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise RuntimeError(f"An error occurred while testing the crew: {e}") from e

def chat():
    """
    Interactive chat mode - run the crew with a question from command line.
    Usage: python -m sub_crew.main chat "Sua pergunta aqui"
    """
    try:
        if len(sys.argv) < 3:
            print("Uso: python -m sub_crew.main chat 'Sua pergunta aqui'")
            print("Exemplo: python -m sub_crew.main chat 'Preciso contratar um contador?'")
            return
        
        question = sys.argv[2]
        print(f"🤖 Pergunta: {question}")
        print("=" * 50)
        
        result = run(question)
        
        print("📝 Resposta:")
        print(str(result))
        
    except Exception as e:
        raise RuntimeError(f"An error occurred while running chat: {e}") from e

if __name__ == "__main__":
    # Se executado diretamente, usar modo chat
    if len(sys.argv) > 1 and sys.argv[1] == "chat":
        chat()
    else:
        # Modo padrão - executar com pergunta padrão
        result = run()
        print("Resultado:", result)
