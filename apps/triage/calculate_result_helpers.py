from enum import Enum
from .slugs import *

# because routing requires very specific checks, setting here to reduce likelihood of unknowing changes
class AnswerConstants(str, Enum):
    ABOVE_2M = "above-2m"
    BETWEEN_12K_AND_2M_STRING = "between-12k-and-2m"
    DIGITAL_STRING = "Digital"


"""
Works out which result to show based on the combination of answers.

Returns a result slug.
Called when calculate-result is the next step, not in general flow
"""
def get_result_from_answers(answers: dict) -> str:
    total_value = answers.get(total_value_of_business_case)

    if total_value == AnswerConstants.ABOVE_2M:
        return "you-need-to-follow-a-three-stage-process"

    if total_value == AnswerConstants.BETWEEN_12K_AND_2M_STRING:
            if is_commission_research(answers):
                return 'you-need-to-speak-to-the-research-team'
            
            if full_12k_to_2m_flow_completed(answers):
                return get_procurement_exit(answers)
            else:
                if is_three_stage_process_novel_or_pilot(answers):
                    return "you-need-to-follow-a-three-stage-process-novel-or-pilot"
                return "we-could-not-find-the-right-process-for-you"

    if total_value == "below-12k":
        return determine_is_less_than_12k_exit_route(answers)

    return "we-could-not-find-the-right-process-for-you"


def determine_is_less_than_12k_exit_route(answers: dict) -> str:
    if answers.get(part_of_wider_programme_with_existing_fbc, None) == "yes":
        return "speak-to-someone-first"

    if answers.get(part_of_wider_programme_with_existing_fbc, None) == "no":
        involves_digital: bool = answers.get(does_request_involve_anything_digital, None) == "yes"

        if involves_digital != None:
            return ("do-not-need-a-business-case-no-programme-digital" if involves_digital 
                        else "do-not-need-a-business-case-no-programme-not-digital")
        
    return "we-could-not-find-the-right-process-for-you"

def is_three_stage_process_novel_or_pilot(answers: dict) -> bool:
    # could be 'I don't know' so check it's not No here, as Yes and Don't Know are the same route
    is_novel = answers.get(novel_repercussive_contentious_hmt_consent, None) != "no"
    is_pilot = answers.get(is_this_request_a_pilot, None) == "yes"

    return (is_novel or is_pilot)

def is_commission_research(answers: dict) -> bool:
    is_not_novel = answers.get(novel_repercussive_contentious_hmt_consent, None) == "no"
    is_not_pilot = answers.get(is_this_request_a_pilot, None) == "no"
    is_not_existing_programme = answers.get(is_this_request_part_of_a_wider_programme_with_existing_business_case, None) == "no"
    is_not_digital_budget = answers.get(where_is_the_budget_held, None) != ""

    is_trying_to_commission_research = answers.get(which_option_describes_what_you_are_trying_to_do, None) == commission_research

    return (is_not_novel and
            is_not_pilot and
            is_not_existing_programme and
            is_not_digital_budget and
            is_trying_to_commission_research)


'''
Check all the answers that will lead from 12k-2m cost to the end, to determine
if we reached the end of the journey
'''
def full_12k_to_2m_flow_completed(answers: dict) -> bool:
    is_not_novel = answers.get(novel_repercussive_contentious_hmt_consent, None) == "no"
    is_not_pilot = answers.get(is_this_request_a_pilot, None) == "no"
    is_not_existing_programme = answers.get(is_this_request_part_of_a_wider_programme_with_existing_business_case, None) == "no"
    budget_answered = answers.get(where_is_the_budget_held, None) != ""
    is_corporate_spend_or_procurement: bool = answers.get(which_best_describes_your_spend, None) != ""
    is_business_case_title_answered: bool = answers.get(give_your_bjc_a_name, None) != ""
    is_summary_answered: bool = answers.get(provide_a_high_level_summary, None) != ""

    is_trying_to_procure_from_third_party = answers.get(which_option_describes_what_you_are_trying_to_do, None) in {
        procure_goods_and_services_from_third_party,
        hire_contracted_workers_to_fill_temporary_capacity_gap
        }

    return (is_not_novel and
            is_not_pilot and
            is_not_existing_programme and
            budget_answered and
            is_trying_to_procure_from_third_party and
            is_corporate_spend_or_procurement and
            is_business_case_title_answered and
            is_summary_answered)


def get_procurement_exit(answers: dict) -> str:
    best_describes_your_situation: str | None = answers.get(which_option_describes_what_you_are_trying_to_do, None)
    best_describes_your_spend: str | None = answers.get(which_best_describes_your_spend, None)

    if answers.get(where_is_the_budget_held, None) == AnswerConstants.DIGITAL_STRING:
        return "we-could-not-find-the-right-process-for-you"
    
    if best_describes_your_situation == procure_goods_and_services_from_third_party:
        if best_describes_your_spend == spend_on_corporate_activities:
            return "exit-to-download-template-corporate-spend-fbp-route"
        if best_describes_your_spend == procuring_something_else:
            return "exit-to-download-template-procurement-route" 

    if best_describes_your_situation == hire_contracted_workers_to_fill_temporary_capacity_gap:
        return "exit-to-download-template-hrbp-contingent-labour-route"
 
    return "we-could-not-find-the-right-process-for-you"

