
let roomName = JSON.parse(document.getElementById('room-name').textContent);
let conversation=document.getElementById("conversation");
let sendButton = document.getElementById("sendMessage");
let inputField = document.getElementById("message-input-chat");
let chatSocket = "";  
var appointmentDuration = "";
var appointmentStartTime = 0;
let other_user=JSON.parse(document.getElementById('other_user').textContent);
let requestUserUsername=JSON.parse(document.getElementById('requestUserUsername').textContent);
let fileName="";
let chatScroll=document.getElementById("chatScroll");
let typeOfUser = JSON.parse(document.getElementById('typeOfUser').textContent);
document.getElementById("hiddenInput").addEventListener("change",handleFileSelect,false);
let otherUserPeerId="";
let typeCall="";
let requestUserSlug=JSON.parse(document.getElementById("requestUserSlug").textContent);
var sockets = [];

//call part assigne

let currentUserSlug = JSON.parse(document.getElementById('requestUserUsername').textContent);
let other_user_slug = JSON.parse(document.getElementById('other_user').textContent);
let otherUser=JSON.parse(document.getElementById('other_user_slug').textContent);
let otherUserFullName=document.getElementById('nameContent').textContent;
let chatPart=document.getElementById("chatPart");
let videoCallPart=document.getElementById("videoCallPart");
const baseURL = "/";
let callTypeOfAppointment="";
let remoteVideo = document.getElementById("video1");
let localVideo = document.getElementById("video2");

let camera = document.getElementById("camera");
let microfone = document.getElementById("microfone");
let microfone2 = document.getElementById("microfone2");

let isMicOpen = true;
let isCamOpen = true;
let otherCustomUser;

let remoteRTCMessage;
let iceCandidatesFromCaller = [];
let peerConnection;
let remoteStream;
let localStream;

let localAudio = document.querySelector('#localAudio'); 
let remoteAudio = document.querySelector('#remoteAudio'); 

let callInProgress = false;

var time=document.getElementById("timeDuration");

// peer.on("open", function (id) {
    
    // const csrf=document.getElementsByName("csrfmiddlewaretoken");
    // $.ajax({
    //     type: "POST",
    //     url: "/createPeerIdToUser",							
    //     data: {
    //       'peerId': id,
    //       'csrfmiddlewaretoken' : csrf[0].value,	
    //     },
        
    //   });

// });





// function videoCallUser(){
//     var slugName = document.getElementById('other_user_slug').textContent;
//     if(typeOfUser == "doctor"){
//         window.location="videoCall/"+slugName+"?side=caller";
//     }else{
//         window.location="videoCall/"+slugName;
//     }
    
// }






function handleFileSelect(){
    var file=document.getElementById("hiddenInput").files[0];
    fileName=file.name;
    var extension=fileName.split('.').pop();
    const fsize = file.size;
    const fileSize = Math.round((fsize / 1024));
    if (fileSize >= 10024) {
        alert(
          "Dosya çok büyük.Lütfen en fazla 10 mb büyüklüğünde dosya seçiniz");
    }else {
        const interestingItems = new Set(['doc','xls','xlsx','pdf','jpg','png','jpeg']);
        const isItemInSet = interestingItems.has(extension);
        if (isItemInSet==true){
            getBase64(file);
        }else{
            alert(
                "Yükleyeceğiniz dosya tipi 'doc','xls','xlsx','pdf','jpg','png','jpeg' bunlardan biri olmalıdır.");
        }
        
    }
    
}


function getBase64(file){
    var reader=new FileReader();
    reader.readAsDataURL(file);
    reader.onload=function (){
        chatSocket.send(JSON.stringify({
            'message': reader.result,
            "command": "new_message",
            "to":other_user,
            "roomName":roomName,
            "first_user":requestUserUsername,
            "what_is_it":"image",
            "fileName":fileName,
        }));
    }   
}






