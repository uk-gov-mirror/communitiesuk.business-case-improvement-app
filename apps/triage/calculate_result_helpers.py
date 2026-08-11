from enum import Enum
from .slugs import *
from .triage_data import TriageData

# because routing requires very specific checks, setting here to reduce likelihood of unknowing changes
class AnswerConstants(str, Enum):
    ABOVE_2M = "above-2m"
    BETWEEN_12K_AND_2M_STRING = "between-12k-and-2m"
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

    if total_value == AnswerConstants.BETWEEN_12K_AND_2M_STRING:
        if triage_data.is_commission_research:
            return 'you-need-to-speak-to-the-research-team'
        
        if full_12k_to_2m_flow_completed(triage_data):
            return get_procurement_exit(triage_data)
        else:
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
        

'''
Check all the answers that will lead from 12k-2m cost to the end, to determine
if we reached the end of the journey
'''
def full_12k_to_2m_flow_completed(triage_data: TriageData) -> bool:
    correct_options_chosen = triage_data.which_option_best_describes_what_is_trying_to_be_done in {
        procure_goods_and_services_from_third_party,
        hire_contracted_workers_to_fill_temporary_capacity_gap
    }
    
    return (not triage_data.is_novel and
            not triage_data.is_pilot and
            not triage_data.is_existing_programme and
            triage_data.where_is_the_budget_held != "" and
            correct_options_chosen and
            triage_data.is_corporate_spend_or_procurement and
            triage_data.business_case_title != "" and
            triage_data.summary != "")


def get_procurement_exit(triage_data: TriageData) -> str:
    best_describes_your_situation: str  = triage_data.which_option_best_describes_what_is_trying_to_be_done
    best_describes_your_spend: str = triage_data.which_option_best_describes_the_spend

    if triage_data.where_is_the_budget_held == AnswerConstants.DIGITAL_STRING:
        return "we-could-not-find-the-right-process-for-you"
    
    if best_describes_your_situation == procure_goods_and_services_from_third_party:
        if best_describes_your_spend == spend_on_corporate_activities:
            return "exit-to-download-template-corporate-spend-fbp-route"
        if best_describes_your_spend == procuring_something_else:
            return "exit-to-download-template-procurement-route" 

    if best_describes_your_situation == hire_contracted_workers_to_fill_temporary_capacity_gap:
        return "exit-to-download-template-hrbp-contingent-labour-route"
 
    return "we-could-not-find-the-right-process-for-you"

