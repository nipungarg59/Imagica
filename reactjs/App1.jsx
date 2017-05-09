import React from "react"
import { render } from "react-dom"

class App1 extends React.Component {
	render() {
		return (
			<div>
				Hello there...!!
			</div>
		)
	}
}

render(<App1/>, document.getElementById('App1'))