function callAjax(){
    $.ajax({
        type : "GET",
        url : "get_user/"+roomName,
        dataType: 'JSON',								
        data : {	
            
        },
        success : function(data) {
            document.getElementById('other_user_slug').textContent=data.slug;
            otherUserPeerId=data.otherUserPeerId;
            document.getElementById('nameContent').textContent=data.second_user_name;
            otherUser=data.slug;        //kontorl et
            otherUserFullName=data.otherUserFullName;
            appointmentDuration=data.appointmentDuration;
            appointmentStartTime=data.appointmentStartTime;
            document.getElementById('other_user_image').src=data.imageUrl;
            var status="";
            if(data.className == "avatar avatar-online"){
                status="online"
            }else if(data.className == "avatar avatar-offline"){
                status="offline"
            }
            $("#chat-header-part").html(`<a id="back_user_list" href="javascript:void(0)" class="back-user-list">
            <i class="material-icons">chevron_left</i>
        </a>
        <div class="media">
            <div class="media-img-wrap">
                <div class="${data.className}">
                    <img src="${data.image}" alt="User Image" class="avatar-img rounded-circle">
                </div>
            </div>
            <div class="media-body">
                <div class="user-name">${data.second_user_name}</div>
                <div class="user-status">${status}</div>
            </div>
        </div>
        <div class="chat-options">
            <a href="" onclick="call('voice');" data-toggle="modal" data-target="#video_call">
                <i class="material-icons">local_phone</i>
            </a>
            <a href="" onclick="call('video');" data-toggle="modal" id="videoCallButton" data-target="#video_call">
                <i class="material-icons">videocam</i>
            </a>
            
        </div>`)
             
        }
        
    });
 





};









window.onload=function(){
    connect();
    callAjax();
};

window.onunload = closingCode;
function closingCode(){
    chatSocket.send(JSON.stringify({"command":"closeSocket","roomName":roomName,"requested":requestUserUsername}));
}





// function updateclose(){
//     $.ajax({
//         type : "GET",
//         url : "updateOffline",
//         dataType: 'JSON',								
//         data : {	
            		        
//         },
//     });
// }

function connect(){
   
    chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );

    chatSocket.onopen=function (e){
        fetchMessages();
    };



function writeTyping(data){
    
    var elements=document.getElementsByName("typingMessage");
    var message=`<li name="typingMessage" class="media received">
        <div class="avatar">
            <img src="${data.data.image}" alt="User Image" class="avatar-img rounded-circle">
        </div>
        <div class="media-body">
            <div class="msg-box">
                <div>
                    <div class="msg-typing">
                        <span></span>
                        <span></span>
                        <span></span>   
                    </div>
                </div>
            </div>
        </div>
    </li>`
    if(elements.length==0){
        conversation.innerHTML+=message;
        chatScroll.scrollTop=chatScroll.scrollHeight;
    }
    
    
};


$("#message-input-chat").keypress(function() {
    if(document.getElementById("message-input-chat").value.length>0){
        chatSocket.send(JSON.stringify({"command":"typing","otherUser":otherUser,"requested":requestUserSlug})); 
    }
    else if(document.getElementById("message-input-chat").value.length==0){
        var elements=document.getElementsByName("typingMessage");
        for (var i = 0, len = elements.length; i < len; i++) {
            elements[i].remove();
        }
       
    }
});



chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    if (data["command"] === "messages" ){
        for(let i=0;data["messages"].length;i++){
            createMessage(data["messages"][i]);
        }
       
    }else if (data["command"] === "new_message" ){
        var elements=document.getElementsByName("typingMessage");
        for (var i = 0, len = elements.length; i < len; i++) {
            elements[i].remove();
        }
        createMessage(data["message"]);
        lastChatId=roomName+"lastChat";
        document.getElementById(lastChatId).textContent=data["message"]["content"];  //write last message
        lastMinute=roomName+"lastMinute";
        document.getElementById(lastMinute).textContent="0 dakika"  //write last message
        
    }else if (data["command"] === "call_received" ){
        onNewCall(data.data)    
    }else if (data["command"] === "call_answered" ){
        onCallAnswered(data.data);    
    }else if (data["command"] === "ICEcandidate" ){
        onICECandidate(data.data);    
    }else if (data["command"] === "callType" ){
        callTypeOfAppointment=data.data.callType;    
    }else if (data["command"] === "rejectCall" ){
        location.reload();
        // console.log("aramanız reddedildi reject call");
        // localStream.getTracks().forEach(track => track.stop());
        // document.getElementById("endCallButton").click();
        // callInProgress=false;
        // document.getElementById("chatPart").style.display = "block";
        // document.getElementById("videoCallPart").style.display = "none";
        // document.getElementById("voiceCallPart").style.display = "none";
    }else if (data["command"] === "typing" ){
        writeTyping(data);
    }
    
   
};


function createMessage(data){
    if(data["is_okey"] == "false"){
        location.reload();
    }
   
    var messageType=data["what_is_it"];
    if (messageType === "text"){
        messageX=data.content;
    }else if (messageType === "image"){
        messageX=`<div class="chat-msg-attachments">
        <div class="chat-attachment">
            <img src="${data.content}" alt="Attachment">
            <div class="chat-attach-caption">${data.fileName}</div>
            <a href="${data.content}" download="${data.fileName}" class="chat-attach-download">
                <i class="fas fa-download"></i>
            </a>
        </div>
    </div>`;
    }

    if (requestUserUsername == data["first_user"]){
        var message=`<li class="media sent">
        <div class="media-body">
            <div class="msg-box">
                <div>
                    <p>${messageX}</p>
                    <ul class="chat-msg-info">
                        <li>
                            <div class="chat-time">
                                <span>${data.created_date}</span>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </li>`
    }else{
        var message=`<li class="media received">
        <div class="avatar">
            <img src="${data.image}" alt="User Image" class="avatar-img rounded-circle">
        </div>
        <div class="media-body">
            <div class="msg-box">
                <div>
                   
                    <p>${messageX}</p>
                    <ul class="chat-msg-info">
                        <li>
                            <div class="chat-time">
                                <span>${data.created_date}</span>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </li>`
    }

    conversation.innerHTML+=message;
    chatScroll.scrollTop=chatScroll.scrollHeight;
}


chatSocket.onclose=function(e){
   
    console.error("Söket beklenmedik şekilde kapatıldı.");
    
};




inputField.focus();

inputField.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        sendButton.click();
    }
};


sendButton.onclick = function(e) {   
    var message = inputField.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        "command": "new_message",
        "to":other_user,
        "roomName":roomName,
        "first_user":requestUserUsername,
        "what_is_it":"text",
        "fileName":fileName
    }));
    inputField.value = '';
   
};



function fetchMessages(){
    chatSocket.send(JSON.stringify({"command":"fetch_messages","roomName":roomName,"name":requestUserSlug}));
};




const onNewCall = (data) => {
    //when other called you
    //show answer button
    otherUser = data.caller;
    otherUserFullName=data.otherUserFullName;
    remoteRTCMessage = data.rtcMessage;

    document.getElementById("comingRequestButton").click();
    document.getElementById("comingRequestName").textContent=otherUserFullName;
   
}


const onCallAnswered = (data) => {
    //when other accept our call
    chatSocket.send(JSON.stringify({"command":"defineStartTime"}));
    remoteRTCMessage = data.rtcMessage
    peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));
    document.getElementById("endCallButton").click();
    document.getElementById("chatPart").style.display = "none";
    if(callTypeOfAppointment=="video"){
        document.getElementById("videoCallPart").style.display = "block";
        document.getElementById("showName").textContent=otherUserFullName;
        time=document.getElementById("timeDuration");
        
    }else if(callTypeOfAppointment=="voice"){
        document.getElementById("voiceCallPart").style.display = "block";
        document.getElementById("showName2").textContent=otherUserFullName;
        document.getElementById("showName3").textContent=otherUserFullName;
        time=document.getElementById("timeDuration2");
    }
    
    setInterval(setTime, 1000);
    console.log("Call Started. They Answered accept");
    
    // console.log(pc);

    //callProgress();
    callInProgress=true;
} 



