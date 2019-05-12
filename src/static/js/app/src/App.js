import React from 'react';

// Material UI CSS
import Container from 'muicss/lib/react/container';
import Row from 'muicss/lib/react/row';
import Col from 'muicss/lib/react/col';
import Appbar from 'muicss/lib/react/appbar';

import Tabs from 'muicss/lib/react/tabs';
import Tab from 'muicss/lib/react/tab';
import Button from 'muicss/lib/react/button';

import TeamList from './components/TeamList';
import OrganizationList from './components/OrganizationList';

import { login } from './util/Auth';


class App extends React.Component {
  onChange(i, value, tab, ev) {
    console.log(arguments);
  }

  onActive(tab) {
    console.log(arguments);
  }

  render() {
    login('george', '1234');
    return (
      <Container fluid={true}>
        <link href="//cdn.muicss.com/mui-0.9.41/css/mui.css" rel="stylesheet" type="text/css" />
        <Row>
          <Col md="6" md-offset="3">
            <Appbar>
              {/* <Button color="accent">Teams</Button> */}
            </Appbar>
            <Tabs onChange={this.onChange} defaultSelectedIndex={0}>
              <Tab value="pane-1" label="Organizations" onActive={this.onActive}>
                <OrganizationList />
              </Tab>
              <Tab value="pane-2" label="Teams">
                <TeamList />
              </Tab>
            </Tabs>

          </Col>
        </Row>
      </Container>
    );
  }
}

export default App;
