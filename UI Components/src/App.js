import React from 'react';
import logo from './logo.svg';
import woman from './SomePicture.jpg'
import glogo from './New_Logo.jpg';
//import wlogo from './wayne_rooney.jpg';
import wlogo from './200.gif';
import './App.css';
import './index.css';
import Collapse from 'react-bootstrap/Collapse'
import SearchBar from 'material-ui-search-bar'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { Fab } from '@material-ui/core';
import PublishIcon from '@material-ui/icons/Publish';
import axios from 'axios';
import FormData from 'form-data'
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Switch from '@material-ui/core/Switch';



function Homebtn() {
  return (
      <a className="nav-link" href="#" style={{color: "white"}} onClick={() => window.location.reload()}>Home</a>
  );
}

function Aboutbtn() {
  return (
      <a className="nav-link" href="https://github.com/GovindBhala/InfoViz_ImageLabelling#infoviz_imagelabelling" style={{color: "white"}} onClick={() => window.location.reload()}>About</a>
  );
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

class PhotoGrid extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchResult: null
    };
  }

  componentDidUpdate(prevProps){
    if(this.props.dataFromParent !== prevProps.dataFromParent){
      this.setState({searchResult: this.props.dataFromParent}, () => {
        console.log(this.state.searchResult);  
      });
    }
  }  

  render() {
    const paper = {
      height: "100%",
      width: "100%",
      margin: 0,
      padding: 0
    }
    const gridDim = {
      width: "100%",
      height: "30%",
      margin: 0,
    }
    const gridDimMed = {
      width: "100%",
      height: "100%",
      margin: 0,
    }
    const gridDimInner = {
      width: "30%",
      height: "100%",
      padding: 5
    }
    const imgDim = {
      height: "100%",
      width: "100%",
      
      margin: 0,
    }
    const searchStyle = {
      margin:0,
      transform:"translate(-50%, -50%)",
      position:"absolute",
      top:"50%",    
      left:"50%",
    }
    return(
        this.state.searchResult==null?
        <React.Fragment>
          <Button variant="" disabled style={searchStyle}>
    <Spinner
      variant="primary"
      as="span"
      animation="border"
      size="md"
      role="status"
      aria-hidden="true"
    />
     <br/>Loading...
  </Button> 
            </React.Fragment>:<React.Fragment>
        <Grid item xs={12} style={gridDim}>
          <Grid container justify="center" spacing={6} style={gridDimMed}>
            {(this.state.searchResult?this.state.searchResult.slice(0,3):[{caption: 0, path: null},{caption: 1, path: null},{caption: 2, path: null}]).map((value, index) => (
              <Grid key={index} item style={gridDimInner}>
                <Paper style={paper}>
                  <img src={value.path ? value.path : wlogo} style={imgDim} alt={value.caption} title={value.caption}/>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Grid>
        <Grid item xs={12} style={gridDim}>
          <Grid container justify="center" spacing={6} style={gridDimMed}>
          {(this.state.searchResult?this.state.searchResult.slice(3,6):[{caption: 3, path: null},{caption: 4, path: null},{caption: 5, path: null}]).map((value, index) => (
              <Grid key={index} item style={gridDimInner}>
                <Paper style={paper}>
                  <img src={value.path ? value.path: wlogo} style={imgDim} alt={value.caption} title={value.caption}/>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Grid>
        <Grid item xs={12} style={gridDim}>
          <Grid container justify="center" spacing={6} style={gridDimMed}>
          {(this.state.searchResult?this.state.searchResult.slice(6,9):[{caption: 6, path: null},{caption: 7, path: null},{caption: 8, path: null}]).map((value, index) => (
              <Grid key={index} item style={gridDimInner}>
                <Paper style={paper}>
                  <img src={value.path ? value.path : wlogo} style={imgDim} alt={value.caption} title={value.caption}/>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Grid>
      </React.Fragment>
    );
  }
}

class FullScreen extends React.Component {
  state = {searchBarState: false, capImageState: false, caption: null, imagePath: null, searchQuery: null};
  callbackFunction = (childData) => {
    this.setState({searchBarState: childData.searchBarState, searchQuery: childData.searchQuery})
  }
  fabCallbackFunction = (childData) => {
    this.setState({capImageState: childData.capImg, caption: childData.cap, imagePath: childData.imgPath, searchBarState: childData.searchBarState})
  }
  searchBarCallbackFunction = (childData) => {
    this.setState({searchQuery: childData.searchQuery}, () => {
    })
  }
  render(){
    const alignFS = {
      width: '100%',
      height: '100%',
    }
    return (
        <div style={alignFS}>
          <CustomSearchBar parentCallback = {this.searchBarCallbackFunction} dataFromParent = {{searchBarState : this.state.searchBarState, searchQuery: this.state.searchQuery}}/>
          <Toggle parentCallback = {this.callbackFunction} dataFromParent = {{capImg: this.state.capImageState, cap: this.state.caption, imgPath: this.state.imagePath, searchQuery: this.state.searchQuery}} />
          <UploadFAB parentCallback = {this.fabCallbackFunction}/>
        </div>
    );
  }
}

class Toggle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchCardOpen: true,
      gridCardOpen: false,
      capImgOpen: false,
      caption: null,
      imagePath: null,
      searchQuery: null,
      searchResult: null,
      firstModel: true
    };
  }
  sendData = () => {
    console.log(this.state);
    this.props.parentCallback({searchBarState: this.state.gridCardOpen, searchQuery: this.state.searchQuery});
  }



  fetchResult = () => {
    console.log(this.state.searchQuery);
    
    var qs = this.state.searchQuery.split(" ");
    var str = '';
    for(var i = 0; i< qs.length-1; i++){
      str += qs[i] + '%20'
    }
    if(qs.length>1){
      str+= qs[qs.length-1];
    }
    // var that = this;
    console.log(str)
    this.setState({searchResult:null});
    // this.state.searchResult=null;
    axios({
      method: 'get',
      url: 'http://localhost:5010/get-search-result?query='+str,
      })
      .then((response) => {
          console.log(response);
          this.setState({searchResult: response.data})
          
      })
      .catch(function (response) {
          console.log(response);
      });
  }

  changeSearchCardState(param) {
    this.setState(param, () => {
      this.sendData();
    });
    this.fetchResult();
  }

  componentDidUpdate(prevProps){
    if((this.props.dataFromParent.cap !== prevProps.dataFromParent.cap) || (this.props.dataFromParent.imgPath !== prevProps.dataFromParent.imgPath)){
      this.setState({searchCardOpen: false, gridCardOpen: false, capImgOpen: this.props.dataFromParent.capImg, caption: this.props.dataFromParent.cap, imagePath: this.props.dataFromParent.imgPath});  
    }
    if(this.props.dataFromParent.searchQuery !== prevProps.dataFromParent.searchQuery){
      console.log(this.props.dataFromParent.searchQuery);
      this.setState({searchQuery: this.props.dataFromParent.searchQuery}, () => {
          console.log(this.state.searchQuery)
          this.fetchResult();
      });
    }
  }

  sendData = () => {
    if(this.state.searchQuery){
      this.props.parentCallback({searchBarState: this.state.gridCardOpen, searchQuery: this.state.searchQuery});
    }
  }
  
  handleChange = event => {
    this.setState({searchQuery: event.target.value}, () => {
    });
  }

  render() {
    const searchbaralign = {
      left: "5%",
      width: "90%",
    };
    const captionStyle = {
      fontSize: "25px", 
      fontStyle: "italic", 
      textAlign: "center",
      paddingBottom: "10px"
    }
    const captionDivImgSize = {
      height: "85%",
      width: "100%",
      padding: "5px",
    }
    const cardStyling = {
      height:"75%", 
      width:"70%",
    }
    const captionImgSize = {
      maxHeight: "100%",
      width: "100%",
      display: "block",
      marginLeft: "auto",
      marginRight: "auto",
    }
    
    return (
      <div id="card-class" className="card" style={cardStyling}>
        <Collapse in={this.state.searchCardOpen} className="collapse-search-bar">
        <div>
          <img className="search-bar-img" src={glogo} alt="logo"/>
            <div className="input-group" style={searchbaralign}>
                <input type="text" className="form-control search-form" placeholder="Search" value={this.state.searchQuery?this.state.searchQuery: ""} onChange={this.handleChange}/>
                <span className="input-group-btn">
                  <button type="submit" className="btn btn-dark search-btn" data-target="#search-form" disabled={!this.state.searchQuery} name="q" onClick={() => this.changeSearchCardState({searchCardOpen:false, gridCardOpen:true})}>
                    <i className="fa fa-search"></i>
                  </button>
                </span>
            </div>
        </div>
        </Collapse>
        <div style={{paddingBottom: "25px"}}></div>
        <Collapse in={this.state.gridCardOpen} style={{maxHeight: "100%"}}>
          <div>
            <PhotoGrid dataFromParent={this.state.searchResult}/>
          </div>
        </Collapse>
        <Collapse in={this.state.capImgOpen} style={{maxHeight: "100%"}}>
          <div style={{width: "100%", height:"100%"}}>
            <div id="captionId" style={captionStyle}>{this.state.caption}</div>
            <div style={captionDivImgSize}>
              <img src={this.state.imagePath ? require('./'+`${this.state.imagePath}`): wlogo} alt={this.state.caption} style={captionImgSize}/>
            </div>
          </div>
        </Collapse>
        
      </div>
    );
  }
}
class CustomSearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchBarOpen: false,
      searchQuery: "",
    };
  }

  componentDidUpdate(prevProps){
    if(this.props.dataFromParent !== prevProps.dataFromParent){
      this.setState({searchBarOpen: this.props.dataFromParent.searchBarState, searchQuery: this.props.dataFromParent.searchQuery});  
    }
  }

  sendData = () => {
    this.state.searchResult = null
    this.props.parentCallback({searchQuery: this.state.searchQuery});
  }

  handleChange = event => {
    this.setState({searchQuery: event, value: event}, () => {
    });
  }

  changeSearchBarState(param) {
    this.setState(param);
  }
  render() {
      const barAlign = {
        width: "100%",
        height: "10%",
        paddingTop: "10px",
      };
      return (
        <div style={barAlign}>
          <Collapse in={this.state.searchBarOpen}>
            <div className="holder">
              <MuiThemeProvider>
                <SearchBar
                  type={"text"}
                  value={this.state.searchQuery? this.state.searchQuery: ""}
                  onChange={this.handleChange}
                  onRequestSearch= {this.sendData}
                  style={{
                    margin: '0 auto',
                    maxWidth: '65%',
                    maxHeight: '80%', 
                  }}
                />
              </MuiThemeProvider>
            </div>
          </Collapse>
        </div>
      )
  }
}

class UploadFAB extends React.Component {
  constructor() {
    super();
    this.state = {
      selectedFile: null,
      caption: null,
      imagePath: null,
      toggle: false
    };
  }

  sendData = () => {
    console.log({capImg: true, cap: this.state.caption, imgPath: this.state.imagePath})
    this.props.parentCallback({capImg: true, cap: this.state.caption, imgPath: this.state.selectedFile.name, searchBarState: false});
  }

  setFileName(param){
    this.setState(param, () => {
      console.log(this.state.selectedFile);
      this.onFileUpload();
    });
  }

  onFileChange = event => {
    this.setFileName({selectedFile: event.target.files[0]});
  };

  componentDidUpdate(prevProps, prevState) {
    if(this.state.caption !== prevState.caption || this.state.imagePath !== prevState.imagePath){
      this.sendData();
    }
  }
  

  onFileUpload = () => {
    const formData = new FormData();
    console.log(this.state.selectedFile);
    let model = 'gru'
    if(this.state.toggle==true){
      model = 'lstm'
    }
    console.log(this.state.toggle)
    // let model = this.state.toggle?'lstm':'gru'; 
    formData.append('Image', this.state.selectedFile, this.state.selectedFile.name);
    axios({
      method: 'post',
      url: 'http://localhost:5000/upload-image?model='+model,
      data: formData,
      headers: {'Content-Type': 'multipart/form-data' }
      })
      .then((response) => {
          console.log(response);
          this.setState({caption: response.data.prediction, imagePath: response.data.image_path}, () => {
          });
          
      })
      .catch(function (response) {
          console.log(response);
      });
  }

  switchChanged = event => {
   if(event.target.checked){
    this.setState({toggle:true}, () => {
      if(this.state.selectedFile!==null){
        this.onFileUpload();
       }
    })
    
   }else{
    this.setState({toggle:false}, () => {
      console.log(this.state.toggle);
      if(this.state.selectedFile!==null){
        this.onFileUpload();
       }
    })
   }
 };

  renderFunc = (prediction,image_path) => {
    this.setState({caption: prediction, imagePath: image_path});
  }

  render() {
    const fabstyle = {
      margin: 0,
      top: 'auto',
      right: 40,
      bottom: 20,
      left: 'auto',
      position: 'fixed',
      backgroundColor: "#000000",
      zIndex: 2,
      outline: "none"
  };
  const captionStyle = {
    fontSize: "25px", 
    fontStyle: "italic", 
    textAlign: "center",
    paddingBottom: "10px"
  }
  const captionDivImgSize = {
    height: "85%",
    width: "100%",
    padding: "5px",
  }
  const cardStyling = {
    height:"75%", 
    width:"70%",
  }
  const captionImgSize = {
    maxHeight: "100%",
    width: "100%",
    display: "block",
    marginLeft: "auto",
    marginRight: "auto",
  }
  const switchStyle = {
    width: "100%", height:"100%", marginTop: "-40%",
    marginLeft: "80%"
  }
    return (
      <div>
        <div in={this.state.capImgOpen} style={{maxHeight: "100%"}}>
          <div style={switchStyle}>
          <Switch
            onChange={this.switchChanged}
            name="changeModel"
            inputProps={{ 'aria-label': 'primary checkbox' }}/>
            <span className="primary">{this.state.toggle ? 'LSTM' : 'GRU'}</span>
          </div>
        </div>
        <div>
        <input id="myInput" type="file" accept="image/*" ref={(ref) => this.myInput = ref} style={{ display: 'none' }} onChange={this.onFileChange} />
        <Fab color="secondary" aria-label="upload" style={fabstyle} onClick={(e) => this.myInput.click()} >
            <PublishIcon />
        </Fab>
        </div>
      </div>
    );
  }
}

export default App;
export {
  Homebtn,
  Aboutbtn,
  FullScreen,
};
