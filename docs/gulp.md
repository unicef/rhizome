#GULP Documentation

##Environment

In this project, we use gulp to build frontend system.

Gulp: use `npm install -g gulp` to install gulp.

Gulp src directory: `/webapp/src`

Gulp destination directory: `/webapp/public`

We have two basic **GULP TASKS**, `gulp` and `gulp dev`, they are defined in `gulpfile.babel.js`.

```
gulp.task('dev', () => {
  gulp.config(gulp.DEV_MODE, true)
  gulp.start(['build'])
})

gulp.task('default', ['build'])
```

* Use `gulp dev` in local development environment to build and watch frontend change.
* Use `gulp` in production environment for deployment.

##Tasks

We have sevaral gulp tasks, `clean, copy, sass, standard, browserify and revision`. 

All the tasks are defined seperately in `/webapp/tasks` folder.

###Clean

**Clean** task is used to remove the whole gulp destination directory `/webapp/public`  to prepare for next step.

###Copy

**Copy** task is used to copy all static assets from gulp src directory to gulp dest directory.

###Sass

**Sass** task is used to compile all sass files to css files.

###Standard

**Standard** task is used to check JavaScript code with the standard syntax.

###Browserify and Watchify

**Browserify** task is used to build a bundle which can be served up to browser in a single `<script>` tag.

**Watchify** task will update any source file and the browserify bundle will be recompiled on the spot.

###Revision

[**RevCompile**](https://github.com/sindresorhus/gulp-rev) task will revision static asset by appending content hash to filenames, such as `unicorn.css => unicorn-d41d8cd98f.css`.

This task will generation a `rev-manifest.json` file in `/webapp/public/static` folder to map the original paths to the revisioned paths.

To use the generated revisioning file, we defined a  `base.hbs` file with `<script>` tag like below:


	//This is base.hbs
	//static css files
	<link rel="stylesheet" href="{% static "{{ assetPath "css/screen.css" }}" %}">
	<link rel="stylesheet" href="{% static "{{ assetPath "css/print-redesign.css" }}" %}" media="print">

	//static js files
	<script src="{% static "{{ assetPath "js/vendor.js" }}" %}"></script>
	<script src="{% static "{{ assetPath "js/main.js" }}" %}"></script>


[**RevReplace**](https://github.com/sindresorhus/gulp-rev/blob/master/integration.md) task will replace the `<script>` tag in `base.hbs` based on `rev-manifest.json`, then will generate a `base.html` file.

Since we need to have a watchify task to reload static files in development env, so we have another `rev-manifest.json` file in `/webapp` folder to use in development env.

These two `rev-manifest.json` looks different:

```
//This is rev-manifest.json in deveopment env
{
  "css/pdf.css": "css/pdf.css",
  "css/print-redesign.css": "css/print-redesign.css",
  "css/screen.css": "css/screen.css",
  "js/main.js": "js/main.js",
  "js/vendor.js": "js/vendor.js"
}
```

```
//This is rev-manifest.json in production env
{
  "css/pdf.css": "css/pdf-1ceeaff80e.css",
  "css/print-redesign.css": "css/print-redesign-27445033fc.css",
  "css/screen.css": "css/screen-ddff506646.css",
  "js/main.js": "js/main-ea7844e656.js",
  "js/vendor.js": "js/vendor-24f5548b98.js"
}
```

In this way, we can use revisioning static files in production env, and will not influnce our development env.

So `base.html` in development env will not use revisioning files.

		
		//This is base.html in development env
		//static css files
		<link rel="stylesheet" href="{% static "css/screen.css" %}">
    	<link rel="stylesheet" href="{% static "css/print-redesign.css" %}" media="print">
		
		//static js files
		<script src="{% static "js/vendor.js" %}"></script>
		<script src="{% static "js/main.js" %}"></script>
		
And `base.html` in production env will use revisioning files.

		//This is base.html in production env
		//static css files
		<link rel="stylesheet" href="{% static "css/screen-ddff506646.css" %}">
    	<link rel="stylesheet" href="{% static "css/print-redesign-27445033fc.css" %}" media="print">
    	
		//static js files
		<script src="{% static "js/vendor-0a1c002fc5.js" %}"></script>
		<script src="{% static "js/main-efc4d25176.js" %}"></script>
		
		
###Lint

**Lint** task is used to identify and report on patterns found in ECMAScript/JavaScript code.

###Mocha

**Mocha** task is used to run Mocha tests in a separate process from the gulp process.

###Package

**Package** task is used to compress frontend code into a zip package.

