import {url_mode} from './package.js';

export async function get_message(stock_id){
    let url=url_mode["url_api_message"]+stock_id;
    return await fetch(url).then(response => {
        return response.json();
    })
}

export async function add_message(user_id, stock_id, message){
    let url=url_mode["url_api_message"]+stock_id;
    let data=[user_id, message];
    const query_string=["user_id", "message"]
    let form=new FormData();
    for(let i=0;i<data.length;i++){
        form.append(query_string[i], data[i]);
    }

    return await fetch(url, {
        method:"POST",
        body:form
    }).then(response => {
        return response.json();
    })
}

export async function delete_message(stock_id){
    let url=url_mode["url_api_message"]+stock_id;
    return await fetch(url, {
        method:"DELETE",
        body:null
    }).then(response => {
        return response.json();
    })
}