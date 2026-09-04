from django import forms

class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with library catalog data',
        widget=forms.FileInput(attrs={'accept': '.csv'})
    )
    update_existing = forms.BooleanField(
        required=False,
        initial=False,
        label='Update existing records',
        help_text='Update records with matching control_no'
    )
    skip_header = forms.BooleanField(
        required=False,
        initial=True,
        label='Skip header row',
        help_text='Check if your CSV has a header row'
    )