---
label: Front End Document
id: rhizome_front_end_doc
categorySlug: front_end
categoryLabel: Front End Document
categoryRank: 1
documentRank: 1

# Front-end Documentation

## Environment

Node: >= 0.10, suggested 0.12. Don't use Node 4.0.

Npm: >= 2.0. Feature of installing local dependency is needed.

Working direction: `/webapp`

## Code Principle
### standard

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

### General Rules

We're using ES6(ECMAScript 6) entirely in our project. There are also some general rules which are not restricted by standard but we need to follow. As soon as we format the legacy code, these rules will also be added into standard lint.

Use ES6 recommended principle as much as you can. For example:

* Use camel case instead of snake case for variables and function names. For example, `getIndicatorTag` instead of `get_indicator_tag`.
* Use `let` and `const` instead of `var`. [http://eslint.org/docs/rules/no-var.html](http://eslint.org/docs/rules/no-var.html)
* Use arrow function to avoid using `let self = this`. See example below. More details about how `this` in arrow function is different from ES5 function. [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions#Lexical_this](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions#Lexical_this)

```javascript
// Good
let items = arr.map(item => {
	return this.createItem(item)
})

//Bad
let self = this
let items = arr.map(function (item) {
	return self.createItem(item)
})
```

* Use rest parameters instead of `arguments`. No `Array.prototype.slice.call(arguments)` is needed. [https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Functions/rest_parameters](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Functions/rest_parameters)
* Use method properties. [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Method_definitions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Method_definitions). For example:

```javascript
// Good
export default {
	create () {},
	destroy () {}
}

// Bad
export default {
	create: function () {},
	destroy: function () {}
}
```

* React file should be named as `.jsx` instead of `.js`.


## Test

We're using mocha/chai as our test suites. Run `gulp mocha` will run all front end tests.

Test suite file is located in `__tests__` directory which is in the same level of the tested file. Test file name is ended with `.spec.js(x)`, depending on original file name.

```
component
 |- __tests__
 |   |_ MenuItem.spec.jsx
 |_ MenuItem.jsx
```

Use existing spec file as example to create new spec when needed.

Javascript tests are focused on dealing complicate data model and processing, rather than UI interaction. Tests now are in Unit Test level.

## React/Reflux

**Avoid sending API request in store.init()**

Reflux store.init() will be called when store is initialized. Put API request in store.init() will send request when a page is launched no matter whether it is necessary and worsen the performance.

It's better to send API request via a Reflux action.

**Avoid binding store directly on state**

Binding store directly on state is easily overriden therefore not stable. It's better to bind onto a property of state.

Use

`mixins: [Reflux.connect(DataExplorerStore, 'data')]`

instead of

`mixins: [Reflux.connect(DataStore)]`

**Write React in ES6+**

Writing React in ES6/ES7 is not compulsory but highly recommended. Read this [guide](http://babeljs.io/blog/2015/06/07/react-on-es6-plus/) in babeljs.org.

## File Structure

```
rhizome
 |- webapp
    |- public
       |- static
       |  |- ....
       |_ index.html
    |- src
       |- actions
       |- chart
       |- component
       |- dashboard
       |- store
       |- ufadmin
       |- view
       |- ....
       |_ Rhizome.js
       |_ ....
```

As above file structure, all front-end files store in rhizome/webapp folder, and we use [Gulp](gulp.md) to generate script and html files to `public` folder.
 
Base on the architecture of Reflux, there is some target folders: `actions` `store` `view` which are Reflux actions, store and views. So please put your code file to these folders, when you create new Reflux module. `component` folder keeps all our Reflux components.

And base on business requirement, we have `chart` `dashboard` `ufadmin` folders, `chart` is all chart render component, `dashboard` is all dashboard component, `ufadmin` is all Manage System page functionality.  

## Program Entry Point
Rhizome.js is the javascript entry point. rhizome/templates/base.html includes the vendor.js and main.js. The vendor.js is for all script package javascript, the main.js is for all source javascript. There are some major page javascript classes: `Explorer` `Dashboard` `DataEntry` `SourceData` `UserAccount` `Dashboards` `HomepageCharts` `DashboardBuilder` `UFAdmin` in Rhizome.js

The server side page routing rule is defined in rhizome/urls.py, So the default empty site root address is routed to homepage.html, homepage.html call Rhizome.HomepageCharts, then the homepage is rendered. Other pages are similar as the homepage. 

The server side rhizome/urls.py define the routing rule, every html page define the DOM container element, and then call Rhizome target page class to render the whole page.

## Dashboard
There is two kinds dashboard, one is the built-in dashboard, one is the custom dashboard. Built-in dashboards are shown in 4 places:

#### Built in Dashboard
1. The Homepage, Indicators are defined in: webapp/dashboard/builtin/homepage-afghanistan.js homepage-nigeria.js homepage-pakistan.js
2. Management dashboard url: /datapoints/management-dashboard/ Indicators are defined in webapp/dashboard/builtin/management.js
3. District dashboard url: /datapoints/district-dashboard/ Indicators are defined in webapp/dashboard/builtin/district.js
4. NGA campaign monitoring url: /datapoints/nga-campaign-monitoring/ Indicators are defined in webapp/dashboard/builtin/nco.js

#### Custom Dashboard
The custom dashboard is created by a user, click the url /datapoints/dashboards/create and select a layout, a new custom dashboard will be created, and you can list it in /datapoints/dashboards/ and display a custom dashboard. The code at webapp/src/view/dashboard-builder, and custom dashbaord is rendered by webapp/src/dashboard/CustomDashboard.jsx component.

## DataExplorer
When you create a dashboard, you need to add a chart to the dashboard. the DataExplorer will help you to add a chart to your created custom dashboard. The DataExplorer code is at the webapp/src/view/data-explorer/ the DataExplorer.js defines the whole page UI, you can add the chart settings and actions in this component.

DataExplorer options folder (/webapp/src/view/data-explorer/options) defines all chart options, you can change or define every different chart options as you want.


## UfAdmin
UfAdmin is our Manage System functionality, the code is in webapp/src/ufadmin The webapp/src/ufadmin/index.js is the entry point, and we use client React-Router to link these pages. AdminPage.js is the whole abstract page component, all UfAdmin pages inherit from it. 

## Data Entry
Data entry form gives the user direct access to entry the data that the system reports on. Url: /datapoints/entry/  Code: webapp/src/view/entry-form

## Source Data
The source data page is to upload and manage data source from csv files. This part of the functionality will help a user to manage uploaded data source: validate data, map the location, campaign and indicator, and view the results of the upload. Url: /datapoints/source-data/ Code: webapp/src/dashboard/sd/

## Data Browser
The data browser page is to browse system raw data. you can view the raw data from data browser page. Url: /datapoints/data_browser/ Code: webapp/src/view/Explorer.jsx