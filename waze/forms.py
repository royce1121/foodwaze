from django import forms
from .models import Restaurant
from .models import Menu
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.utils.translation import gettext as _
from django.forms.models import inlineformset_factory
from django.forms import formset_factory
from django.forms import BaseFormSet
from fancy_formsets.helper import InlineFormsetHelper
from fancy_formsets.forms import FancyBaseInlineFormSet


class RestaurantForm(forms.ModelForm):
    
    name = forms.CharField(
		label=_('Restaurant\'s Name'),
		required=False,
	)

    description = forms.CharField(
        label=_('Restaurant\'s Description'),
        required=False,
    )

    latitude = forms.FloatField(
        label=_('Latitude'),
        required=False,
        help_text=_('Specify latitude of the restaurant to properly mark in the google map.'),
    )

    longitude = forms.FloatField(
        label=_('Longitude'),
        required=False,
        help_text=_('Specify longitude of the restaurant to properly mark in the google map.'),
    )

    restau_img_url = forms.CharField(
        label=_('Restaurant\'s Image URL'),
        required=False,
        help_text=_('Kindly paste here the restaurant image url for us to showcase it in the system.'),
    )

    class Meta:
        model = Restaurant
        fields = (
        	'name',
        	'description',
        	'longitude',
			'latitude',
			'restau_img_url',
			'restau_type',
        )

    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        self.fields['restau_type'].label = "Restaurant Type"

    def clean(self):
        name = self.cleaned_data.get('name', None)
        description = self.cleaned_data.get('description', None)
        longitude = self.cleaned_data.get('longitude', None)
        latitude = self.cleaned_data.get('latitude', None)

        if not name:
            raise forms.ValidationError(_('Name is required.'))

        if not description:
            raise forms.ValidationError(_('Description is required.'))

        if not longitude:
            raise forms.ValidationError(_('Latitude is required.'))

        if not latitude:
            raise forms.ValidationError(_('Longitude is required.'))

        return self.cleaned_data

    def set_layout(self):
        self.helper.layout = Layout(
			'name',
			'description',
			'longitude',
			'latitude',
			'restau_type',
            'restau_img_url',
        )

    def save(self, commit=True, *args, **kwargs):
        self.instance = super(RestaurantForm, self).save(commit=False, *args, **kwargs)
        if commit:
            self.instance.save()
        return self.instance


class RestaurantFilterForm(forms.Form):
    q = forms.CharField(
        label=_(''),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Look for restaurant name',
            }
        )
    )
    restau_type = forms.ChoiceField(
        label=_(''),
        choices=[('', 'Type')] + list(Restaurant.RESTAU_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def set_layout(self):
        self._helper.disable_csrf = True
        self._helper.form_show_labels = False


class AddMenuForm(forms.ModelForm):
    description = forms.CharField(
        label=_('Description'),
        required=False,
    )

    class Meta:
        model = Menu
        fields = [
            'name',
            'description',
            'price',
            'restaurant',
            'is_specialty',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request') or None
        super(AddMenuForm, self).__init__(*args, **kwargs)
        self.fields['is_specialty'].label = "Specialty"


class AddMenuBaseFormSet(FancyBaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.extra_kwargs = self.get_formset_extra_kwargs(kwargs)
        super(
            AddMenuBaseFormSet,
            self).__init__(*args, **kwargs)

    def get_formset_extra_kwargs(self, kwargs):
        extra_kwargs = {
            'request': kwargs.pop('request', None),
        }
        return extra_kwargs

    def _construct_form(self, i, **kwargs):
        kwargs.update(self.extra_kwargs)
        return super(AddMenuBaseFormSet, self)._construct_form(i, **kwargs)

    def clean(self):
        name_list = []
        for form in self.forms:
            name = form.cleaned_data.get('name', None)
            if name in name_list:
                raise forms.ValidationError(
                    _('Duplicate Data'))
            else:
                name_list.append(name)


AddMenuFormSet = inlineformset_factory(
    Restaurant,
    Menu,
    form=AddMenuForm,
    formset=AddMenuBaseFormSet,
    extra=2,
)
AddMenuFormSet.helper = InlineFormsetHelper()
