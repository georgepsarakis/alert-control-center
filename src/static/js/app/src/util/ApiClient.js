// file: src/util/ApiClient.js
import axios from 'axios';
import store from '../store';
import { URL } from '../config/Api';
import { login } from './Auth';

export const apiClient = function (requires_login) {
    var token = store.getState().token;
    if (requires_login) {
        if (token === null) {
            login('george', '1234');
        }
        token = store.getState().token;
        console.log(token);
    }

    const params = {
        baseURL: URL,
        headers: { 'Authorization': 'Token ' + token }
    };
    console.log(params);
    return axios.create(params);
}
