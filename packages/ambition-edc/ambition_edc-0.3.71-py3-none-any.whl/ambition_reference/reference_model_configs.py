from edc_reference import site_reference_configs

site_reference_configs.register_from_visit_schedule(
    visit_models={"edc_appointment.appointment": "ambition_subject.subjectvisit"}
)

configs = {
    "ambition_subject.education": ["household_head"],
    "ambition_subject.patienthistory": ["cd4_date", "viral_load_date"],
    "ambition_subject.medicalexpenses": ["care_before_hospital"],
    "ambition_subject.week16": ["patient_alive"],
}

for reference_name, fields in configs.items():
    site_reference_configs.add_fields_to_config(name=reference_name, fields=fields)
