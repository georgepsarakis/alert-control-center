import React from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { apiClient } from '../util/ApiClient';


class TeamList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            teams: [],
            ready: false
        }
    }

    componentDidMount() {
        apiClient().get('/teams').then((response) => {
            this.setState({
                teams: response.data,
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
                                <TableCell>Organization</TableCell>
                                <TableCell>Created</TableCell>
                                <TableCell>Updated</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            { this.state.teams.map((team) => (
                                <TableRow key={team.name}>
                                    <TableCell>{team.name}</TableCell>
                                    <TableCell>{team.organization_id}</TableCell>
                                    <TableCell>{team.created_at}</TableCell>
                                    <TableCell>{team.updated_at}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Paper>
            </div>
        );
    }
}

export default TeamList;
