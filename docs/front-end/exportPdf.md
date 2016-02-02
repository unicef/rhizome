---
label: PDF Document
id: rhizome_front_end_pdf_doc
categorySlug: front_end
categoryLabel: Front End Document
categoryRank: 1
documentRank: 3

# Export PDF

## Tools

### Wkhtmltopdf
* Convert HTML to PDF

* Use Command Line Tool provided by Wkhtmltopdf to convert URL to PDF

* Wkhtmltopdf Version

* Use `--quiet` option 


## Docker

* Dockerfile

	1. Wkhtmltopdf Version
	
	2. xvfb-run
	
	3. xfonts-75dpi
	
	4. Server -> Manually Install
	

			# The version for local Debian env
			RUN sudo apt-get install -y xfonts-75dpi
			RUN wget http://download.gna.org/wkhtmltopdf/0.12/0.12.2.1/wkhtmltox-0.12.2.1_linux-jessie-amd64.deb

			RUN sudo dpkg -i wkhtmltox-0.12.2.1_linux-jessie-amd64.deb
			RUN rm wkhtmltox-0.12.2.1_linux-jessie-amd64.deb

			# The version for server Ubuntu env
			RUN wget http://download.gna.org/wkhtmltopdf/0.12/0.12.2.1/wkhtmltox-0.12.2.1_linux-trusty-amd64.deb
			RUN sudo dpkg -i wkhtmltox-0.12.2.1_linux-trusty-amd64.deb
			RUN rm wkhtmltox-0.12.2.1_linux-trusty-amd64.deb

		
## Backend
* URL

		# PRINT DASHBOARDS
    	url(r'^dashboards/export_pdf/?$',views.export_pdf, name='export_pdf'),

* View

```
		from datapoints.pdf_utils import print_pdf
		from rhizome.settings.base import STATICFILES_DIRS

		def export_file(request):
    file_type = request.GET['type']
    url = request.GET['path']
    file_name = 'dashboards.' + file_type
    css_file = 'file://' + STATICFILES_DIRS[0] + '/css/pdf.css'

    cookie = {}
    cookie['name'] = 'sessionid'
    cookie['value'] = request.COOKIES[cookie['name']]

    javascript_delay = '10000'

    if 'pdf' in file_type:
        options = {'orientation': 'Landscape', 'javascript-delay': javascript_delay, 'quiet': ' '}
        content_type = 'application/pdf'
    else:
        options = {'javascript-delay': javascript_delay, 'width': '1425', 'quality': '100', 'quiet': ' '}
        content_type = 'image/JPEG'

    pdf_content = print_pdf(type=file_type, url=url, output_path=None, options=options, cookie=cookie, css_file=css_file)

    if isinstance(pdf_content, IOError):
        response = HttpResponse(status=500)
    else:
        response = HttpResponse(content=pdf_content, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=' + file_name

    response.set_cookie('fileDownloadToken', 'true')
    return response
```


* PDF Util

```
  // pdf_utils.py
  class Configuration(object):
  
  def print_pdf(type, url, output_path, options=None, cookie=None, css_file=None):
    if 'pdf' in type:
      // print pdf
      wk_command = configuration.wkhtmltopdf.decode('utf-8')
    else:
      // print image
      wk_command = configuration.wkhtmltoimage.decode('utf-8')
  
  def to_pdf(args, path=None):
```

* Feature Toggle

  This project uses Django-waffle as a feature toggle tool.

  i. Command Line
		[Django-waffle](http://waffle.readthedocs.org/en/v0.11/usage/cli.html)
		
		```
		./manage.py waffle_switch pdf on --create
		```
		
  ii. [Django-admin](http://localhost:8000/admin)
  
  iii. [Using Waffle](http://waffle.readthedocs.org/en/v0.11/usage/index.html)		  	       		        		
 
  ```
  from waffle.decorators import waffle_switch

  @waffle_switch('pdf')
  def export_pdf(request):
  ```

  iv. Requirementst.txt

  ```
  django-waffle==0.11 
  ```


## Frontend

* Function Bind

	Since Webkit cannot support `bind` method in Javascript, so we need to replace bind method.
  ```
  function _replaceBindMethodForWktToPdf () {
      let replaceFunction = Function
      if (typeof replaceFunction.prototype.bind !== 'function') {
      ...
    }
  }
  ```

* PDF control iFrame

  ```
  // ExportPdf.jsx
  <iframe width='0' height='0' className='hidden' src={this.state.href}/>
  ```

* Using waffle in JS

  1. Django 
    ```
    # Waffle PATH
      url(r'^', include('waffle.urls')),
    ```
    			
  2. JS
    
  ```
  let exportPdf = ((waffle.switch_is_active('pdf')) && dashboardName === 'Management Dashboard')
      ? (<ExportPdf className='cd-titlebar-margin' />)
      : ''
  ```
      			
* package.json

  ```
  "standard": {
    "globals": [
        "describe",
        "context",
        "it",
        "waffle",
        "IsWkhtmlToPdf"
    ],
    "parser": "babel-eslint",
    "ignore": []
  }
  ```

* svg

	1. **viewbox**
	
	2. **bullet chart**

* IsWkhtmlToPdf

  ```
  // Polyfill.js
  global.IsWkhtmlToPdf = global.IsWkhtmlToPdf || (typeof Function.prototype.bind !== 'function')
  
  // browser.js
  export default {
      isIE: function () {
        return ('ActiveXObject' in window)
      },
      isWkhtmlToPdf: () => {
        return IsWkhtmlToPdf
      }
  }
  ```
		
* Button pop up after downloading

	Cookie
		
	Python -> Set cookit in response
		
	JS -> Set Interval -> Check cookie -> Clear Interval -> Delete cookie

		

## CSS

1. css file -> pdf.scss

2. Foundation

3. gulp

  ```
  entry: `${gulp.config('base.src')}/styles/pdf.scss`,
  src: [
    `${gulp.config('base.src')}/styles/_settings.scss`,
    `${gulp.config('base.src')}/styles/pdf.scss`
  ],
  dest: `${gulp.config('base.dist')}/static/css`
  ```
  
4. wkhtmltopdf

  ```
  from rhizome.settings.base import STATICFILES_DIRS
  
  css_file = 'file://' + STATICFILES_DIRS[0] + '/css/pdf.css'
    ...
  pdf_content = print_pdf(url=url, output_path=None, options=options, cookie=cookie, css_file=css_file)
  ```

 5. css file path
				
  ```
  from rhizome.settings.base import STATICFILES_DIRS\
  ```
