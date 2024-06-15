const axiosClass = require('axios');

class Servers{
    constructor(){
        this.servers = [
            "https://rubino1.iranlms.ir/", "https://rubino2.iranlms.ir/",
            "https://rubino3.iranlms.ir/", "https://rubino4.iranlms.ir/",
            "https://rubino5.iranlms.ir/", "https://rubino6.iranlms.ir/",
            "https://rubino7.iranlms.ir/", "https://rubino8.iranlms.ir/",
            "https://rubino9.iranlms.ir/", "https://rubino10.iranlms.ir/",
            "https://rubino11.iranlms.ir/", "https://rubino12.iranlms.ir/",
            "https://rubino13.iranlms.ir/", "https://rubino14.iranlms.ir/",
            "https://rubino15.iranlms.ir/", "https://rubino16.iranlms.ir/",
            "https://rubino17.iranlms.ir/", "https://rubino18.iranlms.ir/",
            "https://rubino19.iranlms.ir/", "https://rubino20.iranlms.ir/",
            "https://rubino21.iranlms.ir/", "https://rubino22.iranlms.ir/",
            "https://rubino23.iranlms.ir/", "https://rubino24.iranlms.ir/",
            "https://rubino25.iranlms.ir/", "https://rubino26.iranlms.ir/",
            "https://rubino27.iranlms.ir/", "https://rubino28.iranlms.ir/",
            "https://rubino29.iranlms.ir/", "https://rubino30.iranlms.ir/"
        ]
    }

    get newServer(){
        const rnd = Math.floor(Math.random() * this.servers.length);
        return this.servers[rnd];
    }
}

class Random{
    get getRandomNumber(){
        return Math.floor(Math.random() * 999999999) - 100000 
    }
}

class NetworkHandler{
    constructor(AuthToken,
                proxy){
                    this.auth = AuthToken
                    this.prx = proxy ? proxy : undefined || null;
                    this.axGet = new axiosClass.Axios("GET");
                    this.axPost = new axiosClass.Axios("POST");
                }

    create(method, params, callback = null){
        let json_data = {
            "api_version": "0",
            "auth": this.auth,
            "client":{
                "app_name": "Main",
                "app_version": "3.0.2",
                "lang_code": "fa",
                "package":"app.rbmain.a",
                "platform": "Android"

            },
            "data": JSON.parse(JSON.stringify(params)),
            "method": method
        }
        try{
            this.axPost.post(new Servers().newServer, JSON.stringify(json_data), {
                headers: {
                    'Content-Type': 'application/json',
                    'User-Agent': 'axios/1.7.2'
                },
                proxy: this.prx
            }).then((resp) => {
                if (callback === null){true;}else{
                    let data = JSON.parse(resp.data);
                    data.error = false;
                    data.base = null;
                    callback(data);
                }
            })
        }catch (Error){
            let data = JSON.parse(JSON.stringify({}));
            data.error = true;
            data.base = String(Error);
            if (callback === null){true;}else{
                callback(data);
            }
        }
    }
}

class StringBuilder{
    pathBuild(path){
        let pathx = String(path);
        if (pathx.includes("/")){
            return pathx.split("/")[pathx.split("/").length - 1];
        }else if (pathx.includes("\\")){
            return pathx.split("\\")[pathx.split("\\").length - 1]
        }else{
            return pathx
        }
    }
}

module.exports = {
    Servers,
    Random,
    NetworkHandler,
    StringBuilder
}