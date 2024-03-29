const domain_name="yin888.info";
const ec2="3.115.234.130:5000";

const url={
    "dev":{
        "url_stock":"http://127.0.0.1:5000/",
        "url_member":"http://127.0.0.1:5000/member",
        "url_api_stock":"http://127.0.0.1:5000/api/stock/",
        "url_api_stocks_news":"http://127.0.0.1:5000/api/stocks/news",
        "url_api_member":"http://127.0.0.1:5000/api/member",
        "url_api_member_id":"http://127.0.0.1:5000/api/member/",
        "url_api_email":"http://127.0.0.1:5000/api/email",
        "url_api_message":"http://127.0.0.1:5000/api/message/",
        "url_api_subscription":"http://127.0.0.1:5000/api/subscription",
        "url_api_push":"http://127.0.0.1:5000/api/push",
    },
    "prod":{
        "url_stock":"https://"+domain_name+"/",
        "url_member":"https://"+domain_name+"/member",
        "url_api_stock":"https://"+domain_name+"/api/stock/",
        "url_api_stocks_news":"https://"+domain_name+"/api/stocks/news",
        "url_api_member":"https://"+domain_name+"/api/member",
        "url_api_member_id":"https://"+domain_name+"/api/member/",
        "url_api_email":"https://"+domain_name+"/api/email",
        "url_api_message":"https://"+domain_name+"/api/message/",
        "url_api_subscription":"https://"+domain_name+"/api/subscription",
        "url_api_push":"https://"+domain_name+"/api/push",
    }
};

const env="prod";
// const env="dev";

export const url_mode=url[env];
export default url_mode;