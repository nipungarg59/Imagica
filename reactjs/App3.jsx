import React from "react"
import { render } from "react-dom"
import axios from 'axios';

class App3 extends React.Component {

	constructor(props)
	{
		super(props);
		this.state= {
			similarity : '',
			phrase_1 : '',
			phrase_2 : '',
			loaderclass : {'display':'none'}
		}
		this.onClickSubmit = this.onClickSubmit.bind(this);
		this.handlePhrase1Change = this.handlePhrase1Change.bind(this);
		this.handlePhrase2Change = this.handlePhrase2Change.bind(this);
	}

	handlePhrase1Change(evt)
	{
		console.log(evt.target.value)
		this.setState({phrase_1 : evt.target.value})
	}

	handlePhrase2Change(evt)
	{
		console.log(evt.target.value)
		this.setState({phrase_2 : evt.target.value})
	}

	onClickSubmit()
	{
		this.setState({loaderclass: {}, similarity : ''})
		fetch('/get/analysis', {
			method: "POST",
			body: JSON.stringify({ ...this.state}),
			headers: {
			"Content-Type": "application/json"
			},
		}).then(res => res.json()).then(res => {
			this.setState({similarity : res, loaderclass: {'display':'none'}})
		})
	}

	render() {
		return (
			<div className="container">
				<div style={{'top':'0', textAlign:"right", 'marginTop':'10px'}}>
					<span style={{'cursor':'pointer','backgroundColor':'rgba(44,44,44,0.7)', 'color':'white', 'fontSize':'24px', 'padding': '18px'}}><a style={{'color':'white'}} href="/semantic/similarity">Home</a></span>
				</div>
				<div className="container" style={{textAlign:"center"}}>
					<h1>About Us</h1>
					<br/>
				</div>

				<div className="container" style={{textAlign:"center"}}>
					
				</div>
				
				<br/>
				<div style={{textAlign:"center"}}>
					<img src="https://loading.io/spinners/typing/lg.-text-entering-comment-loader.gif" style={this.state.loaderclass}/>
				</div>

				<div className="container" style={{'backgroundColor':'rgb(236, 239, 241)', 'paddingTop':'50px'}}>
					<div className="col-sm-4" style={{textAlign:"center"}}>
						<img src="https://scontent-bom1-1.xx.fbcdn.net/v/t1.0-9/12651334_1674915142791264_9202626119017210772_n.jpg?oh=c1e05219a8af5b2e894c4aea56c5c370&oe=5ABA5543" style={{'width':'250px', 'height': '250px'}}/>
						<div style={{textAlign:"center", 'color' : 'rgb(51, 51, 51)', 'fontWeight':'500'}}><h4>Hardik Gulati</h4></div>
					</div>
					<div className="col-sm-4" style={{textAlign:"center"}}>
						<img src="http://api.staging.icofarm.net/images/team_icofarm/c9452bae22c5553a42f38db4d36e14f8DSC07905.jpg" style={{'width':'250px', 'height': '250px'}}/>
						<div style={{textAlign:"center", 'color' : 'rgb(51, 51, 51)', 'fontWeight':'500'}}><h4>Nipun Garg</h4></div>
					</div>
					<div className="col-sm-4" style={{textAlign:"center"}}>
						<iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fphoto.php%3Ffbid%3D1694207460850848%26set%3Da.1443269059278024.1073741826.100007848317099%26type%3D3&width=500" width="500" height="608" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowTransparency="true" style={{'width':'250px', 'height': '250px'}}></iframe>
						<div style={{textAlign:"center", 'color' : 'rgb(51, 51, 51)', 'fontWeight':'500'}}><h4>Priyanshu Sinha</h4></div>
					</div>
				</div>
				
				<hr/>
			</div>
		)
	}
}

render(<App3/>, document.getElementById('App3'))