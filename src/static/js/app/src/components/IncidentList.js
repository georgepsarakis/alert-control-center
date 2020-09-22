import React from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import { apiClient } from '../util/ApiClient';


class IncidentList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            incidents: [],
            ready: false
        }
    }

    componentDidMount() {
        apiClient().get('/incidents').then((response) => {
            this.setState({
                incidents: response.data,
                ready: true
            })
        });
    }

    render() {
        if (!this.state.ready) {
            return (<div>Loading ...</div>)
        }

        return (
            <div>
                <Paper>
                    <Table size="small" classes={{ padding: 'dense' }}>
                        <TableHead>
                            <TableRow>
                                <TableCell>Title</TableCell>
                                <TableCell>Alert Group</TableCell>
                                <TableCell>Created</TableCell>
                                <TableCell>Updated</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            { this.state.incidents.map((incident) => (
                                <TableRow key={incident.id}>
                                    <TableCell>{incident.title}</TableCell>
                                    <TableCell>{incident.alert_group}</TableCell>
                                    <TableCell>{incident.created_at}</TableCell>
                                    <TableCell>{incident.updated_at}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Paper>
                <Button variant="contained" color="primary">
                    Add
                </Button>
            </div>
        );
    }
}

export default IncidentList;