const onICECandidate = (data) =>{
    console.log("GOT ICE candidate");

    let message = data.rtcMessage;

    let candidate = new RTCIceCandidate({
        sdpMLineIndex: message.label,
        candidate: message.candidate
    });

    if (peerConnection) {
        console.log("ICE candidate Added");
        peerConnection.addIceCandidate(candidate);
    } else {
        console.log("ICE candidate Pushed");
        iceCandidatesFromCaller.push(candidate);
    }

}





}


function runChatUser(id,username){
    document.getElementById(roomName).className="media"
    $("#conversation").html("<p>"+"</p>");
    document.getElementById('room-name').textContent=id;
    other_user=username;
    roomName = id;
    document.getElementById(roomName).className="media read-chat active";
    chatSocket.close();
    connect();
    callAjax();
    

   
};








//call parts






//var appointmentStartTime = appointmentStartTime;
function setTime() {
    console.log("set time fonkdaaaaaaaaaaaaaa");
    ++appointmentStartTime;
    let seconds = pad(appointmentStartTime % 60);
    let minute = pad(parseInt(appointmentStartTime / 60));
    time.textContent=minute+":"+seconds;
    let difference=minute-appointmentDuration;
    if( difference==1){
        //location.href="/chat";
        sendRejectCall();
    }
  }
  function pad(val) {
    var valString = val + "";
    if (valString.length < 2) {
      return "0" + valString;
    } else {
      return valString;
    }
  }










    





  

//webrtc parts



function call(callType) {
    callTypeOfAppointment=callType;
    console.log(otherUser);
    chatSocket.send(JSON.stringify({
        "command": "defineType",
        "callType":callTypeOfAppointment,
        "otherUser":otherUser
    }));
    if(callType=="video"){
        beReady()
        .then(bool => {
            processCall(otherUser)
        })
    }else if(callType=="voice"){
        beReadyVoice()
        .then(bool => {
            processCall(otherUser)
        })
    }
}

//event from html
function answer() {
    //do the event firing
    //document.getElementById("comingRequestRed").click();
    document.getElementById("chatPart").style.display = "none";
    if(callTypeOfAppointment=="video"){
        document.getElementById("videoCallPart").style.display = "block";
        document.getElementById("showName").textContent=otherUserFullName;
        time=document.getElementById("timeDuration");
    }else if(callTypeOfAppointment=="voice"){
        document.getElementById("voiceCallPart").style.display = "block";
        document.getElementById("showName2").textContent=otherUserFullName;
        document.getElementById("showName3").textContent=otherUserFullName;
        time=document.getElementById("timeDuration2");
    }
    
    setInterval(setTime, 1000);
    $('.modal').modal('hide');
    if(callTypeOfAppointment=="video"){
        beReady()
        .then(bool => {
            processAccept();
        })
    }else if(callTypeOfAppointment=="voice"){
        beReadyVoice()
        .then(bool => {
            processAccept();
        })
    }
    

}

let pcConfig = {
    "iceServers":
        [
            { "url": "stun:stun.jap.bloggernepal.com:5349" },
            {
                "url": "turn:turn.jap.bloggernepal.com:5349",
                "username": "guest",
                "credential": "somepassword"
            },
            {"url": "stun:stun.l.google.com:19302"}
        ]
};











/**
 * 
 * @param {Object} data 
 * @param {number} data.name - the name of the user to call
 * @param {Object} data.rtcMessage - the rtc create offer object
 */
