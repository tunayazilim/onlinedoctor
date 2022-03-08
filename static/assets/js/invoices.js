


// var detayKismi=document.getElementById("appt_details");


// function changeInformation(pk){
//     //console.log(pk)
//    // detayKismi.html("");
   

//    $.ajax({
//     type : "POST",
//     url : 'randevuDetayi/'+pk,			
//     dataType: 'JSON',								
//     data : {
//         'csrfmiddlewaretoken' : '{{  csrf_token  }}',								
//         'pk' : pk,
        
//     },
//     success : function(data) {
//         console.log(data);
//         console.log("başarılı")
        
//         var message=`<div class="modal-dialog modal-dialog-centered">
//     <div class="modal-content">
//         <div class="modal-header">
//             <h5 class="modal-title">Appointment Details</h5>
//             <button type="button" class="close" data-dismiss="modal" aria-label="Close">
//                 <span aria-hidden="true">&times;</span>
//             </button>
//         </div>
//         <div class="modal-body">
//             <ul class="info-details">
//                 <li>
//                     <div class="details-header">
//                         <div class="row">
//                             <div class="col-md-6">
//                                 <span class="title">#APT${data.schedule.pk}</span>
//                                 <span class="text">21 Oct 2019 10:00 AM</span>
//                             </div>
//                             <div class="col-md-6">
//                                 <div class="text-right">
//                                     <button type="button" class="btn bg-success-light btn-sm" id="topup_status">Completed</button>
//                                 </div>
//                             </div>
//                         </div>
//                     </div>
//                 </li>
//                 <li>
//                     <span class="title">Status:</span>
//                     <span class="text">Completed</span>
//                 </li>
//                 <li>
//                     <span class="title">Confirm Date:</span>
//                     <span class="text">29 Jun 2019</span>
//                 </li>
//                 <li>
//                     <span class="title">Paid Amount</span>
//                     <span class="text">$450</span>
//                 </li>
//             </ul>
//         </div>
//     </div>
// </div>`
// detayKismi.innerHTML=message;
            
//     }
    
// });


    

// }