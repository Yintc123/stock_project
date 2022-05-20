import {url_mode} from './package.js';

const input_search=document.querySelector("#input_search");
const button_search=document.querySelector("#button_search");

button_search.addEventListener("click", ()=>{
    let url=url_mode["url_stock"]+input_search.value;
    window.location=url;
})

window.addEventListener("keyup", function(e){//放開鍵盤剎那，觸發該事件
    if(document.activeElement===input_search && (e.code=="Enter" || e.code=="NumpadEnter")){
        button_search.click();
    }
});

// ----------V(View)----------
export function hide_loading(){
    const loading_background=document.querySelector("#loading_background");
    loading_background.style.display="none";
}