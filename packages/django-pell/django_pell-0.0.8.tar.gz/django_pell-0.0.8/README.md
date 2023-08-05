# Django Pell

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![coverage report](https://gitlab.com/BradleyKirton/django-pell/badges/master/coverage.svg?job=test)](https://gitlab.com/BradleyKirton/django-pell/)

Custom django widget built on [pell](https://github.com/jaredreich/pell).

![Django Pell in action](django_pell.png)


## Usage

```python
class EditorForm(forms.Form):
    """Simple form which exposes the Django Pell Widget."""

    editor = forms.CharField(
        widget=PellWidget(),
        help_text='Pell is "the simplest and smallest WYSIWYG text editor for web, with no dependencies"',
        label=False,
    )


def editor_view(request):
    """Simple view which renders the EditorForm."""

    return render(
        request,
        "editor.html",
        context={"form": EditorForm()},
    )
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
{{ form.media }}
<body>
  {{ form.as_p }}
</body>
</html>
```

For a complete example check out the `example` included in this repo.
