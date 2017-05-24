'use strict';

const bcrypt = require('bcryptjs');
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const userSchema = new Schema({
    username: {type: String, required: true},
    password: {type: String, required: true}
});

// instance methods ======================
userSchema.methods = {
    // encript
    generateHash: function(password) {
        return bcrypt.hashSync(password, bcrypt.genSaltSync(10));
    },
    // check pw
    validPassword: function(password) {
        return bcrypt.compareSync(password, this.password);
    }
}

const User = mongoose.model('user', userSchema);

User.on('index', function(err) {
    if (err) {
        console.error('User index error: %s', err);
    } else {
        console.info('User indexing complete');
    }
});
module.exports = User;
