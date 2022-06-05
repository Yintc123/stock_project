import {url_mode} from './package.js';

let flag_sign_pattern=0;
const button_text={
    "sign_in":"登入帳戶",
    "sign_up":"註冊新帳戶"
}

// ----------V(View)----------
function show_frame(swch){
    const background_member=document.querySelector("#background_member");
    const frame_member=document.querySelector("#frame_member");
    if (swch==0){
        background_member.style.display="inline-block";
        frame_member.style.display="flex";
    }else{
        background_member.style.display="none";
        frame_member.style.display="none";
    }
}

function change_sign_pattern(flag){
    const input_username=document.querySelector("#input_username");
    if(flag==0){
        input_username.style.display="inline-block";
    }else{
        input_username.style.display="none";
    }
    change_member_sucess_error_message(null, 0)
    change_member_sign_message(flag, 1);
    change_switch_text(flag);
    change_button_text(flag);
}

function change_member_sign_message(sign_flag, show){
    //sign_flag=0，顯示p_member_signUp_message
    //sign_flag=1，顯示p_member_signIn_message
    const div_sign_message=document.querySelector("#div_sign_message");
    const span_member_signIn_message=document.querySelector("#span_member_signIn_message");
    const span_member_signUp_message=document.querySelector("#span_member_signUp_message");
    if(show==0){
        div_sign_message.style.display="none";
        return;
    }
    div_sign_message.style.display="block";
    if (sign_flag==1){
        span_member_signUp_message.style.display="none";
        span_member_signIn_message.style.display="inline-block";
        return;
    }
    span_member_signIn_message.style.display="none";
    span_member_signUp_message.style.display="inline-block";
}

function change_member_sucess_error_message(resp, show){
    const div_success_error_message=document.querySelector("#div_success_error_message");
    const span_member_error_message=document.querySelector("#span_member_error_message");
    const span_member_success_message=document.querySelector("#span_member_success_message");
    if(show==0){
        div_success_error_message.style.display="none";
        return;
    }
    if(resp["error"]==true){
        span_member_success_message.style.display="none";
        span_member_error_message.textContent=resp["message"];
        span_member_error_message.style.display="block";
    }else{
        span_member_error_message.style.display="none";
        span_member_success_message.textContent=resp["message"];
        span_member_success_message.style.display="block";
    }
    div_success_error_message.style.display="block";
}

function change_switch_text(flag){
    //flag=0，顯示"點此登入"
    //flag=1，顯示"點此註冊"
    const span_member_switch=document.querySelector("#span_member_switch");
    if(flag==0){
        span_member_switch.textContent="點此登入";
    }else{
        span_member_switch.textContent="點此註冊";
    }
}

function change_button_text(flag){
    //flag=0，顯示"點此登入"
    //flag=1，顯示"點此註冊"
    const button_member=document.querySelector("#button_member");
    if(flag==0){
        button_member.textContent=button_text.sign_up;
    }else{
        button_member.textContent=button_text.sign_in;
    }
}

function clean_input(){
    const input_username=document.querySelector("#input_username");
    const input_email=document.querySelector("#input_email");
    const input_password=document.querySelector("#input_password");
    input_username.value=null;
    input_email.value=null;
    input_password.value=null;
}

export function show_nav_member(member_info){
    if (member_info){
        member_center.style.display="none";
        li_member_photo.style.display="inline-block";
        return;
    }
    member_center.style.display="inline-block";
    li_member_photo.style.display="none";
    return;
}

function show_div_signOut_frame(swch){
    const div_signOut_frame=document.querySelector("#div_signOut_frame");
    if (swch==0){
        div_signOut_frame.style.display="none";
        return;
    }
    div_signOut_frame.style.display="inline-block";
}

function show_div_signIn_frame(swch){
    const div_signIn_frame=document.querySelector("#div_signIn_frame");
    if (swch==0){
        div_signIn_frame.style.display="none";
        return;
    }
    div_signIn_frame.style.display="inline-block";
}

export function show_member_photo(photo){
    const member_photo=document.querySelectorAll(".member_photo");
    let photo_src="/static/icon/default_member.jpg";
    if(photo){
        photo_src=photo;
    }
    for(let i=0;i<member_photo.length;i++){
        member_photo[i].src=photo_src;
    }
}
// ----------監聽事件----------
const member_center=document.querySelector("#member_center");
const li_member_photo=document.querySelector("#li_member_photo");
const nav_member_photo=document.querySelector("#nav_member_photo");
const close_frame_member=document.querySelectorAll(".close_frame_member");
const button_member=document.querySelector("#button_member");
const span_member_switch=document.querySelector("#span_member_switch");
const button_signOut=document.querySelector("#button_signOut");
const button_member_page=document.querySelector("#button_member_page");
const home_img=document.querySelector("#home_img");

