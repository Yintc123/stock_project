const container_chart=document.querySelector("#container_chart");

let container_width=container_chart.clientWidth*0.95;
let container_height=container_chart.clientHeight;
//-----------------------------------Function--------------------------------------
//--------------------------------畫面處理(V)-------------------------------//
function init_chart(mode){
    let chart = LightweightCharts.createChart(container_chart, {
        width: container_width,
        height: container_height,
        layout: {
            backgroundColor: '#000',
            textColor: 'rgba(255, 255, 255, 0.9)',
        },
        grid: {
            vertLines: {
                color: 'rgba(197, 203, 206, 0.5)',
            },
            horzLines: {
                color: 'rgba(197, 203, 206, 0.5)',
            },
        },
        crosshair: {
            mode: LightweightCharts.CrosshairMode[mode],
        },
        rightPriceScale: {
            borderColor: 'rgba(197, 203, 206, 0.8)',
        },
        timeScale: {
            borderColor: 'rgba(197, 203, 206, 0.8)',
        },
    });
    return chart;
}

function create_candlestick_chart(chart, data){
    let candleSeries = chart.addCandlestickSeries({
      upColor: 'rgba(255,82,82, 1)',
      downColor: 'rgba(0, 150, 136, 1)',
      borderDownColor: 'rgba(0, 150, 136, 1)',
      borderUpColor: 'rgba(255,82,82, 1)',
      wickDownColor: 'rgba(0, 150, 136, 1)',
      wickUpColor: 'rgba(255,82,82, 1)',
    });
    
    candleSeries.setData(data);
}

function create_volume_chart(chart, data){
    let volumeSeries = chart.addHistogramSeries({
        color: '#26a69a',
        priceFormat: {
            type: 'volume',
        },
        priceScaleId: '',
        scaleMargins: {
            top: 0.8,
            bottom: 0,
        },
    });
    const newdata=translate_to_volume_data(data);
    volumeSeries.setData(newdata);
}

function create_index_chart(chart, data){
    const result=judge_trends(data);
    let color={
        "increase":"255,82,82",
        "decrease":"38,198,218",
        "equal":"255, 255, 255"
    };
    let areaSeries = chart.addAreaSeries({
        topColor: 'rgba('+color[result]+', 0.56)',
        bottomColor: 'rgba('+color[result]+', 0.04)',
        lineColor: 'rgba('+color[result]+', 1)',
        lineWidth: 2,
    });
    let new_data=translate_to_value_data(data);
    areaSeries.setData(new_data);
}

function create_sma(chart, data, period, color){
    let smaData = calculate_sma(data, period);
    let smaLine = chart.addLineSeries({
        color: color,
        lineWidth: 2,
    });
    smaLine.setData(smaData);
    return smaLine;
}

//--------------------------------處理data(M)-------------------------------//
function translate_to_volume_data(data){
    let new_data=[];
    for(let i=0;i<data.length;i++){
        let temp={};
        let trend=data[i]["open"]-data[i]["close"];
        temp["time"]=data[i]["time"];
        temp["value"]=data[i]["Trading_Volume"];
        if (trend<0){
            temp["color"]="rgba(0, 150, 136, 0.6)";//股價跌，綠色
        }else if(trend>0){
            temp["color"]="rgba(255,82,82, 0.6)";//股價漲，紅色
        }else{
            temp["color"]="rgba(255,255,255, 0.6)";//平盤，白色
        }
        new_data.push(temp);
    }
    return new_data;
}

function translate_to_value_data(data){
    let new_data=[];
    for (let i=0;i<data.length;i++){
        let temp={
            "time":null,
            "value":null
        }
        temp["time"]=data[i]["time"];
        temp["value"]=data[i]["close"];
        new_data.push(temp);
    }
    return new_data;
}

function calculate_sma(data, period){
    let sma_data=[];
    for(let i=period-1;i<data.length;i++){
        let temp={};
        temp["time"]=data[i]["time"];
        temp["value"]=calculate_avg(data.slice(i-period+1, i+1)).toFixed(2);
        sma_data.push(temp);
    }
    return sma_data;
}

function calculate_avg(data){
    let sum=0;
    for (let i=0;i<data.length;i++){
        sum+=data[i]["close"];
    }
    return sum/data.length;
}

function judge_trends(data){
    let result=data[data.length-1]["spread"];
    if(result>0){
        return "increase";
    }else if(result<0){
        return "decrease";
    }else{
        return "equal";
    }
}
//-------------------------------------export----------------------------------------
export function load_chart(mode, data, chart_type){
    let chart = init_chart(mode);
    // const charts={
    //     "candlestick":create_candlestick_chart(chart, data),
    //     "index":create_index_chart(chart, data)
    // }
    if (chart_type=="candlestick"){
        create_candlestick_chart(chart, data);
    }else if(chart_type=="index"){
        create_index_chart(chart, data);
    }
    create_volume_chart(chart, data);
    return chart;
}

export function add_sma(chart, data, period, color){
    let sma=create_sma(chart, data, period, color);
    return sma;
}
