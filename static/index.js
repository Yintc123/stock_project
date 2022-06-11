console.log("hi");

import * as stock from './stock_module.js';
import * as trading_view from './tv_stock_chart.js';
import * as member from './member_module.js';
import * as search from './search_module.js';


let chart_parameter={};
const chart_type="index";
let news_data=null;
let TAIEX_data=null;
let member_info=null;
const news_trademark={
    "Yahoo奇摩新聞":"https://s.yimg.com/cv/apiv2/twfrontpage/logo/Yahoo-TW-desktop-FP@2x.png",
    "Yahoo奇摩股市":"https://s.yimg.com/rz/p/yahoo_finance_zh-Hant-TW_h_p_financev2.png",
    "udn.com":"https://udn.com/static/img/logo.svg?2020020601",
    "中時新聞網 Chinatimes.com":"https://static.chinatimes.com/images/2020/logo-chinatimes2020.svg",
    "旺得富 WantRich":"https://wr-static.chinatimes.com/images/wantrich_logo.svg",
    "經濟日報":"https://money.udn.com/static/img/logo.png?1",
    "自由財經":"https://cache.ltn.com.tw/images/rwd_ltnlogo.png",
    "ETtoday財經雲":"https://cdn2.ettoday.net/style/finance2020/images/logo.png",
    "三立新聞網 Setn.com":"https://attach.setn.com/images/2018_logo_B.png",
    "Anue鉅亨":"https://sfiles.cnyes.cool/fe-common/ccbabd1c/ac25a5abb8fcbdfddb46fa4e9bca6b06.svg",
    "今周刊-在今天看見明天":"https://www.businesstoday.com.tw/lazyweb/web/img/logo2x.png",
    "財訊":"https://www.wealth.com.tw/fbc16f9148c47642c2b0.png",
    "MoneyDJ理財網":"https://cdn.flipboard.com/dev_O/featured/28833577/logo-250x250.png",
    "蘋果新聞網":"https://staticlayout.appledaily.hk/section-logo/tw/logo_appleonline_w.png",
    "民視新聞網FTVn":"https://newsimg.ftv.com.tw/img/logo.png",
    "Apple Daily TW":"https://staticlayout.appledaily.hk/section-logo/tw/logo_appleonline_w.png",
    "商周財富網":"https://wealth.businessweekly.com.tw/images/bwmoney_logo.png",
    "新浪台灣":"https://newsimgs.sina.tw/assets/images/event_logo/news_logo.0362ff8a0d.jpg",
    "台灣好新聞":"https://www.taiwanhot.net/imgs/logo.png",
    "MSN":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/2015_MSN_logo.svg/1200px-2015_MSN_logo.svg.png",
    "工商時報":"https://cteecors.azureedge.net/wp-content/uploads/2020/02/10-00642-005.png",
    "翻爆":"https://imgv.azureedge.net/wpupload/2019/04/logo.jpg"
};


// ----------V(View)----------
async function init(){
    member_info=await member.get_member();
    if (member_info["data"]){
        member.show_nav_member(member_info["data"]);
        member.show_member_photo(member_info["data"]["photo"]);
    }

    // news_data=await stock.get_stock_news();
    TAIEX_data=await stock.get_stock("TAIEX"); //api分開request避免延遲太久影響使用者體驗
    chart_parameter.chart=trading_view.load_chart("Magnet", TAIEX_data["stock_transaction"], chart_type);

    news_data=await stock.get_stock_news(); //api分開request避免延遲太久影響使用者體驗
    console.log(news_data)
    reorder_news_data(news_data)
    create_news_columns(news_data);
    search.hide_loading();
}

function create_news_columns(raw_data){
    const container_news=document.querySelector("#container_news");
    for (let i=0;i<raw_data["source"].length;i++){
        const n_source=raw_data["source"][i];
        const n_data=raw_data["news_data"][n_source];
        const col=create_news_column(n_data, n_source);
        container_news.appendChild(col);
    }
}

function create_news_column(data, news_source){
    const div_news=document.createElement("div");
    div_news.className="div_news";
    const trademark=create_news_trademark(news_source, data[0]["link"]);
    const news_titles=create_news_title(data);
    div_news.appendChild(trademark);
    div_news.appendChild(news_titles);
    return div_news;
}

function create_news_trademark(source, first_news_link){
    const trademark=document.createElement("div");
    const img_trademark=document.createElement("img");
    const a_news=document.createElement("a");
    a_news.href=first_news_link;
    trademark.className="trademark";
    img_trademark.src=news_trademark[source];
    if (source=="ETtoday財經雲"){
        trademark.style.backgroundColor="red";
    }
    if (source=="蘋果新聞網" || source=="Apple Daily TW"){
        trademark.style.backgroundColor="#0096df";
    }
    if (source=="商周財富網"){
        trademark.style.backgroundColor="black";
    }
    
    a_news.appendChild(img_trademark);
    trademark.appendChild(a_news);
    return trademark;
}

function create_news_title(data){
    const news_titles=document.createElement("div");
    news_titles.className="news_titles";
    for(let i=0;i<data.length;i++){
        const h3_news_titles=document.createElement("h3");
        const a_news_titles=document.createElement("a");
        a_news_titles.textContent=data[i]["title"];
        a_news_titles.href=data[i]["link"];
        h3_news_titles.appendChild(a_news_titles);
        news_titles.appendChild(h3_news_titles);
    }
    return news_titles;
}
// ----------監聽事件----------
const button_reset=document.querySelector("#button_reset");

button_reset.addEventListener("click", () => {
    chart_parameter.chart.remove();
    chart_parameter.chart=trading_view.load_chart("Magnet", TAIEX_data["stock_transaction"], chart_type);
})

// ----------M(Model)----------
function reorder_news_data(news_data){
    for(let i=0;i<news_data["source"].length;i++){
        for(let j=i+1;j<news_data["source"].length;j++){
            if(news_data["news_data"][news_data["source"][i]].length<news_data["news_data"][news_data["source"][j]].length){
                let temp=news_data["source"][i];
                news_data["source"][i]=news_data["source"][j];
                news_data["source"][j]=temp;
            }
        }
    }
}
// ----------run----------
init();