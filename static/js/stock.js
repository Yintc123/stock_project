console.log("hi");

import * as stock from './module/stock_module.js';
import * as trading_view from './module/tv_stock_chart.js';
import * as search from './module/search_module.js'; //搜尋欄的module
import * as member from './module/member_module.js';
import * as message from './module/message_module.js';
import {url_mode} from './module/package.js';

let member_info=null;
let chart_parameter={};
let transaction_data=null;
let spec_data=null;
let spec_data2=null;
let stk_id=window.location.href.split("/")[3];
const chart_type="candlestick";


// ----------V(View)----------
async function init(){
    member.get_member().then(resp => {
        member_info=resp;
        if (member_info["data"]){
            member.show_nav_member(member_info["data"]);
            member.show_member_photo(member_info["data"]["photo"]);
            show_favorite_star(check_favorite_star(member_info["data"]["favorite"]));
            show_price_notification(member_info["data"]["email_status"], member_info["data"]["favorite"]);
            show_div_message_member_photo(member_info["data"]["photo"]);
        }else{//未登入
            show_div_message_member_photo("https://icons.veryicon.com/png/128/miscellaneous/somethingxs/person-24.png");
        }
    })

    // stock.get_stock_from_CDN(stk_id).then(resp => { //cdn有資料從cdn抓取
    //     transaction_data=resp;
    //     show_stock_title(transaction_data["stock_data"]);
    //     show_stock_info(transaction_data["stock_data"]);
    //     chart_parameter.chart=trading_view.load_chart("Normal", transaction_data["stock_transaction"], chart_type);
    // }).catch(async (error) => { // cdn無資料從api抓取
    //     console.log(error);
    //     transaction_data=await stock.get_stock(stk_id);
    //     if(transaction_data.error){
    //         window.location=url_mode["url_stock"]; //查無該股票跳回首頁
    //     }
    //     show_stock_title(transaction_data["stock_data"]);
    //     show_stock_info(transaction_data["stock_data"]);
    //     chart_parameter.chart=trading_view.load_chart("Normal", transaction_data["stock_transaction"], chart_type);
    //     // stock.get_stock(stk_id).then(resp => {
    //     //     transaction_data=resp;
    //     //     if(transaction_data.error){
    //     //         window.location=url_mode["url_stock"]; //查無該股票跳回首頁
    //     //     }
    //     //     show_stock_title(transaction_data["stock_data"]);
    //     //     show_stock_info(transaction_data["stock_data"]);
    //     //     chart_parameter.chart=trading_view.load_chart("Normal", transaction_data["stock_transaction"], chart_type);
    //     // })
    // }).then(() => {
    //     stock.get_stock_specific_data(stk_id, "PER").then(resp => {
    //         spec_data=resp;
    //         show_stock_info_table(spec_data["stock_data"], transaction_data, "PER");
    //     })
    // }).then(() => {
    //     search.hide_loading();
    // })


    stock.get_stock(stk_id).then(resp => {
        transaction_data=resp;
        if(transaction_data.error){
            window.location=url_mode["url_stock"]; //查無該股票跳回首頁
        }
        show_stock_title(transaction_data["stock_data"]);
        show_stock_info(transaction_data["stock_data"]);
        chart_parameter.chart=trading_view.load_chart("Normal", transaction_data["stock_transaction"], chart_type);
    }).then(()=>{
        stock.get_stock_specific_data(stk_id, "PER").then(resp => {
            spec_data=resp;
            show_stock_info_table(spec_data["stock_data"], transaction_data, "PER");
        }).then(() => {
            search.hide_loading();
        })
    })
    
    message.get_message(stk_id).then(resp => {
        let message_data=resp;
        show_message_column(message_data["data"]);
    })
}

function show_stock_info(t_data){
    const block=document.querySelectorAll(".block");
    for(let i=0;i<block.length;i++){
        block[i].textContent=t_data[block[i].id.split("_")[1]];
    }
}

function show_stock_title(t_data){
    const stock_name=document.querySelector("#stock_name");
    const stock_id=document.querySelector("#stock_id");
    stock_name.textContent=t_data["stock_name"];
    stock_id.textContent=t_data["stock_id"];
}

function show_stock_info_table(s_data, t_data, data_abbreviation){
    const div_stock_info=document.querySelector("#div_stock_info");
    const table=create_table(s_data, t_data, data_abbreviation)
    div_stock_info.appendChild(table);
}

