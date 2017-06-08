'use strict';
const express        = require('express');
const Promise        = require("bluebird");
const bodyParser     = require('body-parser');
const helmet         = require('helmet');
const sessions       = require('client-sessions');
const bcrypt         = require('bcryptjs');
const cookieParser   = require('cookie-parser');
const morgan         = require('morgan');
const flash          = require('connect-flash');
const csrf           = require('csurf');
const csrfProtection = csrf({ cookie: true });
const app            = express();
const multer         = require('multer');
const mongoose       = require('mongoose');
mongoose.Promise     = Promise;

const User           = require('./model');

let config
if(app.get('env') === 'development') {
  console.log('you are running in dev mode');
  config = require('./config').dev;
  mongoose.connect('mongodb://localhost/ondiversity?socketTimeoutMS=300000');
}
else {
  console.log('production')
  config = require('./config').production;
  mongoose.connect(`mongodb:${config.db.user}:${config.db.pass}//@localhost/ondiversity?socketTimeoutMS=300000`);
}


app.use(helmet());
app.set('view engine', 'jade');
app.use(cookieParser());
app.use(sessions({
    cookieName:'session',
    secret: config.sessionSecret,
    duration: 30 * 60 * 10000,
    activeDuration: 5 * 60 * 1000,
    httpOnly: true, // don't let browser JS access cookie ever
    secure: true, // only use cookies over https
    ephemeral: true // delete this cookie when the browser is closed
}));
app.use(flash());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:false}));
app.set('views', __dirname + '/views');
app.use('/public', express.static(__dirname + '/public'));
app.use('/data', express.static(__dirname + '/data'));
app.use('/dropzone', express.static(__dirname + '/node_modules/dropzone/dist'));
app.use(morgan('dev'));

app.use(function(req, res, next) {
  if (req.session && req.session.user) {
    User.findOne({ username: req.session.user.username }, function(err, user) {
      if (user) {
        req.user = user;
        delete req.user.password; // delete the password from the session
        req.session.user = user;  //refresh the session value
        res.locals.user = user;
      }
      next(); // finishing processing the middleware and run the route
    });
  } else {
    next();
  }
});


// middlewares
const middleware = require('./middleware');
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, __dirname + '/data')
  },
  filename: function (req, file, cb) {
    cb(null, `${req.user._id}_input.csv`)
  }
})
const upload = multer({storage: storage})

// routes
const controller = require('./controller');
app.get('/', controller.getIndex)
app.post('/login', controller.postLogin)
app.post('/register', controller.postRegister)
app.get('/input', middleware.requireLogin, controller.getInput)
app.post('/input', middleware.requireLogin, upload.single('file'), controller.postInput) 
app.post('/calculation', middleware.requireLogin, controller.postCalculation)
app.get('/output', middleware.requireLogin, controller.getOutput);
app.get('/logout', controller.getLogout)
app.get('/download', middleware.requireLogin, controller.download);


// error
app.use(function(req, res,next){
  res.send('404!')
});

app.listen(8000, function(req, res){
    console.log('listening on port 8000');
});
