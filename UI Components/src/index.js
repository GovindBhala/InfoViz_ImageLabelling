import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import {Homebtn, FullScreen, Aboutbtn} from './App';
import * as serviceWorker from './serviceWorker';

// const navStyle = {
//   display: "flex",
//   justifyContent: "center",
//   alignItems: "center",
//   marginRight: "0px"
// }

ReactDOM.render(
  <React.StrictMode>
    <FullScreen />
  </React.StrictMode>,
  document.getElementById('full-screen')
);

ReactDOM.render(

  <React.StrictMode>
    <div id="container row" >
      <Aboutbtn />
    </div>
  </React.StrictMode>,
  document.getElementById('home_link')
)

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
