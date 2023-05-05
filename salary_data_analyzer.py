import csv
import matplotlib.pyplot as plt

class JobListing:
    def __init__(self, work_year, experience_level, employment_type, job_title, salary, salary_currency, salary_in_usd, employee_residence, remote_ratio, company_location, company_size):
        self.work_year = work_year
        self.experience_level = experience_level
        self.employment_type = employment_type
        self.job_title = job_title
        self.salary = salary
        self.salary_currency = salary_currency
        self.salary_in_usd = salary_in_usd
        self.employee_residence = employee_residence
        self.remote_ratio = remote_ratio
        self.company_location = company_location
        self.company_size = company_size

def read_csv(filename):
    job_listings = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        for row in reader:
            try:
                row[6] = float(row[6])  # convert salary_in_usd to float
            except ValueError:
                row[6] = 0  # set invalid value to 0
            job = JobListing(*row)
            job_listings.append(job)
    return job_listings

def find_top_job_titles(job_listings, n=10):
    sorted_jobs = sorted(job_listings, key=lambda x: x.salary_in_usd or 0, reverse=True)
    top_jobs = sorted_jobs[:n]
    return top_jobs

def calculate_average_salary(job_listings):
    salaries = [float(job.salary_in_usd) for job in job_listings]
    average_salary = sum(salaries) / len(salaries)
    return average_salary

def sort(job_titles, average_salaries):
    n = len(job_titles)
    for i in range(n):
        # Perform n-i-1 comparisons in each iteration
        for j in range(n-i-1):
            # Compare salaries and swap positions if necessary
            if average_salaries[j] > average_salaries[j+1]:
                average_salaries[j], average_salaries[j+1] = average_salaries[j+1], average_salaries[j]
                job_titles[j], job_titles[j+1] = job_titles[j+1], job_titles[j]

# Example usage:
job_listings = read_csv('ds_salaries.csv')
top_jobs = find_top_job_titles(job_listings)

# Extract job titles and average salaries
job_titles = [job.job_title for job in top_jobs]
average_salaries = []
for job in top_jobs:
    matching_jobs = [j for j in job_listings if j.job_title == job.job_title]
    average_salary = calculate_average_salary(matching_jobs)
    average_salaries.append(average_salary)
    
sort(job_titles, average_salaries)

# Create bar chart
fig, ax = plt.subplots()
# ax.bar(job_titles, average_salaries)
ax.barh(job_titles[::], average_salaries[::])

# Set chart title and labels
ax.set_title('Top 10 Data Science Jobs by Salary')
ax.set_xlabel('Job Title')
ax.set_ylabel('Average Salary (USD)')

# Rotate x-axis labels for readability
plt.xticks(rotation=90)

# Display chart
plt.show()
