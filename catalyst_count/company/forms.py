from django import forms

from .models import Company


class FileUploadForm(forms.Form):
    file = forms.FileField()


class CompanyFilterForm(forms.Form):
    keyword = forms.CharField(required=False)
    industry = forms.ChoiceField(choices=[],required=False)
    year_founded = forms.ChoiceField(choices=[],required=False)
    city = forms.ChoiceField(choices=[],required=False)
    state = forms.ChoiceField(choices=[],required=False)
    country = forms.ChoiceField(choices=[],required=False)
    size_range = forms.ChoiceField(choices=[],required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['industry'].choices = self.get_unique_industries()
        self.fields['year_founded'].choices = self.get_unique_year_founded()
        self.fields['city'].choices = self.get_unique_cities()
        self.fields['state'].choices = self.get_unique_states()
        self.fields['country'].choices = self.get_unique_countries()
        self.fields['size_range'].choices = self.get_unique_size_ranges()

        # Set the initial values for the dropdowns
        self.fields['industry'].initial = 'Select Industry'
        self.fields['year_founded'].initial = 'Select Year Founded'
        self.fields['city'].initial = 'Select City'
        self.fields['state'].initial = 'Select State'
        self.fields['country'].initial = 'Select Country'
        self.fields['size_range'].initial = 'Select Size Range'

    def get_unique_industries(self):
        industries = Company.objects.values_list('industry', flat=True).distinct()
        return [('Select Industry','Select Industry')]+[(industry, industry) for industry in industries]

    def get_unique_year_founded(self):
        year_founded = Company.objects.values_list('year_founded', flat=True).order_by('-year_founded').distinct()
        return [('Select Year Founded','Select Year Founded')]+[(year, year) for year in year_founded]

    def get_unique_cities(self):
        cities = Company.objects.exclude(city_name='').values_list('city_name', flat=True).order_by('city_name').distinct()
        return [('Select City','Select City')]+[(city, city) for city in cities]

    def get_unique_states(self):
        states = Company.objects.exclude(state_name='').values_list('state_name', flat=True).order_by('state_name').distinct()
        return [('Select State','Select State')]+[(state, state) for state in states]

    def get_unique_countries(self):
        countries = Company.objects.exclude(country_name='').values_list('country_name', flat=True).order_by('country_name').distinct()
        return [('Select Country','Select Country')]+[(country, country) for country in countries]

    def get_unique_size_ranges(self):
        size_range = Company.objects.exclude(size_range='').values_list('size_range', flat=True).order_by('size_range').distinct()
        return [('Select Size Range','Select Size Range')]+[(range, range) for range in size_range]