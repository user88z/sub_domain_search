from django import forms

from domain_parser.models import Input_data



class DataForm(forms.ModelForm):

	class Meta:
		model = Input_data
		fields = [
			'main_domain',
			'depth',
		]