function create_table(s_data, t_data, data_abbreviation){
    const table_stock_info=document.createElement("table");
    table_stock_info.id="table_stock_info";
    const data_titles={
        "PER":"本益比",
        "dividend-yield":"現金殖利率(%)",
        "PBR":"股價淨值比",
        "EPS":"EPS",
        "ROE":"ROE(%)"
    }
    const data_index={
        "PER":0,
        "dividend-yield":0,
        "PBR":0,
        "EPS":1,
        "ROE":1
    }

    const titles=[
        {"date":"日期", "stock_name":"股票名稱", "stock_id":"股票代號", "close":"收盤"},
        {"year":"年份", "stock_name":"股票名稱", "stock_id":"股票代號"},
    ];
    titles[data_index[data_abbreviation]][data_abbreviation]=data_titles[data_abbreviation];
    const needs=Object.keys(titles[data_index[data_abbreviation]]);
    const tr_title=create_tr(titles[data_index[data_abbreviation]], needs, "th");
    table_stock_info.appendChild(tr_title);
    let list_data=translate_data_to_list(s_data, t_data)
    for (let i=0;i<list_data.length;i++){
        const tr_data=create_tr(list_data[i], needs, "td");
        table_stock_info.appendChild(tr_data);
    }
    return table_stock_info;
}

function create_tr(json_data, needs, tag){
    const tr_stock_info=document.createElement("tr");
    for (let i=0;i<needs.length;i++){
        const th_stock_info=document.createElement(tag);
        th_stock_info.textContent=json_data[needs[i]];
        tr_stock_info.appendChild(th_stock_info);
    }
    return tr_stock_info;
}

function remove_table(){
    const div_stock_info=document.querySelector("#div_stock_info");
    const table_stock_info=document.querySelector("#table_stock_info");
    div_stock_info.removeChild(table_stock_info);
}

function show_favorite_star(flag_favorite){
    if (flag_favorite==1){
        yellow_star.style.display="inline-block";
        white_star.style.display="none";
    }else{
        white_star.style.display="inline-block";
        yellow_star.style.display="none";
    }
}

function show_price_notification(email_status, favorite){
    const div_notification=document.querySelector("#div_notification");
    // const price_notification=document.querySelector("#price_notification");
    div_notification.style.display="inline-block";
    // price_notification.readOnly=true;
    if(/*email_status==1 &&*/ check_favorite(favorite)){
        // price_notification.readOnly=false;
        // price_notification.value=get_price(favorite);
        input_price(1, get_price(favorite));
    }else{
        input_price(0, "");
    }
}

function input_price(flag, price){
    //flag=1，可輸入股票價格
    //flag=0，反之
    const price_notification=document.querySelector("#price_notification");
    if(flag==1){
        price_notification.placeholder="請輸入股價";
        price_notification.readOnly=false;
        price_notification.value=price;
    }else{
        price_notification.placeholder="請加入關注";
        price_notification.readOnly=true;
        price_notification.value="";
    }
}

function show_div_message_member_photo(member_photo){
    const div_message_member_photo=document.querySelector("#div_message_member_photo");
    if(!member_photo){
        member_photo="/static/icon/default_member.jpg";
    }
    div_message_member_photo.style.backgroundImage="url('"+member_photo+"')";
}

function show_message_column(message_data){
    const div_message_column=document.querySelector("#div_message_column"); 
    for(let i=0;i<message_data.length;i++){
        let new_time=handle_time_format(message_data[i]["creation_time"]);
        const div_board=show_message_div(message_data[i]["username"], 
                                         message_data[i]["message"], 
                                         message_data[i]["photo"], 
                                         new_time, 1);
        div_message_column.appendChild(div_board);
    }
}

function show_message_div(member_name, message, member_photo, time, order){
    reorder_div_board();
    const div_board=document.createElement("div");
    const message_member_photo=document.createElement("div");
    div_board.className="div_board";
    div_board.style.order=order;
    message_member_photo.className="message_member_photo";
    if(!member_photo){
        member_photo="/static/icon/default_member.jpg";
    }
    message_member_photo.style.backgroundImage="url('"+member_photo+"')";
    const div_post_message=show_message(member_name, message, time);
    
    div_board.appendChild(message_member_photo);
    div_board.appendChild(div_post_message);
    
    return div_board;
}

