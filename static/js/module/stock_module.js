import {url_mode} from './package.js';

export async function get_stock(stock_id){
    let url=url_mode["url_api_stock"]+stock_id
    return await fetch(url)
                .then(response => {
                    return response.json();
                })
}

export async function get_stock_from_CDN(stock_id){
    let today=new Date();
    let y=today.getFullYear();
    let m=(today.getMonth()+1)
    if (m <10){
        m="0"+m;
    }
    let d=today.getDate()>=10 ? today.getDate():("0"+today.getDate());
    let filename=stock_id+y+"_"+m+"_"+d+".json";
    console.log(filename);
    let url=url_mode["url_cdn"]+filename;
    return await fetch(url).then(response => {
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

export async function get_server_time(){
    let url="https://yin888.info/api/time";
    return await fetch(url).then(response => {
        return response.json();
    })
}