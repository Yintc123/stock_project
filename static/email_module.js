import {url_mode} from './package.js'

export async function get_verification(email){
    let form=new FormData();
    form.append("email", email)
    return await fetch(url_mode["url_api_email"], {
        method:"POST",
        body:form
    }).then(response => {
        return response.json();
    })
}