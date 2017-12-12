import React from "react"
import { render } from "react-dom"
import axios from 'axios';

class App2 extends React.Component {

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
				<div className="container" style={{textAlign:"center"}}>
					<h1>Finding Semantic Similarity</h1>
					<br/>
				</div>

				<div className="container" style={{textAlign:"center"}}>
					<div className="form-group">
						<label for="usr">Phrase 1 :</label>
						<input type="text" value={this.state.phrase_1} onChange={this.handlePhrase1Change} className="form-control"/>
					</div>
					<div className="form-group">
						<label for="usr">Phrase 2 :</label>
						<input type="text" value={this.state.phrase_2} onChange={this.handlePhrase2Change} className="form-control"/>
					</div>
				</div>
				<div className="container" style={{textAlign:"center"}}>
					<button className="btn btn-primary" onClick={this.onClickSubmit}>Submit</button>
				</div>
				<br/>
				<div style={{textAlign:"center"}}>
					<img src="https://loading.io/spinners/typing/lg.-text-entering-comment-loader.gif" style={this.state.loaderclass}/>
				</div>
				{this.state.similarity?
					<div className="container" style={{textAlign:"center",}}>
						
						<h3>Tf-Idf :{this.state.similarity['Tf-Idf']}</h3>
						<h3>Indexing :{this.state.similarity['Indexing']}</h3>
						<h3>Distribution-F :{this.state.similarity['Distribution-F']}</h3>
						<h3>Distribution-T :{this.state.similarity['Distribution-T']}</h3>
						<img src={this.state.similarity['image_url']}/>
						<hr/>
					</div>:
					<div/>
				}

			</div>
		)
	}
}

render(<App2/>, document.getElementById('App2'))