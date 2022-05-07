console.log("hi");

import('./stock_module.js')
.then(func=>{
    func.get_stock();
})