function show_message(member_name, message, time){
    const div_post_message=document.createElement("div");
    const message_member_name=document.createElement("div");
    const div_message=document.createElement("div");
    div_post_message.className="div_post_message";
    message_member_name.className="message_member_name";
    div_message.className="div_message";
    message_member_name.textContent=member_name;
    div_message.textContent=message;
    const div_message_others=show_others(time);
    div_post_message.appendChild(message_member_name);
    div_post_message.appendChild(div_message);
    div_post_message.appendChild(div_message_others);
    return div_post_message;
}

function show_others(time){
    const div_message_others=document.createElement("div");
    const div_message_time=document.createElement("div");
    div_message_others.className="div_message_others";
    div_message_time.className="div_message_time";
    // let new_time=handle_time_format(time);
    div_message_time.textContent=time;
    div_message_others.appendChild(div_message_time);
    return div_message_others;
}

function show_message_button(flag){
    const ul_message_button=document.querySelector("#ul_message_button");
    if(flag==0){
        div_typing.textContent="";
        ul_message_button.style.display="none";
        return;
    }
    ul_message_button.style.display="flex";
}
// ----------監聽事件----------
let button_crosshair=document.querySelector("#button_crosshair");
let button_sma=document.querySelectorAll(".button_sma");
let li_block=document.querySelectorAll(".li_block");
let li_block2=document.querySelectorAll(".li_block2");
const white_star=document.querySelector("#white_star");
const yellow_star=document.querySelector("#yellow_star");
const button_notification=document.querySelector("#button_notification");
const button_message_submit=document.querySelector("#button_message_submit");
const div_typing=document.querySelector("#div_typing");
const button_message_cancel=document.querySelector("#button_message_cancel");

button_crosshair.addEventListener("click", () => {
    chart_parameter.chart.remove();
    chart_parameter={};
    if (button_crosshair.textContent=="Magnet"){
        button_crosshair.textContent="Normal";
        chart_parameter.chart=trading_view.load_chart("Magnet", transaction_data["stock_transaction"], chart_type);
    }else{
        button_crosshair.textContent="Magnet";
        chart_parameter.chart=trading_view.load_chart("Normal", transaction_data["stock_transaction"], chart_type);
    }
})

for (let i=0;i<button_sma.length;i++){
    button_sma[i].addEventListener("click", () => {
        let days=button_sma[i].id.split("-")[1];
        if(chart_parameter["sma_"+days]){
            chart_parameter.chart.removeSeries(chart_parameter["sma_"+days]);
            chart_parameter["sma_"+days]=null;
            return;
        }
        const color={
            "10":"rgba(4, 111, 232, 1)",
            "30":"#00EC00",
            "365":"#FF00FF"
        }
        chart_parameter["sma_"+days]=trading_view.add_sma(chart_parameter.chart, transaction_data["stock_transaction"], days, color[days]);
    })
}

for (let i=0;i<li_block.length;i++){
    li_block[i].addEventListener("click", () => {
        remove_table();
        let data_abbreviation=li_block[i].id.split("_")[1];
        show_stock_info_table(spec_data["stock_data"], transaction_data, data_abbreviation);
    })
}

for (let i=0;i<li_block2.length;i++){
    li_block2[i].addEventListener("click", async () => {
        remove_table();
        if (!spec_data2){
            spec_data2=await stock.get_stock_specific_data(stk_id, "EPS");
        }
        let data_abbreviation=li_block2[i].id.split("_")[1];
        show_stock_info_table(spec_data2["stock_data"], transaction_data, data_abbreviation);
    })
}

white_star.addEventListener("click", async () => {
    show_favorite_star(1);
    input_price(1, "");
    let response=await member.add_favorite_stock(member_info["data"]["id"], stk_id);
    // if (member_info["data"]["email_status"]==1){
    //     input_price(1, "");
    // }
    // input_price(1, "");
    console.log(response);
})

yellow_star.addEventListener("click", async () => {
    show_favorite_star(0);
    input_price(0, "");
    let response=await member.delete_favorite_stock(member_info["data"]["id"], stk_id);
    // if (member_info["data"]["email_status"]==1){
    //     input_price(0, "");
    // }
    // input_price(0, "");
    console.log(response);
})

button_notification.addEventListener("click", async () => {
    const price_notification=document.querySelector("#price_notification");
    if (price_notification.readOnly){
        console.log("請將此股票添加至我的最愛");
        return;
    }
    alert("設定成功!");
    let response=await member.add_price_notification(member_info["data"]["id"], stk_id, price_notification.value);
    console.log(response);
})

