APPOINTMENT_DATE_CONSTRAINT_NAME = (
    "appointment_date_must_be_in_the_future"
)
APPOINTMENT_DATE_ERROR_MESSAGE = (
    "Consulta só pode ser agendada para uma data posterior a hoje"
)
UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_CONSTRAINT_NAME = (
    "unique_appointment_date_health_care_worker"
)
UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_ERROR_MESSAGE = (
    "Consulta já existente para a combinação de data e profissional"
)


# From https://en.wikipedia.org/wiki/Health_professional
HEALTH_PRACTITIONERS_AND_PROFESSIONALS = (
    "Athletic trainer",
    "Audiologist",
    "Chiropractor",
    "Clinical coder",
    "Clinical nurse specialist",
    "Clinical officer",
    "Community health worker",
    "Dentist",
    "Dietitian and nutritionist",
    "Emergency medical technician",
    "Feldsher",
    "Health administrator",
    "Medical assistant",
    "Medical laboratory scientist",
    "Medical transcriptionist",
    "Nurse anesthetist",
    "Nurse practitioner",
    "Nurse midwife",
    "Nurse",
    "Occupational Therapist",
    "Optometrist",
    "Paramedic",
    "Pharmacist",
    "Pharmaconomist",
    "Pharmacy technician",
    "Phlebotomist",
    "Physician",
    "Physician assistant",
    "Podiatrist",
    "Psychologist",
    "Psychotherapist",
    "Physical therapist",
    "Radiographer",
    "Radiotherapist",
    "Respiratory therapist",
    "Speech-language pathologist",
    "Social Work",
    "Surgeon",
    "Surgeon's assistant",
    "Surgical technologist",
)


# Based on https://en.wikipedia.org/wiki/Preferred_gender_pronoun
PRONOUNS = (
    "He/him",
    "She/her",
    "They/them",
    "Xe/xem",
    "Ze/hir",
    "Ey/em",
    "Hir/hir",
    "Fae/faer",
    "Hu/hu",
)
