import os

from django.template import loader
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from .generators import PDFGenerator
from .settings import pdf_settings
from .utils import get_random_filename



def render_pdf(filename, request, template_name, context=None, content_type=None, status=None, using=None, options={}):
	content = loader.render_to_string(template_name, context=context, request=request, using=using)
	if request.GET.get('html'):
		return HttpResponse(content, content_type, status)
	html_key = get_random_filename(20)
	html_filename = '%s.html' % html_key
	with open(os.path.join(pdf_settings.TEMPLATES_DIR, html_filename), 'w') as f:
		f.write(content.encode('utf8'))
		f.close()
	relative_url = reverse('pdf_generator:pdf_html', kwargs={'html_key': html_key})
	url = request.build_absolute_uri(relative_url)
	pdf = PDFGenerator(url, **options)
	return pdf.get_http_response(filename)
