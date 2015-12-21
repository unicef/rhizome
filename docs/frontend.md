#Front-end Documentation

##Environment

Node: >= 0.10, suggested 0.12. Don't use Node 4.0.

Npm: >= 2.0. Feature of installing local dependency is needed.

Working direction: `/webapp`

##Code Principle
###standard

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

###General Rules

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


##Test

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

##React/Reflux

**Avoid sending API request in store.init()**

Reflux store.init() will be called when store is initialized. Put API request in store.init() will send request when a page is launched no matter whether it is necessary and worsen the performance.

It's better to send API request via a Reflux action.

**Avoid binding store directly on state**

Binding store directly on state is easily overriden therefore not stable. It's better to bind onto a property of state.

Use

`mixins: [Reflux.connect(ChartWizardStore, 'data')]`

instead of

`mixins: [Reflux.connect(DataStore)]`

**Write React in ES6+**

Writing React in ES6/ES7 is not compulsory but highly recommended. Read this [guide](http://babeljs.io/blog/2015/06/07/react-on-es6-plus/) in babeljs.org.
