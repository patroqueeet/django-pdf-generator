[![django-pdf-generator v0.1.0 on PyPi](https://img.shields.io/badge/pypi-0.1.0-green.svg)](https://pypi.python.org/pypi/django-pdf-generator)
![MIT license](https://img.shields.io/badge/licence-MIT-blue.svg)
![Stable](https://img.shields.io/badge/status-stable-green.svg)

# django-pdf-generator
Convert HTML to pdf with django using phantomjs


## Requirements

+ Python (2.7) (Need to be tested for 3.x)
+ Django (1.10, 1.9) (Need to be tested for previous versions)


## Installation

Install using `pip` :


`pip install django_pdf_generator`


Add `pdf_generator` to your INSTALLED_APPS setting.


    INSTALLED_APPS = (
        ...
        'pdf_generator',
    )


## Example

Generate a pdf from an url and save it to database, or retrieve it as a ContentFile, or return it inside an HttpResponse :


	from pdf_generator.generators import PDFGenerator

	pdf = PDFGenerator(url="https://github.com/charlesthk/django-pdf-generator",
	
	# Save it to database and retrieve a PdfDoc Object (database):
	pdf.save(
			filename='pdf_generator',
			title="pdf_generator on github",
			description="Convert HTML to pdf with django using phantomjs")

	# Get the PDf as a Django ContentFile named 'my_pdf_file.pdf' :
	pdf_content_file = pdf.get_content_file('my_pdf_file') 

	# Return a Django HttpResponse with the PDF Attached named 'my_pdf_file.pdf':
	return pdf.get_http_response('my_pdf_file')


Generate a pdf just like Django `render` function :

urls.py


    url(r'^invoice$', views.invoice, name='invoice'),


views.py


    from pdf_generator.renderers import render_pdf

    def invoice(request):
        """
        Render an invoice
        The invoice.pdf file is returned
        """
        return render_pdf('invoice', request, 'front/invoice.html')


Juste add `?html=1` to view the HTML instead of getting the pdf file


## `PDFGenerator` options

The `PDFGenerator` class accepts the following arguments :

+ url				[required]
+ paperformat 		[Required] default to 'A4', examples: "5in*7.5in", "10cm*20cm", "A4", "Letter"
+ zoom              [Optional] default to 1.
+ script 			[Optional] default to DEFAULT_RASTERIZE_SCRIPT, defines which render script to use.
+ temp_dir 			[Optional] default to DEFAULT_TEMP_DIR, defines which temp dir to use.


## Model used for saving PDF

When using `save(filename, title='', description='')` method of `PDFGenerator`, the following model is used:


    class PdfDoc(models.Model):
    	"""
    	Store each generated pdf
    	"""
    	title = models.CharField(verbose_name=_("Title"), max_length=255, blank=True)
    	description = models.TextField(verbose_name=_("Description"), blank=True)
    	document = models.FileField(verbose_name=_("Document PDF"), upload_to=pdf_settings.UPLOAD_TO)
    	created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Creation'))
    	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Update'))


## Settings

Add your settings to your main django settings file. The settings are set by default to :

    PDF_GENERATOR = {
        'UPLOAD_TO': 'pdfs',
        'PHANTOMJS_BIN_PATH': 'phantomjs',
        'DEFAULT_RASTERIZE_SCRIPT': os.path.join(PDF_GENERATOR_DIR, 'rasterize.js'),
        'DEFAULT_TEMP_DIR': os.path.join(PDF_GENERATOR_DIR, 'temp'),
        'TEMPLATES_DIR': os.path.join(PDF_GENERATOR_DIR, 'templates/pdf_generator')
    }


### `UPLOAD_TO`

Define the directory or the function to be used when saving PDFs, default to `pdfs`.

### `PHANTOMJS_BIN_PATH`

Define the path to Phantomjs binary, default to `phantomjs`.


### `DEFAULT_RASTERIZE_SCRIPT`

Define which render_script to use by default, default to `rasterize.js` inside the package.


### `DEFAULT_TEMP_DIR`

Define the directory to use for temporarily generated pdf by PhantomJS. default to `pdf_temp`.


### `TEMPLATES_DIR`

Define the directory to use for temporarily generated HTML files by PhantomJS. default to `pdf_temp`.



## Support

If you are having issues, please let us know or submit a pull request.

## License

The project is licensed under the MIT License.
