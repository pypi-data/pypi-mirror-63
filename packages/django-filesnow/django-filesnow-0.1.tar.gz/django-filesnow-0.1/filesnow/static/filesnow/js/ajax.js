// Ajax to post request to django FilesNow app

let fetchSearchBtn = document.getElementById('SearchBtn')
//  Orignal
//  fetchSearchBtn.addEventListener('click', fetchSearchBtnHandler);

// Created to call more then one functions at the same time.
fetchSearchBtn.addEventListener('click',() => { fetchSearchBtnHandler()
});

function deleteBannerStart(){
    document.getElementById("deltLogo").innerHTML = '<span class="spinner-border text-danger"></span>'
    document.getElementById("deltMsg").innerHTML = '<span style="color: white;"> File will be deleted in one minute</span>'

}

function deleteBannerEnd(){
    document.getElementById("deltLogo").innerHTML = ''
    document.getElementById("deltMsg").innerHTML = ''
    document.getElementById("emptyTofill").innerHTML = '<button class="btn btn-danger" type="submit" id="SearchBtn">File Deleted</button>'

    const deltReq = new XMLHttpRequest();
    var delte_url = '/filesnow/delete?Sstring='+inputVal;

    deltReq.open('POST', delte_url, true);
    deltReq.onload = function(){
            console.log(this.response)
    }
    deltReq.send();

}

function fetchSearchBtnHandler() {
    inputVal = document.getElementById("fill").value;
    var site_href = window.location.host
    var site_protocol = window.location.protocol

    const searchReq = new XMLHttpRequest();
    var search_url = '/filesnow/saveme?Sstring='+inputVal+'&url='+site_href+'&proto='+site_protocol;
    searchReq.open('POST', search_url, true);
    
    searchReq.onload = function(){

        if (this.status === 200) {

            var onloadResponse = this.responseText

            if (onloadResponse == 4) {
                document.getElementById("emptyTofill").innerHTML = '<button class="btn btn-warning" type="submit" id="SearchBtn">No Such File</button>'
                document.getElementById('SearchBtn').innerHTML = "Search Again";
        }   else if (onloadResponse == 5){
                document.getElementById("emptyTofill").innerHTML = '<button class="btn btn-danger" type="submit" id="SearchBtn">Internal Server Error! Contact Admin</button>'
                document.getElementById('SearchBtn').innerHTML = "Search Again";
        }   else {
                document.getElementById("emptyTofill").innerHTML = '<button class="btn btn-success" type="submit" id="SearchBtn"><a style="color:white" href='+onloadResponse+'><i class="fa fa-download" aria-hidden="true"></i>  Download</a></button>'
                document.getElementById('SearchBtn').innerHTML = "Search Again"

                deleteBannerStart()
                setTimeout(deleteBannerEnd, 30000)
        }
        
    }
        else {
            console.log("Something went wrong")
        }
	 
    }
    
    searchReq.onprogress = function (){
        document.getElementById("SearchBtn").innerHTML = '<span>searching </span><span class="spinner-border spinner-border-sm"></span>'

    }

    searchReq.send();
}

