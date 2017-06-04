const child_process = require('child_process');
const mongoose = require('mongoose');
const User = mongoose.model('user');
const fs = require('fs');
const Promise = require('bluebird');

const flashAndRedirect = (req,res,message,uri="/") => {
    req.flash('message', message);
    res.redirect(uri);
}

function readFirstLine (path) {
  return new Promise(function (resolve, reject) {
    var rs = fs.createReadStream(path, {encoding: 'utf8'});
    var acc = '';
    var pos = 0;
    var index;
    rs
      .on('data', function (chunk) {
        index = chunk.indexOf('\n');
        acc += chunk;
        index !== -1 ? rs.close() : pos += chunk.length;
      })
      .on('close', function () {
        resolve(acc.slice(0, pos + index));
      })
      .on('error', function (err) {
        reject(err);
      })
  });
}

/**
 * POST method, handling upload csv file and spawn python calculation script
 * @param  {[type]}   req  [description]
 * @param  {[type]}   res  [description]
 * @param  {Function} next [description]
 * @return {[type]}        [description]
 */
exports.postInput = (req,res,next) => {
    if(req.file && req.user){
        readFirstLine(__dirname + `/data/${req.user._id}_input.csv`)
            .then(line => {
                res.send(line.replace(/\r?\n|\r/g, '').split(','));
            })
    }
    else{flashAndRedirect(req,res,'error')}
};

exports.postCalculation = (req,res,next) => {
    const file_name = __dirname + `/data/${req.user._id}_input.csv`;
    const cr = JSON.parse(req.body.order);
    let GroupName = JSON.parse(req.body.groupNames);
    // const GroupName = ['Section', 'Study Group'];
    let NumofGroup = [];
    JSON.parse(req.body.groupNums).forEach(item => {
        NumofGroup.push(Number(item));
    });
    console.log(req.body)
    if (GroupName.length === 0 || GroupName[0] === "") {
        GroupName = ['Section', 'Study Group'];
        NumofGroup = [3,15];
    }
    GroupName = ['Main Group', 'Sub Group'];
    // const NumofGroup = [3,15];
    let divProcess = child_process.spawn('python3', [__dirname + '/../python_note/run.py', file_name, cr, GroupName, NumofGroup, req.user._id]);
    divProcess.stdout.on('data', (data) => {
        console.log('stdout: ' + data);
    });
    divProcess.stderr.on('data', (data) => {
        console.log('stderr: ' + data);
    });
    divProcess.on('close', (code)=> {
        console.log('close');
        res.send('done')
    });
}

/**
 * [description]
 * @param  {[type]}   req  [description]
 * @param  {[type]}   res  [description]
 * @param  {Function} next [description]
 * @return {[type]}        [description]
 */
exports.getIndex = (req,res,next) => {
    res.render('index', {message: req.flash('message')});
};

exports.postLogin = (req,res,next) => {
    User.findOne({username: req.body.username})
        .then(user => {
            if(!user){flashAndRedirect(req,res,'User Not Found')}
            else if(user.validPassword(req.body.password)){
                req.session.user = user;
                res.redirect('/input');
            }
            else {flashAndRedirect(req,res,'Incorrect Password')}
        })
        .catch(err => {
            console.log(err)
            flashAndRedirect(req,res,'Error')
        });
};

exports.postRegister = (req,res,next) => {
    User.findOne({username: req.body.username})
        .then(user => {
            if(user){flashAndRedirect(req,res,'username already taken')}
            else{
                const newUser = new User();
                newUser.username = req.body.username;
                newUser.password = newUser.generateHash(req.body.password);
                return newUser.save();
            }
        })
        .then(user => {
            req.session.user = user;
            req.flash('message', 'Register successfully');
            res.redirect('/input');
        })
        .catch(err => {flashAndRedirect(req,res,'Error')});
};
exports.getLogout = (req,res,next) => {
    req.session.reset();
    flashAndRedirect(req,res,'You have successfully logout');
};

exports.getInput = (req,res,next) => {
    res.render('input', {message: req.flash('message')});
}

exports.getOutput = (req,res,next) => {
    const outputPath = `/data/${req.user._id}_output.csv`;
    if (fs.existsSync(__dirname + outputPath)){
        // console.log('outpu')
        res.render('output', {message: req.flash('message')});    
    }
    else{flashAndRedirect(req,res,'Error');}    
}

exports.download = (req,res,next) => {
    const file = __dirname + `/data/${req.user._id}_output.csv`;
    res.download(file); // Set disposition and send it.
}