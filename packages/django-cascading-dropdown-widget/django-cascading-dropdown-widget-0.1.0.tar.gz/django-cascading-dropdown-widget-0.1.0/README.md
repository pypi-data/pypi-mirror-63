# django-cascading-dropdown-widget

Provide a cascading-dropdown widget for django.

## Install

```shell
pip install django-cascading-dropdown-widget
```

## Usage

**pro/settings.py**

**Note:**

- The application used static file jquery3/jquery.js, so MUST include django_static_jquery3 in INSTALLED_APPS.
- The application used template of django_cascading_dropdown_widget, so MUST include django_cascading_dropdown_widget in INSTALLED_APPS.

```python
INSTALLED_APPS = [
    ...
    'django_static_jquery3',
    'django_cascading_dropdown_widget',
    ...
]
```

**app/admin.py**

**Note:**

- Create a new ModelForm, and setting field widget to DjangoCascadingDropdownWidget.
- Use CascadingModelchoices while creating DjangoCascadingDropdownWidget.
- The parameters for DjangoCascadingDropdownWidget are the CASCADING-MODEL-SETTINGS. A MODEL-SETTING's config items are:
    - model, required. The Model class.
    - related_name, required but except for the last model-setting. Use the related_name to get the queryset of the next level items.
    - fk_name, required but except for the first model-setting. Which field name to get parent model.
    - empty, optional. Use *empty* string instread of '----- xxx ----' in select for empty value.
    - str, optional. Get item title from *str* method or property instread of get title by *str(item)*.

```python
from django.contrib import admin
from django_cascading_dropdown_widget.widgets import DjangoCascadingDropdownWidget
from django_cascading_dropdown_widget.widgets import CascadingModelchoices
from django import forms
from .models import Category
from .models import Book
from .models import Character

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []
        widgets = {
            "book": DjangoCascadingDropdownWidget(choices=CascadingModelchoices({
                "model": Category,
                "related_name": "books",
            },{
                "model": Book,
                "fk_name": "category",
            })),
        }

class CharacterAdmin(admin.ModelAdmin):
    form = CharacterForm
    list_display = ["name", "book"]
```

## MPTTModel supported!

- Create *indented_title* function for the MPTTModel.

    ```
    class MyModel(MPTTModel):
        def indented_title(self):
            return ("-"*4) * self.get_level() + self.name
    ```

- Setting ```"str": "indented_title"``` in MODEL-SETTING.
- That's ALL.
- The application django-cascading-dropdown-widget is NOT required django-mptt, so install django-mptt by youself. We have did try...except... with django-mptt's missing.

## Releases

### v0.1.0 2020/03/16

- Fisrt release.