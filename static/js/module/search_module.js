import {url_mode} from './package.js';
import * as stock from './stock_module.js';

const input_search=document.querySelector("#input_search");
const button_search=document.querySelector("#button_search");

button_search.addEventListener("click", ()=>{
    loading();
    let url=url_mode["url_stock"]+input_search.value;
    if(input_search.value==""){
        window.location=url;
        return;
    }
    stock.get_stock(input_search.value).then(resp => {
        if(resp.error){
            hide_loading();
            alert("查無此股票資訊，可能為ETF或是該股票已下市。");
            input_search.value="";          
            return;
        }
        window.location=url;
    })
    // window.location=url;
})

window.addEventListener("keyup", function(e){//放開鍵盤剎那，觸發該事件
    if(document.activeElement===input_search && (e.code=="Enter" || e.code=="NumpadEnter")){
        button_search.click();
    }
});

// ----------V(View)----------
export function hide_loading(){
    const loading_background=document.querySelector("#background_loading");
    loading_background.style.display="none";
}

function loading(){
    const loading_background=document.querySelector("#background_loading");
    loading_background.style.display="block";
}