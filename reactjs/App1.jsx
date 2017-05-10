import React from "react"
import { render } from "react-dom"

class App1 extends React.Component {
	render() {
		return (
			<div className="container">
				Hello there...!!
				<img src="/static/images/df.jpg" style={{maxHeight:'50%',width:'100%',maxWidth:'400px',margin:'auto'}} className="img-responsive"></img>
				<img src="/static/images/giphy.gif" style={{maxHeight:'50%',width:'100%',maxWidth:'400px',margin:'auto'}} className="img-responsive"></img>
			</div>
		)
	}
}

render(<App1/>, document.getElementById('App1'))