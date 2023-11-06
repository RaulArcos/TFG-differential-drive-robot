const devMode = (process.env.NODE_ENV === 'development');

export default {
  input: './src/websockets.js',
  output: {
    file: './robotuca-client.js',
    format: 'es',
    inlineDynamicImports: false,
    sourcemap: devMode ? 'inline' : false
  }
};