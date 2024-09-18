# tasks.py
import pandas as pd
from celery import shared_task

from .models import Company


@shared_task(bind=True)
def process_csv(self, file_path):
    df = pd.read_csv(file_path)
    total_rows = len(df)
    companies = []
    for index, row in df.iterrows():
        if type(row["locality"]) == str:
            state_name = row["locality"].split(",")[1]
            city_name = row["locality"].split(",")[0]
        else:
            state_name = ""
            city_name = ""
        company = Company(
            name= row.get("name",""),
            domain= row.get("domain",""),
            year_founded= row.get("year founded",""),
            industry= row.get("industry",""),
            size_range= row.get("size range",""),
            country_name= row.get("country",""),
            state_name= state_name,
            city_name= city_name,
            linkedn_url= row.get("linkedin url",""),
            current_employee_count= row.get("current employee estimate",0),
            total_employee_count= row.get("total employee estimate",0),
        )
        companies.append(company)
        if (index + 1) % 100 == 0 or (index + 1) == total_rows:
            self.update_state(state='PROGRESS', meta={'current': index + 1, 'total': total_rows})
            if len(companies) >= 100000:
                Company.objects.bulk_create(companies)
                companies = []
