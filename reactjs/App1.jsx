import React from "react"
import { render } from "react-dom"
import axios from 'axios';

class App1 extends React.Component {

	constructor(props)
	{
		super(props);
		this.state= {
			accessKey : '',
		}
		this.onClickGenerateAccessKeyButton = this.onClickGenerateAccessKeyButton.bind(this);
	}
	onClickGenerateAccessKeyButton()
	{
		axios.get('/getKey/')
		.then(function (response){
			console.log(response.data,"onClickGenerateAccessKeyButton");
			if(response.data.error)
			{
				alert(response.data.description);
			}
			else
			{
				this.setState({
					accessKey : response.data.accessKey
				})
			}
		}.bind(this))
	}

	render() {
		return (
			<div className="container">
				<div className="container" style={{textAlign:"center"}}>
					<h1>Image Api Management</h1>
				</div>
				<div className="container" style={{textAlign:"center"}}>
					<button className="btn btn-primary" onClick={this.onClickGenerateAccessKeyButton}>Generate Access Key</button>
					<br/>
					{this.state.accessKey}
					<br/>
					<h5>Details : </h5>
					Url : https://imagicaa.herokuapp.com/getKey/
					<br/>
					Request Type : GET
					<br/>
					Response : Dictionary
				</div>
				<br/>
				<div className="container">
					<div className="col-sm-6">
						<span>&#123;</span>
						<br/>
						<span>&nbsp;&nbsp;&nbsp;&nbsp;error: 'True',</span>
						<br/>
						<span>&nbsp;&nbsp;&nbsp;&nbsp;description: 'Description Of error.'</span>
						<br/>
						<span>&#125;</span>
					</div>
					<div className="col-sm-6">
						<span>&#123;</span>
						<br/>
						<span>&nbsp;&nbsp;&nbsp;&nbsp;error: 'False',</span>
						<br/>
						<span>&nbsp;&nbsp;&nbsp;&nbsp;accessKey: 'accessKey'</span>
						<br/>
						<span>&#125;</span>
					</div>
				</div>
				<br/>
				<hr/>
				<div className="container" style={{textAlign:"center"}}>
					<h3>Get Method</h3>
					<img src="/static/images/df.jpg" style={{maxHeight:'50%',width:'100%',maxWidth:'400px',margin:'auto'}} className="img-responsive"></img>
				</div>

			</div>
		)
	}
}

render(<App1/>, document.getElementById('App1'))