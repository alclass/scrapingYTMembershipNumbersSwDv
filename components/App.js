/*
https://github.com/codingforentrepreneurs/Try-Reactjs.git

  "dependencies": {
    "react": "^16.4.1",
    "react-dom": "^16.4.1",
    "react-dropzone": "^4.2.12",
    "react-image-crop": "^4.0.1",
    "react-markdown": "^3.3.3",
    "react-router": "^4.3.1",
    "react-router-dom": "^4.3.1",
    "react-youtube": "^7.6.0",
    "whatwg-fetch": "^2.0.4"
  },
  "devDependencies": {
    "react-scripts": "1.1.4"
  },
*/

import React, { Component } from 'react'
// import PostSorting from './src/posts/PostSorting'
import './src/App.css'

import ImgDropAndCrop from './src/learn/ImgDropAndCrop'

class App extends Component {
  render () {
    return (
      <div className='App'>
        <ImgDropAndCrop />
      </div>
    )
  }
}

export default App
