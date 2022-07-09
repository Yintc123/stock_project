import {url_mode} from './module/package.js';
import * as search from './module/search_module.js';
import * as member from './module/member_module.js';
import * as email from './module/email_module.js';

let member_info=null;
let email_verification_number=null;


// ----------V(View)----------
async function init(){
    member_info=await member.get_member();
    if (!member_info["data"]){
        window.location=url_mode["url_stock"]; //未登入跳回首頁
    }
    // console.log(member_info)

    show_favorite_stock_in_table(member_info["data"]["favorite"]);
    show_member_info(member_info["data"]);
    show_email_verification_icon(member_info["data"]["email_status"]);
    member.show_nav_member(member_info["data"]);
    member.show_member_photo(member_info["data"]["photo"]);
    search.hide_loading();
}

function show_member_info(info){
    const member_username=document.querySelector("#member_username");
    const member_email=document.querySelector("#member_email");
    // const member_password=document.querySelector("#member_password");
    member_username.textContent=info["username"];
    member_email.textContent=info["email"];
    // member_password.textContent=info["password"];
}

function change_member_info_pattern(flag){
    const input_member_info=document.querySelector("#input_member_info");
    const member_info=document.querySelector("#member_info");;
    change_button_pattern(flag);
    if(flag==0){
        member_info.style.display="inline-block";
        input_member_info.style.display="none";
        return;
    }
    member_info.style.display="none";
    input_member_info.style.display="flex";
    return
}

function show_email_verification_input(flag){
    const email_verification=document.querySelectorAll(".email_verification");
    const input_email_renew=document.querySelector("#input_email_renew");
    const input_email_verify=document.querySelector("#input_email_verify");
    let display="block";
    if(flag==0){
        input_email_renew.readOnly=true;
        input_email_renew.value=member_info["data"]["email"];
        change_email_button.textContent="變更信箱";
        input_email_verify.value="";
        display="none";
    }else{
        input_email_renew.readOnly=false;
        change_email_button.textContent="取消變更";
    }
    for(let i=0;i<email_verification.length;i++){
        email_verification[i].style.display=display;
    }
}

function change_button_pattern(flag){
    const li_renew_button=document.querySelectorAll(".li_renew_button");
    let display="inline-block";
    if(flag==0){
        display="none";
        change_button.style.display="inline-block";
    }else{
        change_button.style.display="none";
    }
    
    for(let i=0;i<li_renew_button.length;i++){
        li_renew_button[i].style.display=display;
    }
}

function show_resp_message(status, response){
    const p_resp_message=document.querySelector("#p_resp_message");
    if(status==0){
        p_resp_message.style.display="none";
        return;
    }
    p_resp_message.style.display="inline-block"
    p_resp_message.textContent=response.message;
    if (response.error){
        p_resp_message.style.color="red";
    }else{
        p_resp_message.style.color="blue";
    }
}

function show_input_info(info){
    const input_username_renew=document.querySelector("#input_username_renew");
    const input_email_renew=document.querySelector("#input_email_renew");
    input_username_renew.value=info["username"];
    input_email_renew.value=info["email"];
}

function change_eyes(flag, member_password){
    const span_password=document.querySelector("#span_password");
    if(flag==0){
        span_password.textContent="******";
        close_eye.style.display="none";
        open_eye.style.display="block";
    }else{ //顯示密碼
        span_password.textContent=member_password;
        close_eye.style.display="block";
        open_eye.style.display="none";
    }
}

function show_email_verification_icon(email_status){
    const verification_icon=document.querySelector("#verification_icon");
    const pass_msg=document.querySelector("#pass_msg");
    const fail_msg=document.querySelector("#fail_msg");
    if(email_status==1){
        verification_icon.src="/static/icon/ok.png";
        pass_msg.style.display="block";
        fail_msg.style.display="none";
        return;
    }
    verification_icon.src="/static/icon/fail.png";
    fail_msg.style.display="block";
    pass_msg.style.display="none";
}

function show_member_frame_info(flag){
    const frame_member_info=document.querySelector("#frame_member_info");
    if(flag==1){
        frame_member_info.style.display="block";
        return;
    }
    frame_member_info.style.display="none";
}

function show_frame_favorite(flag){
    const frame_favorite=document.querySelector("#frame_favorite");
    if(flag==1){
        frame_favorite.style.display="block";
        return;
    }
    frame_favorite.style.display="none";
}

function show_favorite_stock_in_table(favorite){
    const table_favorite=document.querySelector("#table_favorite");
    const needs=["index", "favorite", "stock_id", "stock_name", "price"]
    let new_lst=arrange_favorite_list(favorite);
    for(let i=0;i<new_lst.length;i++){
        const tr=create_tr(new_lst[i], needs);
        table_favorite.append(tr);
    }

    return table_favorite;
}

