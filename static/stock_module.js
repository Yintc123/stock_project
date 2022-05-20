import {url_mode} from './package.js';

export async function get_stock(stock_id){
    if (stock_id==null){
        stock_id="2330";
    }
    let url=url_mode["url_api_stock"]+stock_id
    return await fetch(url)
                .then(response => {
                    return response.json();
                })
}

export async function get_stock_specific_data(stock_id, data_title){
    let url=url_mode["url_api_stock"]+stock_id+"/"+data_title;
    return await fetch(url)
                .then(response => {
                    return response.json();
                })
}

export async function get_stock_news(){
    let url=url_mode["url_api_stocks_news"];
    return await fetch(url)
                .then(response => {
                    return response.json();
                })
}