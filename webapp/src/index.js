require('./polyfill/polyfill.js')

if ('ActiveXObject' in window) {
  var body = document.getElementsByTagName('body')[0]
  body.classList.add('ie')
}

window.Polio = require('./PolioScape')