function create_tr(favorite, needs){
    const tr_stock_info=document.createElement("tr");
    tr_stock_info.id="tr"+favorite[needs[2]];
    tr_stock_info.className="tr_favorite";
    for (let i=0;i<needs.length;i++){
        const th_stock_info=document.createElement("td");
        if(i==1){
            th_stock_info.style.backgroundImage=favorite["favorite"];
            th_stock_info.className="yellow_star";
            th_stock_info.id="yellow_star"+favorite[needs[2]];
            add_star_event(th_stock_info, favorite[needs[2]], favorite["index"]);
            tr_stock_info.append(th_stock_info);
            continue;
        }else if (i==2){
            const a=document.createElement("a");
            a.textContent=favorite[needs[i]];
            a.href=url_mode["url_stock"]+favorite[needs[i]];
            th_stock_info.append(a);
            tr_stock_info.append(th_stock_info);
            continue
        }
        th_stock_info.textContent=favorite[needs[i]];
        tr_stock_info.append(th_stock_info);
    }
    return tr_stock_info;
}

function add_star_event(obj, stk_id, index){
    obj.addEventListener("click", async () => {
        let favorite=member_info["data"]["favorite"];
        favorite.splice(index-1, 1); // 去除favorite stock
        // let tr_id="#tr"+stk_id;
        // const table_favorite=document.querySelector("#table_favorite");
        const tr_favorite=document.querySelectorAll(".tr_favorite");
        for (let i=0;i<tr_favorite.length;i++){
            tr_favorite[i].remove(); //刪除favorite table的tr
        }
        show_favorite_stock_in_table(favorite); // 重新產生favorite table
        // const tr=document.querySelector(tr_id);
        // table_favorite.removeChild(tr);
        const response=await member.delete_favorite_stock(member_info["data"]["id"], stk_id);
        // console.log(response);
    })
}

let reg=null;
function set_push_subscribe(){
    if (!('serviceWorker' in navigator)) // 確認支援service worker
        return;
        navigator.serviceWorker.ready.then((sw) => {
            // console.log("推播api")
            reg=sw;
            return sw.pushManager.getSubscription(); //取得訂閱狀態
        }).then((sub) => {
            if(sub === null){
                //建立新的訂閱
                let vapidPKey = 'BLkF7TRSoLm8SHYKq-rIEtZ4LbEzBghYQwrrtUjtOD-EIjmOIHr1q8YAEbiWVLGX9HMrX7UJSaUMifKhsDdniXE';
                let convertedVapidPKey = url_Base64_to_Uint8Array(vapidPKey);
                return reg.pushManager.subscribe({
                    userVisibleOnly: true, //送出去的訊息，只有此訂閱戶可以看到
                    applicationServerKey: convertedVapidPKey
                }).then((new_Subscription) => {
                    let form=new FormData();
                    let user_id=member_info["data"]["id"];
                    let subscription=JSON.stringify(new_Subscription); //重要，service worker辨別身分的token
                    form.append("user_id", user_id);
                    form.append("subscription", subscription);
                    return fetch(url_mode["url_api_subscription"], {
                        method: 'POST',
                        body: form
                    });
                }).then((response) => {
                    if(response.ok)
                        // console.log(response);
                        display_notification();
                })
                .catch((err) => {
                    // console.log('訂閱失敗',err);
                });;
            }else{
                //已經訂閱
                // console.log('已經訂閱');
            }
        });
}

function display_notification(){
    new Notification("到價通知訂閱成功!");
 }
// ----------監聽事件----------
const change_button=document.querySelector("#change_button");
const cancel_button=document.querySelector("#cancel_button");
const submit_button=document.querySelector("#submit_button");
const open_eye=document.querySelector("#open_eye");
const close_eye=document.querySelector("#close_eye");
const email_button=document.querySelector("#email_button");
const change_email_button=document.querySelector("#change_email_button");
const button_member_frame=document.querySelector("#button_member_frame");
const button_favorite_frame=document.querySelector("#button_favorite_frame");
const changing_photo=document.querySelector("#changing_photo");
const img_uploader=document.querySelector("#img_uploader");
const button_web_push=document.querySelector("#button_web_push");
const button_web_push_cancel=document.querySelector("#button_web_push_cancel");


change_button.addEventListener("click", () => {
    change_member_info_pattern(1);
    show_input_info(member_info["data"]);
})

cancel_button.addEventListener("click", () => {
    change_member_info_pattern(0);
    show_resp_message(0, null);
    show_email_verification_input(0);
})

email_button.addEventListener("click", async () => {
    const input_email_renew=document.querySelector("#input_email_renew").value;
    // console.log(input_email_renew)
    email_verification_number=await email.get_verification(input_email_renew);
    // console.log(email_verification_number);
})

