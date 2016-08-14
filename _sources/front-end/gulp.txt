Building the front end with Gulp
================================




---
label: Gulp Document
id: rhizome_front_end_gulp_doc
categorySlug: front_end
categoryLabel: Front End Document
categoryRank: 1
documentRank: 4

# GULP Documentation

## Environment

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
* Use `gulp build` in production environment for deployment.

## Tasks

We have sevaral gulp tasks, `clean, copy, sass, standard, browserify and revision`.

All the tasks are defined seperately in `/webapp/tasks` folder.

### Clean

**Clean** task is used to remove the whole gulp destination directory `/webapp/public`  to prepare for next step.

### Copy

**Copy** task is used to copy all static assets from gulp src directory to gulp dest directory.

### Sass

**Sass** task is used to compile all sass files to css files.

### Standard

**Standard** task is used to check JavaScript code with the standard syntax.

We're using [standard](https://github.com/feross/standard) with [babel-eslint](https://github.com/babel/babel-eslint) to format our Javascript code. Make sure run standard before committing any Javascript code.

Install `standard` and `babel-eslint` by `npm install -g standard` and `npm install -g babel-eslint`. They must be installed globally. Run `standard` in `/webapp` folder to check Javascript format. Fix any format error before you commit.

Standard will be added to CI pipeline to ensure the code format is strictly followed.

Here's a quick view of standard rules. For more details, visit standard homepage or check standard error output.

* 2 spaces for indentation. No tab is allowed.
* Single quotes for strings.
* No unused variables.
* No semicolons.
* Always use === instead of == except for `null`.
* Space after keywords as `if` and function name.
* React props must be defined by `propTypes`.

### Browserify and Watchify

**Browserify** task is used to build a bundle which can be served up to browser in a single `<script>` tag.

**Watchify** task will update any source file and the browserify bundle will be recompiled on the spot.

### Revision

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

In this way, we can use revisional static files in production env, and will not influence our development env.

How to use these two manifest file in different env are defined in `/tasks/config/revReplace.js`:

```
var proManifest =  jsDestFolder + '/rev-manifest.json'
var devManifest = './rev-manifest.json'
var manifestFile = (process.env.NODE_ENV === 'production') ? proManifest : devManifest
```

So `base.html` in **development env** will not use revisional files.


		//This is base.html in development env
		//static css files
		<link rel="stylesheet" href="{% static "css/screen.css" %}">
    	<link rel="stylesheet" href="{% static "css/print-redesign.css" %}" media="print">

		//static js files
		<script src="{% static "js/vendor.js" %}"></script>
		<script src="{% static "js/main.js" %}"></script>

And `base.html` in **production env** will use revisional files.

		//This is base.html in production env
		//static css files
		<link rel="stylesheet" href="{% static "css/screen-ddff506646.css" %}">
    	<link rel="stylesheet" href="{% static "css/print-redesign-27445033fc.css" %}" media="print">

		//static js files
		<script src="{% static "js/vendor-0a1c002fc5.js" %}"></script>
		<script src="{% static "js/main-efc4d25176.js" %}"></script>


### Lint

**Lint** task is used to identify and report on patterns found in ECMAScript/JavaScript code.

### Mocha

[**Mocha**](https://github.com/knpwrs/gulp-spawn-mocha) task is used to run Mocha tests in a separate process from the gulp process.

We can use `gulp mocha` to run the tests separately from other tasks.

And `gulp mocha` will also generate a coverage report for frontend code. The report is in `/webapp/coverage/lcov-report/` folder and you can view the report through `/webapp/coverage/lcov-report/index.html` file.

If you do not want to test the coverage, you can change the config in `/tasks/config/mocha.js`:

```
export default {
  src: [
    `${gulp.config('base.src')}/**/__tests__/*.spec.js{,x}`
  ],
  options: {
    r: 'src/helpers/jsdom.js',
    R: 'dot',
    compilers: '.:babel/register',
    istanbul: true  // Will test coverage and generate report.
    istanbul: false  // Will not test coverage and generate report.
  }
}

```

### Package

**Package** task is used to compress frontend code into a zip package.