function sendCall(data) {
    //to send a call
    // socket.emit("call", data);
    chatSocket.send(JSON.stringify({
        "command": 'call',
        "data":data
    }));

    document.getElementById("chatPart").style.display = "none";
    if(callTypeOfAppointment=="video"){
        document.getElementById("videoCallPart").style.display = "block";
    }else if(callTypeOfAppointment=="voice"){
        document.getElementById("voiceCallPart").style.display = "block";
    }
   // document.getElementById("video2").srcObject = stream;
   // document.getElementById("video2").play();
}

/**
 * 
 * @param {Object} data 
 * @param {number} data.caller - the caller name
 * @param {Object} data.rtcMessage - answer rtc sessionDescription object
 */
function answerCall(data) {
    //to answer a call
    // socket.emit("answerCall", data);
    chatSocket.send(JSON.stringify({
        "command": 'answer_call',
        "data":data,
    }));
    //callProgress();
    callInProgress = true;
}


/**
 * 
 * @param {Object} data 
 * @param {number} data.user - the other user //either callee or caller 
 * @param {Object} data.rtcMessage - iceCandidate data 
 */
function sendICEcandidate(data) {
    //send only if we have caller, else no need to
    console.log("Send ICE candidate");
    // socket.emit("ICEcandidate", data)
    chatSocket.send(JSON.stringify({
        "command": 'ICEcandidate',
        "data":data
    }));

}





//WECRTC PARTS



function beReady() {
    return navigator.mediaDevices.getUserMedia({
        audio: true,
        video: true
    })
        .then(stream => {
            localStream = stream;
            localVideo.srcObject = stream;
            return createConnectionAndAddStream()
        })
        .catch(function (e) {
            alert('getUserMedia() error: ' + e.name);
        });
}


function beReadyVoice() {
    return navigator.mediaDevices.getUserMedia({
        audio: true,
        video: false
    })
        .then(stream => {
            localStream = stream;
            localAudio.src=stream;
            return createConnectionAndAddStream()
        })
        .catch(function (e) {
            alert('getUserMedia() error: ' + e.name);
        });
}



function createConnectionAndAddStream() {
    createPeerConnection();
    peerConnection.addStream(localStream);
    return true;
}

function processCall(userName) {
    peerConnection.createOffer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);
        sendCall({
            "name": userName,
            "otherUserFullName":JSON.parse(document.getElementById('requestUserFullName').textContent),
            "rtcMessage": sessionDescription
        })
    }, (error) => {
        console.log("Error");
    });
}

function processAccept() {

    peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));
    peerConnection.createAnswer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);

        if (iceCandidatesFromCaller.length > 0) {
            //I am having issues with call not being processed in real world (internet, not local)
            //so I will push iceCandidates I received after the call arrived, push it and, once we accept
            //add it as ice candidate
            //if the offer rtc message contains all thes ICE candidates we can ingore this.
            for (let i = 0; i < iceCandidatesFromCaller.length; i++) {
                //
                let candidate = iceCandidatesFromCaller[i];
                console.log("ICE candidate Added From queue");
                try {
                    peerConnection.addIceCandidate(candidate).then(done => {
                        console.log(done);
                    }).catch(error => {
                        console.log(error);
                    })
                } catch (error) {
                    console.log(error);
                }
            }
            iceCandidatesFromCaller = [];
            console.log("ICE candidate queue cleared");
        } else {
            console.log("NO Ice candidate in queue");
        }

        answerCall({
            "caller": otherUser,
            "otherUserFullName":otherUserFullName,
            "rtcMessage": sessionDescription
        })

    }, (error) => {
        console.log("Error");
    })
}

/////////////////////////////////////////////////////////

