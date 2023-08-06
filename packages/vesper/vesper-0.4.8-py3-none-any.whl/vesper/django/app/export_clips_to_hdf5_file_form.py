from django import forms

import vesper.django.app.form_utils as form_utils
import vesper.django.app.model_utils as model_utils


class ExportClipsToHdf5FileForm(forms.Form):
    

    detectors = forms.MultipleChoiceField(label='Detectors')
    station_mics = forms.MultipleChoiceField(label='Station/mics')
    classification = forms.ChoiceField(label='Classification')
    start_date = forms.DateField(label='Start date')
    end_date = forms.DateField(label='End date')
    
    output_file_path = forms.CharField(
        label='Output file', max_length=255,
        widget=forms.TextInput(attrs={'class': 'command-form-wide-input'}))
    
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        # Populate detectors field.
        self.fields['detectors'].choices = \
            form_utils.get_processor_choices('Detector')

        # Populate station/mics field.
        names = model_utils.get_station_mic_output_pair_ui_names()
        choices = [(name, name) for name in names]
        self.fields['station_mics'].choices = choices

        # Populate classification field.
        self.fields['classification'].choices = \
            form_utils.get_string_annotation_value_choices('Classification')
