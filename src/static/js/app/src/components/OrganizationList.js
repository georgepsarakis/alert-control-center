import React from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { apiClient } from '../util/ApiClient';


class OrganizationList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            organizations: [],
            ready: false
        }
    }

    componentDidMount() {
        apiClient().get('/organizations').then((response) => {
            this.setState({
                organizations: response.data,
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
                                <TableCell>Name</TableCell>
                                <TableCell>Created</TableCell>
                                <TableCell>Updated</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            { this.state.organizations.map((org) => (
                                <TableRow key={org.name}>
                                    <TableCell>{org.name}</TableCell>
                                    <TableCell>{org.created_at}</TableCell>
                                    <TableCell>{org.updated_at}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Paper>
            </div>
        );
    }
}

export default OrganizationList;
