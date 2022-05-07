const taiwan_stock_url="https://openapi.twse.com.tw/v1/exchangeReport/MI_INDEX4";

export async function get_stock(){
    return await fetch(taiwan_stock_url)
    .then(result => {
        console.log(result);
    })
}