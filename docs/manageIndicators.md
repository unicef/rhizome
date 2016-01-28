# Manage Indicators

## React-Json
This project used a npm dependency named 'react-json' to generate and manage the forms for managing indicators.

Since this package is not updated in npm any more, so we download the latest version from [gitHub](https://github.com/arqex/react-json).

Then we put the source code of this package in `/rhizome/external` folder and import it in `package.json` as below:

```
"dependencies": {
  "react-json": "file:../external/react-json",
}
```

You can check the source code of `react-json` there. And if you are not sure with how to use `react-json`, you can follow the [example](http://codepen.io/arqex/pen/rVWYgo?editors=001) `react-json` provided in gitHub.

The entry of `react-json` is `/external/react-json/Json.js`.

### Input Types

`react-json` provided several input types defined in `/external/react-json/src/types`:
* ArrayField
* BooleanField
* NullField
* NumberField
* ObjectField
* PasswordField
* SelectField
* StringField
* TextField

In this project, we used two input types of `react-json` in `manage indicators`: **string** and **select**. These types are used in `SimpleFormStore.js`:

```
var form_settings = {
  'indicator_tag': {
    'form': true,
    fields: {'tag_name': {type: 'string'}}
  },
  'indicator': {
    'form': true,
    fields: {
      'name': {type: 'string'},
      'short_name': {type: 'string'},
      'source_name': {type: 'string'},
      'low_bound': {type: 'string'},
      'high_bound': {type: 'string'},
      'data_format': {
        type: 'select',
        settings: {options: [
          { value: 'pct', label: 'pct' },
          { value: 'bool', label: 'bool' },
          { value: 'int', label: 'int' }
        ]}
      },
      'description': {type: 'string'}
    }
  }
}
```
### Error Message

We have a requirement about displaying error message when creating new indicator.

Since `react-json` do not have a reliable data validation method, we modified the source code of `react-json` to show the error message.

The steps for showing error message:

1. Add a validation method called `validateData` in `SimpleForm.js`.

```
validateData: function (data) {
  var indicators = this.state.store.indicators
  var errorMessage = {}
  ...
  return errorMessage
},
onSubmit: function (e) {
  ...
  let errorMessage = this.validateData(data)

  _.isEmpty(errorMessage)
    ? SimpleFormActions.baseFormSave(this.props.params.id, this.props.params.contentType, data)
    : this.setState({
      errorMessage: errorMessage,
      formData: data
    })
},
```

2. Create a new state `errorMessage` and use it to transfer the validation result.

```
<ReactJson value={formData} settings={formSettings} errorMessage={this.state.errorMessage} ref='form_data'/>
```

3. Modify the source code of `react-json` to show the error message.

```
//Json.js
render: function () {
  var errorMessage = this.props.errorMessage || {}
  var settings = this.props.settings || {},
    ob = React.createElement(TypeField, {
      type: 'object',
      value: this.state.value,
      errorMessage: errorMessage,
      settings: objectAssign({}, this.state.defaults.object, {
        fields: settings.fields,
        editing: this.getFormSetting(settings, 'editing', 'always'),
        fixedFields: this.getFormSetting(settings, 'fixedFields', true),
        adder: this.getFormSetting(settings, 'adder', false),
        hiddenFields: settings.hiddenFields,
        header: false,
        order: settings.order
      }),
      ref: 'value',
      defaults: this.state.defaults,
      id: this.state.id
    }),
    className = 'jsonEditor' + flexboxClass
    ;

  return React.DOM.div({className: className}, ob);
},
```

```
//TypeField.js
render: function () {
  var Component = this.getComponent(),
    settings = objectAssign(
      {},
      this.context.typeDefaults[this.props.type],
      this.props.settings
    )
    ;

  this.addDeepSettings(settings);

  return React.createElement(Component, {
    value: this.props.value,
    errorMessage: this.props.errorMessage,
    settings: settings,
    onUpdated: this.props.onUpdated,
    id: this.props.id,
    ref: 'field'
  });
},
```

```
//Filed.js
render: function(){
  var definition = this.props.definition || {},
    errorMessage = this.props.errorMessage || '',

  ...

  if(errorMessage.length > 0){
    className += ' jsonError';
    error = React.DOM.span({ key:'e', className: 'jsonErrorMsg' }, errorMessage );
  }

  ...

  return React.DOM.div({className: className}, [
    React.DOM.span( {className: 'jsonName', key: 'n'}, jsonName ),
    React.DOM.span( {className: 'jsonValue', key: 'v'}, typeField ),
    error
  ]);
},
```
