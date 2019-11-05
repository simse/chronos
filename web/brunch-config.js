exports.files = {
    stylesheets: {joinTo: 'app.css'},
    javascripts: {joinTo: 'app.js'}
};

exports.plugins = {
    postcss: {processors: [require('autoprefixer')]}
};
