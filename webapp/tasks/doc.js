import gulp from 'gulp'
import markdown from 'gulp-markdown-docs'

const TASK_NAME = 'doc'

function docOnce (fileConf) {
   return gulp.src(fileConf.src)
        .pipe(markdown('index.html', {documentSort: 'rank'}))
        .pipe(gulp.dest(fileConf.dist));
}

function doc () {
  return gulp.autoRegister(TASK_NAME, docOnce, (config) => {
  })
}

gulp.task(TASK_NAME, doc)

export default doc
