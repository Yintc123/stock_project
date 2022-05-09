const url={
    "dev":{
        "url_api_stock":"http://127.0.0.1:5000/api/stock"
    },
    "prod":{
        "url_api_stock":"http://3.115.234.130:5000/api/stock"
    }
};

const env="dev";
// const env="prod";

export const url_mode=url[env];
export default url_mode;