const domain_name="stock.yin888.info";
const ec2="3.115.234.130:5000";

const url={
    "dev":{
        "url_stock":"http://127.0.0.1:5000/",
        "url_api_stock":"http://127.0.0.1:5000/api/stock/",
        "url_api_stocks_news":"http://127.0.0.1:5000/api/stocks/news",
    },
    "prod":{
        "url_stock":"http://"+domain_name+"/",
        "url_api_stock":"http://"+domain_name+"/api/stock/",
        "url_api_stocks_news":"http://"+domain_name+"/api/stocks/news",
    }
};

const env="prod";
// const env="prod";

export const url_mode=url[env];
export default url_mode;