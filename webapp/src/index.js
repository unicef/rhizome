require('./utilities/polyfill.js')

if ('ActiveXObject' in window) {
  var body = document.getElementsByTagName('body')[0]
  body.classList.add('ie')
}

window.Rhizome = require('./Rhizome')
