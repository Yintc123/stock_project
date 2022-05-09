console.log("hi");

import * as d3 from "https://cdn.skypack.dev/d3@7";

const div = d3.selectAll("div");

import('./stock_module.js')
.then(func=>{
    func.get_stock()
    .then(result=>{
        console.log(result);
    });
})

