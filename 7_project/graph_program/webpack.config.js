const path = require('path');

module.exports = {
  mode: 'development',
  entry: './renderer.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  target: 'electron-renderer',
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'], // CSS 처리
      },
    ],
  },
  devtool: 'source-map',
};
