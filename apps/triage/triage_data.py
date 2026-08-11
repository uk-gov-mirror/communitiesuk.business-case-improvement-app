from .slugs import *

class TriageData():
    def __init__(self, triage_dict: dict):
        self.triage_data = triage_dict

    @property
    def total_value_of_business_case(self) -> str:
        return self.triage_data.get(total_value_of_business_case, "")

    @property
    def is_novel(self) -> bool:
        return self.triage_data.get(novel_repercussive_contentious_hmt_consent, "") == "yes"

    @property
    def is_pilot(self) -> bool:
            return self.triage_data.get(is_this_request_a_pilot, "") == "yes"
    @property
    def is_three_stage_process_novel_or_pilot(self) -> bool:
        return self.is_novel or self.is_pilot

    @property
    def is_part_of_wider_programme_with_existing_fbc(self) -> bool:
        return self.triage_data.get(part_of_wider_programme_with_existing_fbc, None) == "yes"

    @property
    def does_involve_digital(self) -> bool:
        return self.triage_data.get(does_request_involve_anything_digital, None) == "yes"

    @property
    def is_existing_programme(self) -> bool:
        return self.triage_data.get(is_this_request_part_of_a_wider_programme_with_existing_business_case, None) == "yes"

    @property
    def where_is_the_budget_held(self) -> str:
        return self.triage_data.get(where_is_the_budget_held, "")

    @property
    def business_case_title(self) -> str:
        return self.triage_data.get(give_your_bjc_a_name, "")

    @property
    def which_option_best_describes_the_spend(self) -> str:
        return self.triage_data.get(which_best_describes_your_spend, "")

    @property
    def is_corporate_spend_or_procurement(self) -> bool:
        return self.triage_data.get(which_best_describes_your_spend, None) != ""

    @property
    def summary(self) -> str:
        return self.triage_data.get(provide_a_high_level_summary, "")

    @property
    def which_option_best_describes_what_is_trying_to_be_done(self) -> str:
        return self.triage_data.get(which_option_describes_what_you_are_trying_to_do, "")

    @property
    def is_commission_research(self) -> bool:
        is_not_novel = self.triage_data.get(novel_repercussive_contentious_hmt_consent, None) == "no"
        is_not_pilot = self.triage_data.get(is_this_request_a_pilot, None) == "no"
        is_not_existing_programme = self.triage_data.get(is_this_request_part_of_a_wider_programme_with_existing_business_case, None) == "no"
        is_not_digital_budget = self.triage_data.get(where_is_the_budget_held, None) != ""
        is_trying_to_commission_research = self.triage_data.get(which_option_describes_what_you_are_trying_to_do, None) == commission_research

        return (is_not_novel and
            is_not_pilot and
            is_not_existing_programme and
            is_not_digital_budget and
            is_trying_to_commission_research)

    def get_answer_string(self, slug: str) -> str:
        return self.triage_data.get(slug, "")
    
    def get_is_answer_equal_to(self, slug: str, desired_value: str) -> bool:
        return self.triage_data.get(slug, "") == desired_value
    
