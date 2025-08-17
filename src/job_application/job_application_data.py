from src.job_application.schemas import JobApplication, Status

job_applications: list[JobApplication] = [
    JobApplication(
        id=1,
        job_title="Frontend Developer",
        company_name="TechWave",
        location="New York, NY",
        application_date="2025-07-10",
        status=Status.APPLIED
    ),
    JobApplication(
        id=2,
        job_title="UI/UX Designer",
        company_name="DesignHub",
        location="Remote",
        application_date="2025-07-12",
        status=Status.INTERVIEWED
    ),
    JobApplication(
        id=3,
        job_title="Backend Engineer",
        company_name="Cloudify",
        location="San Francisco, CA",
        application_date="2025-07-14",
        status=Status.REJECTED
    ),
    JobApplication(
        id=4,
        job_title="Data Analyst",
        company_name="Insight Corp",
        location="Chicago, IL",
        application_date="2025-07-15",
        status=Status.OFFERED
    ),
    JobApplication(
        id=5,
        job_title="DevOps Engineer",
        company_name="NextGen Systems",
        location="Remote",
        application_date="2025-07-20",
        status=Status.SAVED
    ),
]