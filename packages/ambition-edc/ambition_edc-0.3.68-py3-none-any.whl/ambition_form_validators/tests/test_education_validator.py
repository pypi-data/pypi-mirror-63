from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import NO

from ..form_validators import EducationFormValidator


@tag("ambition_form_validators")
class TestEducationalBackgroundFormValidator(TestCase):
    def test_total_money_spent_error(self):
        cleaned_data = {
            "education_years": 15,
            "elementary_years": 10,
            "secondary_years": 5,
            "higher_years": 10,
        }
        form_validator = EducationFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("education_years", form_validator._errors)

    def test_total_money_spent(self):
        cleaned_data = {
            "education_years": 25,
            "elementary_years": 10,
            "secondary_years": 5,
            "higher_years": 10,
        }
        form_validator = EducationFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_elementary_years(self):
        cleaned_data = {"elementary": NO, "elementary_years": 1, "education_years": 1}
        form = EducationFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("elementary_years", form._errors)

    def test_secondary_years(self):
        cleaned_data = {"secondary": NO, "secondary_years": 1, "education_years": 1}
        form = EducationFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("secondary_years", form._errors)

    def test_higher_education(self):
        cleaned_data = {"higher_education": NO, "higher_years": 1, "education_years": 1}
        form = EducationFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn("higher_years", form._errors)
