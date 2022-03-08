"use strict";


let otherUser=JSON.parse(document.getElementById('other_user_slug').textContent);
let chatPart=document.getElementById("chatPart");
let videoCallPart=document.getElementById("videoCallPart");
const baseURL = "/";

let remoteVideo = document.getElementById("video1");
let localVideo = document.getElementById("video2");

let camera = document.getElementById("camera");
let microfone = document.getElementById("microfone");


let isMicOpen = true;
let isCamOpen = true;
let otherCustomUser;

let remoteRTCMessage;
let iceCandidatesFromCaller = [];
let peerConnection;
let remoteStream;
let localStream;
let requestUserSlug;


let callInProgress = false;



function call() {
    for (let index = 0; index < sockets.length; index++) {
        const element = sockets[index];
        element.close();
        console.log("kapandı..");
    }

    //console.log(other_user);
    beReady()
                .then(bool => {
                    processCall(otherUser);
                })

}

function answer() {
    //console.log(other_user);
    beReady()
        .then(bool => {
            processAccept();
        })


}

let pcConfig = {
    "iceServers":
        [
            { "url": "stun:stun.jap.bloggernepal.com:5349" },
            {
                "url": "turn:turn.jap.bloggernepal.com:5349",
                "username": "guest",
                "credential": "somepassword"
            }
        ]
};

// Set up audio and video regardless of what devices are present.
let sdpConstraints = {
    offerToReceiveAudio: true,
    offerToReceiveVideo: true
};


let socket;
let callSocket;
function connectSocket() {
    requestUserSlug=JSON.parse(document.getElementById("requestUserSlug").textContent);
  

    callSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/call/'
    );

    callSocket.onopen = event => {
        //let's send myName to the socket
        callSocket.send(JSON.stringify({
            type: 'login',
            data: {
                name: requestUserSlug
            }
        }));
    }

    callSocket.onmessage = (e) => {
        let response = JSON.parse(e.data);

        // console.log(response);

        let type = response.type;

        if (type == 'connection') {
            console.log(response.data.message)
        }

        if (type == 'call_received') {
            // console.log(response);
            onNewCall(response.data)
        }

        if (type == 'call_answered') {
            onCallAnswered(response.data);
        }

        if (type == 'ICEcandidate') {
            onICECandidate(response.data);
        }
    }

    const onNewCall = (data) => {
        //when other called you
        //show answer button

        otherUser = data.caller;
        remoteRTCMessage = data.rtcMessage;
       
    }

    const onCallAnswered = (data) => {
        //when other accept our call
        remoteRTCMessage = data.rtcMessage
        peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));

        console.log("Call Started. They Answered");
        for (let index = 0; index < sockets.length; index++) {
            const element = sockets[index];
            element.close();
            console.log("closed..");
        }
        // console.log(pc);

        callProgress();
    }   

    const onICECandidate = (data) => {
        // console.log(data);
        console.log("GOT ICE candidate");

        let message = data.rtcMessage

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



/**
 * 
 * @param {Object} data 
 * @param {number} data.name - the name of the user to call
 * @param {Object} data.rtcMessage - the rtc create offer object
 */
function sendCall(data) {
    //to send a call
    console.log("Send Call");

    // socket.emit("call", data);
    callSocket.send(JSON.stringify({
        type: 'call',
        data
    }));

    //   document.getElementById("call").style.display = "none";
    //   // document.getElementById("profileImageCA").src = baseURL + otherUserProfile.image;
    //   document.getElementById("otherUserNameCA").innerHTML = otherUser;
    //   document.getElementById("calling").style.display = "block";
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
    callSocket.send(JSON.stringify({
        type: 'answer_call',
        data
    }));
    callProgress();
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
    callSocket.send(JSON.stringify({
        type: 'ICEcandidate',
        data
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

function createConnectionAndAddStream() {
    createPeerConnection();
    peerConnection.addStream(localStream);
    return true;
}

function processCall(userName) {
    peerConnection.createOffer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);
        sendCall({
            name: userName,
            rtcMessage: sessionDescription
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
            caller: otherUser,
            rtcMessage: sessionDescription
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
            user: otherUser,
            rtcMessage: {
                label: event.candidate.sdpMLineIndex,
                id: event.candidate.sdpMid,
                candidate: event.candidate.candidate
            }
        })

    } else {
        console.log('End of candidates.');
    }
}

function handleRemoteStreamAdded(event) {
    console.log('Remote stream added.');
    remoteStream = event.stream;
    remoteVideo.srcObject = remoteStream;
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
    document.getElementById("answer").style.display = "none";
    document.getElementById("chatPart").display="block";
    document.getElementById("videoCallPart").display="none";
    otherUser=null;

}


function callProgress(){
    document.getElementById("endCallButton").click();
    chatPart.display="none";
    videoCallPart.display="block";

    callInProgress=true;

}