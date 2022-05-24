console.log("hi");

import * as stock from './stock_module.js';
import * as trading_view from './tv_stock_chart.js';
import * as search from './search_module.js'; //搜尋欄的module

let chart_parameter={};
let transaction_data=null;
let spec_data=null;
let spec_data2=null;
let stk_id=window.location.href.split("/")[3];
const chart_type="candlestick";


// ----------V(View)----------
async function init(){
    transaction_data = await stock.get_stock(stk_id); //api分開request避免延遲太久影響使用者體驗
    show_stock_title(transaction_data["stock_data"]);
    show_stock_info(transaction_data["stock_data"]);
    chart_parameter.chart=trading_view.load_chart("Normal", transaction_data["stock_transaction"], chart_type);

    spec_data = await stock.get_stock_specific_data(stk_id, "PER"); //api分開request避免延遲太久影響使用者體驗
    show_stock_info_table(spec_data["stock_data"], transaction_data, "PER"); 
    
    search.hide_loading();
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
    div_stock_info.append(table);
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
    table_stock_info.append(tr_title);
    let list_data=translate_data_to_list(s_data, t_data)
    for (let i=0;i<list_data.length;i++){
        const tr_data=create_tr(list_data[i], needs, "td");
        table_stock_info.append(tr_data);
    }
    return table_stock_info;
}

function create_tr(json_data, needs, tag){
    const tr_stock_info=document.createElement("tr");
    for (let i=0;i<needs.length;i++){
        const th_stock_info=document.createElement(tag);
        th_stock_info.textContent=json_data[needs[i]];
        tr_stock_info.append(th_stock_info);
    }
    return tr_stock_info;
}

function remove_table(){
    const div_stock_info=document.querySelector("#div_stock_info");
    const table_stock_info=document.querySelector("#table_stock_info");
    div_stock_info.removeChild(table_stock_info);
}
// ----------監聽事件----------
let button_crosshair=document.querySelector("#button_crosshair");
let button_sma=document.querySelectorAll(".button_sma");
let li_block=document.querySelectorAll(".li_block");
let li_block2=document.querySelectorAll(".li_block2");

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

// ----------run----------
init();