from pathlib import Path
import govuk_frontend_jinja
from django.contrib.messages import get_messages
from django.middleware.csrf import get_token
from django.templatetags.static import static
from django.urls import reverse
from jinja2 import ChoiceLoader, Environment, FileSystemLoader
from markupsafe import Markup
from apps.core.shared_context import external_links

BASE_DIR = Path(__file__).resolve().parent.parent

GOVUK_PACKAGE = Path(govuk_frontend_jinja.__file__).parent
GOVUK_SITE_PACKAGES = GOVUK_PACKAGE.parent


def csrf_field(request):
    return Markup(
        f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
    )


def environment(**options):
    options.pop("loader", None)
    options.pop("undefined", None)
    options["autoescape"] = True

    env = Environment(
        loader=ChoiceLoader(
            [
                # Our own templates
                FileSystemLoader(str(BASE_DIR / "templates")),
                # gov imports: govuk_frontend_jinja/templates/components/...
                FileSystemLoader(str(GOVUK_SITE_PACKAGES)),
                # For internal package imports: govuk_frontend_jinja/macros/...
                # this maps to the templates/macros/... folder inside the package
                FileSystemLoader(str(GOVUK_PACKAGE / "templates")),
            ]
        ),
        **options,
    )
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            "get_messages": get_messages,
            "csrf_field": csrf_field,
            "external_links": external_links(None)["links"],
            "Markup": Markup,
        }
    )
    return env
