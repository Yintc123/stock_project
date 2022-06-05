console.log("hi")

import {url_mode} from './package.js';

import * as search from './search_module.js';
import * as member from './member_module.js';
import * as email from './email_module.js';

let member_info=null;
let email_verification_number=null;


// ----------V(View)----------
async function init(){
    member_info=await member.get_member();
    if (!member_info["data"]){
        window.location=url_mode["url_stock"]; //未登入跳回首頁
    }
    console.log(member_info)

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
// ----------監聽事件----------
const change_button=document.querySelector("#change_button");
const cancel_button=document.querySelector("#cancel_button");
const submit_button=document.querySelector("#submit_button");
const open_eye=document.querySelector("#open_eye");
const close_eye=document.querySelector("#close_eye");
const email_button=document.querySelector("#email_button");
const change_email_button=document.querySelector("#change_email_button");

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
    console.log(input_email_renew)
    email_verification_number=await email.get_verification(input_email_renew);
    console.log(email_verification_number);
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
    console.log(response);
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

// ----------run----------
init();