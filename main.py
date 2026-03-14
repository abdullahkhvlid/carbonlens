from action_agent import action_agent
from audit_agent import audit_agent
from action_validator_agent import action_validator_agent
from comparison_agent import comparison_agent
from research_agent import research_agent
from validator_agent import validator_agent


def main(query: str) -> dict:

    research_agent(query)
    
    audit_report = audit_agent(query)
    validator_report = validator_agent(query)
    
    comparison_report = comparison_agent(audit_report, validator_report)
    
    actions = action_agent(query)
    
    final_report = action_validator_agent(actions)

    return {
        "audit_report": audit_report,
        "validator_report": validator_report,
        "comparison_report": comparison_report,
        "actions": actions,
        "final_report": final_report
    }