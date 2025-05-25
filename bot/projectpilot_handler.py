from project_pilot_ai.task_extractor import TaskExtractor
from project_pilot_ai.repo_analyzer import RepoAnalyzer
from project_pilot_ai.github_agent import GitHubAgent
from project_pilot_ai.workflow_orchestrator import WorkflowOrchestrator

def handle_projectpilot_command(transcript, repo_path="."):
    extractor = TaskExtractor()
    analyzer = RepoAnalyzer(base_path=repo_path)
    github_agent = GitHubAgent()

    orchestrator = WorkflowOrchestrator(extractor, analyzer, github_agent)
    result = orchestrator.run(transcript)
    return result
