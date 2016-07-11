export default {
  standard: {
    credits: { enabled: false },
    chart: {
      spacingBottom: 20,
      style: {
        fontFamily: "'proxima', 'Helvetica', sans-serif' ",
        paddingTop: '20px'  // Make room for buttons
      }
    },
    exporting: {
      buttons: {
        contextButton: {
          onclick: function () {
            this.exportChart({type: 'jpeg'})
          },
          symbol: null,
          text: 'Export',
          x: -20,
          y: -30,
          theme: {
            style: {
              color: '#039',
              textDecoration: 'underline'
            }
          }
        }
      }
    },
    title: ''
  }
}
