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

The entry of `react-json` is `/external/react-json/json.js`.

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


