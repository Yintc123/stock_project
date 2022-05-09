import {url_mode} from './package.js';

export async function get_stock(){
    return await fetch(url_mode["url_api_stock"])
    .then(response => {
        return response.json();
    })
}