button_message_submit.addEventListener("click", async () => {
    const div_message_column=document.querySelector("#div_message_column");
    const div_typing=document.querySelector("#div_typing");
    let msg=div_typing.textContent;
    if (msg=="") return;
    div_typing.textContent="";
    const message_div=show_message_div(member_info["data"]["username"], msg, member_info["data"]["photo"], GetDateTimeToString(), 1);
    div_message_column.appendChild(message_div)
    let response=await message.add_message(member_info["data"]["id"], stk_id, msg);
    console.log(response);
})

div_typing.addEventListener("click", () => {
    if (!member_info["data"]){
        member_center.click();
        return;
    }
    show_message_button(1);
})

button_message_cancel.addEventListener("click", () => {
    show_message_button(0);
})

const clear_button=document.querySelector("#button_clear")
clear_button.addEventListener("click", async () => {
    let resp=await message.delete_message(stk_id);
    console.log(resp)
    const div_message_column=document.querySelector("#div_message_column");
    while(div_message_column.firstChild){
        div_message_column.removeChild(div_message_column.firstChild);
    }
})
// ----------M(Model)----------

function translate_data_to_list(s_data, t_data){
    let new_t_data=t_data["stock_transaction"].slice(t_data["stock_transaction"].length-Object.keys(s_data).length) //從array中取所需的資料(slice為深拷貝)
    let new_s_data=JSON.parse(JSON.stringify(s_data)); //深拷貝，避免汙染原始資料
    let list_data=[];
    for (let key in new_s_data){
        new_s_data[key]["stock_name"]=t_data["stock_data"]["stock_name"];
        new_s_data[key]["close"]=new_t_data[key]["close"];
        
        list_data.push(new_s_data[key]);
    }

    list_data=list_data.reverse();
    return list_data;
}


function check_favorite_star(data){
    for(let i=0;i<data.length;i++){
        if(data[i]["stock_id"]==stk_id){
            return 1;
        }
    }
    return 0;
}

function get_price(favorite){
    for(let i=0;i<favorite.length;i++){
        if(favorite[i]["stock_id"]==stk_id){
            return favorite[i]["price"];
        }
    }
    return "";
}

function check_favorite(favorite){
    for(let i=0;i<favorite.length;i++){
        if(favorite[i]["stock_id"]==stk_id){
            return true;
        }
    }
    return false;
}

function reorder_div_board(){
    const div_board=document.querySelectorAll(".div_board");
    for(let i=0;i<div_board.length;i++){
        div_board[i].style.order++;
    }
}

function handle_time_format(time){
    const months = {
        Jan: '01',
        Feb: '02',
        Mar: '03',
        Apr: '04',
        May: '05',
        Jun: '06',
        Jul: '07',
        Aug: '08',
        Sep: '09',
        Oct: '10',
        Nov: '11',
        Dec: '12',
      }
    time=time.split(",")[1].split(" ").slice(1, 5);
    let new_time=[time[2], months[time[1]], time[0]];
    let temp=time[3].split(":");
    temp[0]=parseInt(temp[0])+8;
    if(temp[0]<10){
        temp[0]="0"+temp[0].toString();
    }else{
        temp[0]=temp[0].toString();
    }
    new_time=new_time.join("/")+" "+temp.join(":");
    return new_time;
}

function GetDateTimeToString(){
    let time = new Date();
    let year = time.getFullYear();
    let month = time.getMonth()+1;
    let day = time.getDate();
    if(month<10) month = "0"+month;
    if(day<10) day = "0"+day;

    let hours = time.getHours();
    let mins = time.getMinutes();
    let secs = time.getSeconds();
    let msecs = time.getMilliseconds();
    if(hours<10) hours = "0"+hours;
    if(mins<10) mins = "0"+mins;
    if(secs<10) secs = "0"+secs;
    if(msecs<10) secs = "0"+msecs;
    return year+"/"+month+"/"+day+" "+hours+":"+mins+":"+secs;
}
// ----------run----------
init();

console.log(GetDateTimeToString())

// let socket = io();
// socket.connect('http://127.0.0.1:5000/'+stk_id);
// socket.on('connect', (resp) => {
//     socket.send('b');
//     console.log(resp)
// })
// socket.on('message', (msg) => {
//     console.log(msg);
//     socket.send('a');
// })

// socket.on('connect', function() {
//     socket.emit('my event', {data: 'I\'m connected!'});
// });