function createPeerConnection() {
    try {

        peerConnection = new RTCPeerConnection(pcConfig);
        // peerConnection = new RTCPeerConnection();
        peerConnection.onicecandidate = handleIceCandidate;
        peerConnection.onaddstream = handleRemoteStreamAdded;
        peerConnection.onremovestream = handleRemoteStreamRemoved;
        // peerConnection.on('close', function (){
        //     console.log("aramanız karşı taraften reddedildi");
        // })
        console.log('Created RTCPeerConnnection');
        return;
    } catch (e) {
        console.log('Failed to create PeerConnection, exception: ' + e.message);
        alert('Cannot create RTCPeerConnection object.');
        return;
    }
}

function handleIceCandidate(event) {
    // console.log('icecandidate event: ', event);
    if (event.candidate) {
        console.log("Local ICE candidate");
        // console.log(event.candidate.candidate);

        sendICEcandidate({
            "user": otherUser,
            "otherUserFullName":otherUserFullName,
            "rtcMessage": {
                "label": event.candidate.sdpMLineIndex,
                "id": event.candidate.sdpMid,
                "candidate": event.candidate.candidate
            }
        })

    } else {
        console.log('End of candidates.');
    }
}

function handleRemoteStreamAdded(event) {
    console.log('Remote stream added.');
    remoteStream = event.stream;
    if(callTypeOfAppointment=="video"){
        remoteVideo.srcObject = remoteStream;
    }else if(callTypeOfAppointment=="voice"){
        remoteAudio.srcObject=remoteStream;
    }
    
}

function handleRemoteStreamRemoved(event) {
    console.log('Remote stream removed. Event: ', event);
    remoteVideo.srcObject = null;
    localVideo.srcObject = null;
}


window.onbeforeunload = function () {
    if (callInProgress) {
        stop();
        
    }
};

function stop(){
    localStream.getTracks().forEach(track => track.stop());
    callInProgress=false;
    peerConnection.close();
    peerConnection=null;
    document.getElementById("chatPart").display="block";
    document.getElementById("videoCallPart").display="none";
    document.getElementById("voiceCallPart").display="none";
    otherUser=null;

}

function sendRejectCall(){
    chatSocket.send(JSON.stringify({
        "command": 'rejectCall',
    }));
}




function callProgress(){
    document.getElementById("endCallButton").click();
    document.getElementById("chatPart").display="none";
    if(callTypeOfAppointment=="video"){
        document.getElementById("videoCallPart").style.display = "block";
    }else if(callTypeOfAppointment=="voice"){
        document.getElementById("voiceCallPart").style.display = "block";
    }
    callInProgress=true;
    
}




camera.addEventListener("click",evt=>{
    if(isCamOpen){
        localStream.getVideoTracks()[0].enabled=false
        isCamOpen=false
        camera.style="color:red;"
        camera.title="Kameranı Aç"
    }else{
        localStream.getVideoTracks()[0].enabled=true
        isCamOpen=true
        camera.style="color:green;"
        camera.title="Kameranı Kapat"

    }
})

microfone.addEventListener("click",evt=>{
    if(isMicOpen){
        localStream.getAudioTracks()[0].enabled=false
        isMicOpen=false
        microfone.style="color:red;"
        microfone.title="Mikrofonu Aç"
    }else{
        localStream.getAudioTracks()[0].enabled=true
        isMicOpen=true
        microfone.style="color:green;"
        microfone.title="Mikrofonu Kapat"

    }
})



microfone2.addEventListener("click",evt=>{
    if(isMicOpen){
        localStream.getAudioTracks()[0].enabled=false;
        isMicOpen=false;
        document.getElementById("hideSlash").style.display="block";
        microfone2.style="color:red;";
        microfone2.title="Mikrofonu Aç";
    }else{
        localStream.getAudioTracks()[0].enabled=true
        isMicOpen=true;
        document.getElementById("hideSlash").style.display="none";
        microfone2.style="color:green;"
        microfone2.title="Mikrofonu Kapat";

    }
})