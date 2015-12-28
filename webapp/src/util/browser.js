/* global window */

export default {
  isIE: function () {
    return ('ActiveXObject' in window) || IsWebkit
  }
}
