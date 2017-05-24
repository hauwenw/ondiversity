exports.requireLogin = (req,res,next) => {
    if(!req.user){
        req.flash('message', 'Please Login First');
        res.redirect('/');
    }
    else{
        next();
    }
}