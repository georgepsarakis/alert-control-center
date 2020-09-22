import React from 'react';
import { apiClient } from '../util/ApiClient';
import { URL } from '../config/Api';


class IncidentReportForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = { name: '' };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState({ name: event.target.value });
    }

    handleSubmit(event) {
        alert('A name was submitted: ' + this.state.name);
        apiClient(true).post(
            '/incident_reports/',
            { name: this.state.name, alert_group: 2 }
        );
        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <select><option value="2">Test Group 2</option></select>
                <label>
                    Name:
                    <input
                        type="text"
                        value={this.state.name}
                        onChange={this.handleChange} />
                </label>
                <input type="submit" value="Submit" />
            </form>
        );
    }
}

export default IncidentReportForm;