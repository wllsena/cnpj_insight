# Welcome to the CNPJ Insight project!

## How to run

If you want to run locally, you can download the SQLite database in [this drive](https://drive.google.com/file/d/1Rpl5RAMi0dN9nUSKiFoBFUoAU5mxIRbJ/view?usp=sharing), otherwise, you can check out the cloud-deployed version in [http://20.195.169.122:8000/](http://20.195.169.122:8000/).

Just let the database file in the root folder of the project. If you want to start a new database, you can migrate.

### Production
```bash
docker-compose -f docker-compose.prod.yml up --build
```

Access: http://localhost:1337

### Development
```bash
docker-compose -f docker-compose.yml up --build
```

Access: http://localhost:8000

In order to run the tests you need to run the following command:

```bash
docker-compose -f docker-compose.yml run --rm web python manage.py test
```

If you have any problems with the docker-compose, try to using the branch `dockerless`.


### Stop

```bash
docker-compose down -v
```

## API Reference

### Admin

::: cnpj.admin
    options:
        heading_level: 4

### Apps

::: cnpj.apps
    options:
        heading_level: 4

### Documents

::: cnpj.documents
    options:
        heading_level: 4

### Forms

::: cnpj.forms
    options:
        heading_level: 4

### Models

::: cnpj.models
    options:
        heading_level: 4

### Structure

::: cnpj.structure
    options:
        heading_level: 4

### Tests

::: cnpj.tests.test_urls
    options:
        heading_level: 4

::: cnpj.tests.test_views
    options:
        heading_level: 4

### Utils

::: cnpj.utils
    options:
        heading_level: 4

### Views

::: cnpj.views
    options:
        heading_level: 4

## Coverage

See in detail the coverage in [coverage_report.pdf](https://github.com/wllsena/cnpj_insight/blob/main/coverage_report.pdf).

```
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
cnpj/__init__.py                0      0   100%
cnpj/admin.py                  60      0   100%
cnpj/apps.py                    4      0   100%
cnpj/cron.py                    6      6     0%   1-9
cnpj/documents.py              15      0   100%
cnpj/forms.py                   8      0   100%
cnpj/models.py                124     12    90%   36, 45, 54, 63, 74, 83, 104, 149, 164, 203, 230-231
cnpj/structure.py              41     41     0%   1-142
cnpj/tests/__init__.py          0      0   100%
cnpj/tests/test_forms.py        0      0   100%
cnpj/tests/test_models.py       0      0   100%
cnpj/tests/test_urls.py        25      0   100%
cnpj/tests/test_views.py       69      0   100%
cnpj/urls.py                    3      0   100%
cnpj/utils.py                  83     71    14%   61-90, 117-197, 212-286
cnpj/views.py                  72     23    68%   124-147, 173-180, 216-222, 282-291, 337-349
cnpj_insight/__init__.py        0      0   100%
cnpj_insight/asgi.py            9      9     0%   10-34
cnpj_insight/settings.py       29      0   100%
cnpj_insight/urls.py            4      0   100%
cnpj_insight/wsgi.py            4      4     0%   10-14
manage.py                      12      2    83%   12-13
media/__init__.py               0      0   100%
static/__init__.py              0      0   100%
staticfiles/__init__.py         0      0   100%
templates/__init__.py           0      0   100%
---------------------------------------------------------
TOTAL                         568    168    70%

```