//回首頁
home_img.addEventListener("click", () => {
    window.location=url_mode["url_stock"];

})


//開啟會員登入頁面
member_center.addEventListener("click", () => {
    show_div_signOut_frame(1);
    show_frame(0);
    change_sign_pattern(1);//登入/註冊預設畫面為登入畫面

})

//關閉會員登入頁面
for (let i=0;i<close_frame_member.length;i++){
    close_frame_member[i].addEventListener("click", () => {
        show_frame(1);
        clean_input();
        flag_sign_pattern=0;//關閉登入頁面，flag回到預設值
    })
    show_div_signOut_frame(0);
    show_div_signIn_frame(0);
}


button_member.addEventListener("click", async() => {
    const input_username=document.querySelector("#input_username");
    const input_email=document.querySelector("#input_email");
    const input_password=document.querySelector("#input_password");
    const username=input_username.value;
    const email=input_email.value;
    const password=input_password.value;
    let response=null;
    if (button_member.textContent==button_text.sign_in){
        response=await signIn_member(email, password);
        change_member_sign_message(null, 0);
        change_member_sucess_error_message(response, 1);
        if (response["ok"]){
            window.location=window.location.href;
        }
        return;
    }
    response=await signUp_member(username, email, password);
    change_member_sign_message(null, 0);
    change_member_sucess_error_message(response, 1);
    return;
})

//登入/註冊會員切換框架
span_member_switch.addEventListener("click", () => {
    clean_input();
    change_sign_pattern(flag_sign_pattern);
    if(flag_sign_pattern==0){
        flag_sign_pattern=1;
    }else{
        flag_sign_pattern=0;
    }
})

nav_member_photo.addEventListener("click", () => {
    show_div_signIn_frame(1);
    show_frame(0);
})

button_signOut.addEventListener("click", () => {
    signOut_member();
    window.location=window.location.href;
})

button_member_page.addEventListener("click", () => {
    window.location=url_mode["url_member"];
})

// ----------M(Model)----------
export async function get_member(){
    return await fetch(url_mode["url_api_member"]).then(response => {
        return response.json();
    })
}

async function signOut_member(){
    return  await fetch(url_mode["url_api_member"], {
        method:"DELETE"
    }).then(response => {
        return response.json();
    })
}

async function signIn_member(email, password){
    let form=new FormData();
    const member_info=[email, password];
    const query_string=["email", "password"];
    for (let i=0;i<query_string.length;i++){
        form.append(query_string[i], member_info[i]);
    }

    return await fetch(url_mode["url_api_member"], {
        method:"PATCH",
        body:form
    }).then(response => {
        return response.json();
    })
}

async function signUp_member(username, email, password){
    let form=new FormData();
    const member_info=[username, email, password];
    const query_string=["username", "email", "password"];
    for (let i=0;i<query_string.length;i++){
        form.append(query_string[i], member_info[i]);
    }
    
    return await fetch(url_mode["url_api_member"], {
        method:"POST",
        body:form
    }).then(response => {
        return response.json();
    })
}

export async function renew_member(member_id, username, email, password, photo, email_verification){
    let form=new FormData();
    const member_info=[username, email, password, photo, email_verification];
    const query_string=["username", "email", "password", "photo", "email_verification"];
    for (let i=0;i<query_string.length;i++){
        form.append(query_string[i], member_info[i]);
    }

    let url=url_mode["url_api_member_id"]+member_id;
    return await fetch(url, {
        method: "PATCH",
        body:form
    }).then(response => {
        return response.json();
    })
}

export async function get_all_member_info(member_id){
    let url=url_mode["url_api_member_id"]+member_id;
    return await fetch(url, {
        method:"POST",
        body:null
    }).then(response => {
        return response.json();
    })
}

export async function get_favorite_stock(member_id, stock_id){
    let url=url_mode["url_api_member_id"]+member_id+"/"+stock_id;
    return await fetch(url).then(response => {
        return response.json();
    })
}

export async function add_favorite_stock(member_id, stock_id){
    let url=url_mode["url_api_member_id"]+member_id+"/"+stock_id;
    return await fetch(url, {
        method:"POST",
        body:null
    }).then(response => {
        return response.json();
    })
}

export async function delete_favorite_stock(member_id, stock_id){
    let url=url_mode["url_api_member_id"]+member_id+"/"+stock_id;
    return await fetch(url, {
        method:"DELETE",
        body:null
    }).then(response => {
        return response.json();
    })
}

export async function add_price_notification(member_id, stock_id, price){
    let url=url_mode["url_api_member_id"]+member_id+"/"+stock_id;
    let form=new FormData();
    form.append("price", price);
    return await fetch(url, {
        method:"PATCH",
        body:form
    }).then(response => {
        return response.json();
    })
}