function _replaceBindMethodForWktToPdf () {
  let replaceFunction = Function
  if (typeof replaceFunction.prototype.bind !== 'function') {
    replaceFunction.prototype.bind = function bind (obj) {
      var args = Array.prototype.slice.call(arguments, 1)
      var self = this
      var Nop = function () { }
      var bound = function () {
        return self.apply(
          this instanceof Nop
            ? this
            : (obj || {}), args.concat(Array.prototype.slice.call(arguments))
        )
      }
      Nop.prototype = this.prototype || {}
      bound.prototype = new Nop()
      return bound
    }
  }
}

global.Promise = global.Promise || require('es6-promise').Promise
global.Object.assign = global.Object.assign || require('object-assign')
global.IsWkhtmlToPdf = global.IsWkhtmlToPdf || (typeof Function.prototype.bind !== 'function')

_replaceBindMethodForWktToPdf()
