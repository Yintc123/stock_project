// let container_width=800;
// let container_height=400;

let container_width=document.querySelector("#container_candlestick_chart").clientWidth;
let container_height=document.querySelector("#container_candlestick_chart").clientHeight;
//-----------------------------------Function--------------------------------------
//--------------------------------畫面處理(V)-------------------------------//
function init_chart(mode){
    // create_chart_div();
    let chart = LightweightCharts.createChart(document.getElementById("container_candlestick_chart"), {
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
        let trend=data[i]["open"]-data[i]["close"]
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
//-------------------------------------export----------------------------------------
export function load_chart(mode, data){
    let chart = init_chart(mode);
    create_candlestick_chart(chart, data);
    create_volume_chart(chart, data);
    return chart;
}

export function add_sma(chart, data, period, color){
    let sma=create_sma(chart, data, period, color);
    return sma;
}
