from enum import Enum
from .slugs import *
from apps.triage.triage_data import TriageData

# because routing requires very specific checks, setting here to reduce likelihood of unknowing changes
class AnswerConstants(str, Enum):
    ABOVE_2M = "above-2m"
    BETWEEN_12K_AND_2M = "between-12k-and-2m"
    BELOW_12K = "below-12k"
    DIGITAL_STRING = "Digital"


"""
Works out which result to show based on the combination of answers.

Returns a result slug.
Called when calculate-result is the next step, not in general flow
"""
def get_result_from_answers(answers: dict) -> str:
    triage_data = TriageData(answers)

    total_value = triage_data.total_value_of_business_case
    
    if total_value == AnswerConstants.ABOVE_2M:
        return "you-need-to-follow-a-three-stage-process"

    if total_value == AnswerConstants.BETWEEN_12K_AND_2M:
        if triage_data.is_commission_research:
            return 'you-need-to-speak-to-the-research-team'
        
        if triage_data.is_procurement_route_completed:
            return get_procurement_exit(triage_data)
        
        if triage_data.is_general_route_completed:
            return get_general_exit(triage_data)
        
        if triage_data.is_grants_route_completed:
            return "exit-to-download-template-grant-route"
        
        if triage_data.is_three_stage_process_novel_or_pilot:
            return "you-need-to-follow-a-three-stage-process-novel-or-pilot"
        
        return "we-could-not-find-the-right-process-for-you"

    if total_value == AnswerConstants.BELOW_12K:
        return determine_is_less_than_12k_exit_route(triage_data)

    return "we-could-not-find-the-right-process-for-you"


def determine_is_less_than_12k_exit_route(triage_data: TriageData) -> str:
    if triage_data.is_part_of_wider_programme_with_existing_fbc:
        return "speak-to-someone-first"

    return (
        "do-not-need-a-business-case-no-programme-digital" if triage_data.does_involve_digital 
        else "do-not-need-a-business-case-no-programme-not-digital")


def get_procurement_exit(triage_data: TriageData) -> str:
    
    if triage_data.where_is_the_budget_held == AnswerConstants.DIGITAL_STRING.value:
        return "digital-exit-for-procurement-route"

    return "exit-to-download-template-procurement-route"


def get_general_exit(triage_data: TriageData):

    if triage_data.which_option_best_describes_the_spend == spend_on_corporate_activities:
        return "exit-to-download-template-corporate-spend-fbp-route"

    if triage_data.which_option_best_describes_what_is_trying_to_be_done == hire_contracted_workers_to_fill_temporary_capacity_gap:
        return "exit-to-download-template-hrbp-contingent-labour-route"

    if triage_data.which_option_best_describes_what_is_trying_to_be_done == procuring_something_else:
        return "general-exit-for-something-else"
    
    return "we-could-not-find-the-right-process-for-you"