change_email_button.addEventListener("click", () => {
    if(change_email_button.textContent=="變更信箱"){
        show_email_verification_input(1);   
    }else{
        show_email_verification_input(0);
    }
})

submit_button.addEventListener("click", async () => {
    const input_username_renew=document.querySelector("#input_username_renew").value;
    const input_email_renew=document.querySelector("#input_email_renew").value;
    const input_email_verify=document.querySelector("#input_email_verify").value;
    const input_password_renew=document.querySelector("#input_password_renew").value;

    let response=await member.renew_member(member_info["data"]["id"], input_username_renew, input_email_renew, input_password_renew, null, input_email_verify);
    // console.log(response);
    show_resp_message(1, response);
    if (!response.error){
        window.location=window.location.href;
    }
})

let flag_eyes=1;
open_eye.addEventListener("click", async () => {
    if(flag_eyes==0) return;
    let flag_temp=flag_eyes;
    flag_eyes=0;
    let all_member_info=await member.get_all_member_info(member_info["data"]["id"]);
    change_eyes(flag_temp, all_member_info["data"]["password"]);
})

close_eye.addEventListener("click", async () => { 
    if(flag_eyes==1) return; 
    change_eyes(flag_eyes, null);
    flag_eyes=1;
})

button_member_frame.addEventListener("click", () => { 
    show_member_frame_info(1);
    show_frame_favorite(0);
})

button_favorite_frame.addEventListener("click", () => { 
    show_member_frame_info(0);
    show_frame_favorite(1);
})

changing_photo.addEventListener("click", () => { 
    img_uploader.click();
})

img_uploader.addEventListener("change", async function(e){ //不能使用 (e) => {}，why? 
    // console.log(e);
    const reader=new FileReader();
    reader.addEventListener("load", () => {
        let image=new Image();
        image.src=reader.result;
        image.onload=function(){
            compress_img(image);//壓縮圖片
        }
    })
    reader.readAsDataURL(this.files[0]);
    let resp=await member.renew_member(member_info["data"]["id"], null, null, null, e.target.files[0], null); // 將file格式的圖片傳至後端處理
    // console.log(resp);
})

button_web_push.addEventListener("click", () => {
    if (!"Notification" in window){ // 確認瀏覽器支援網頁推播
        // console.log("不支援網頁推播");
        return;
    }
    // console.log(Notification.permission);
    Notification.requestPermission((status) => { // 會被丟入callback queue
        // This allows to use Notification.permission with Chrome/Safari
        if (Notification.permission !== status) { // 為什麼要做這個?
            Notification.permission = status;
        }
        if (Notification.permission !== "granted"){
            // console.log("拒絕訂閱通知!");
        }
        set_push_subscribe(); // 訂閱網站推播
    })
})



button_web_push_cancel.addEventListener("click", async () => {
    let form=new FormData();
    let user_id=member_info["data"]["id"];
    form.append("user_id", user_id);
    let url=url_mode["url_api_push"];
    const response = await fetch(url, {
        method: "POST",
        body:form
    }).then(resp => {
        return resp.json();
    })
})
// ----------M(Model)---------
function arrange_favorite_list(lst){
    // let new_lst=JSON.parse(JSON.stringify(lst)) //深拷貝，避免汙染原始資料
    let new_lst=lst;
    for(let i=0;i<new_lst.length;i++){
        new_lst[i]["favorite"]="url('/static/icon/yellow_star.png')";
        if(new_lst[i]["price"]==0 || new_lst[i]["price"]==null){
            new_lst[i]["price"]="未設定";
        }
        new_lst[i]["index"]=i+1;
    }
    return new_lst;
}

function compress_img(img){
    const canvas=document.createElement("canvas");
    canvas.width=200;
    canvas.height=200;
    let ctx=canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, 200, 200);
    canvas.toBlob((blob)=>{
        blob_to_data_url(blob, (data_url)=>{
            upload_img(data_url);
        });
    },"image/jpeg", 0.8);//以canvas繪圖後儲存為jpeg格式並壓縮比例為0.8
}

function upload_img(img_blob){
    const member_photo=document.querySelectorAll(".member_photo");
    for(let i=0;i<member_photo.length;i++){
        member_photo[i].src=img_blob;
    }
}

function blob_to_data_url(blob, callback){
    const reader=new FileReader();
    reader.addEventListener("load",(e) => {
        callback(e.target.result);
    })
    reader.readAsDataURL(blob);
}

function url_Base64_to_Uint8Array(base64String){ // VAPID_public_key解碼
    let padding = '='.repeat((4 - base64String.length % 4) % 4);
    let base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g,'/');
    let rawData = window.atob(base64);
    let outputArr = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i ){
        outputArr[i] = rawData.charCodeAt(i);
    }    
    return outputArr;
}
// ----------run----------
init();
