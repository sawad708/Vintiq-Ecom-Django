// // $(document).ready(function () {

// //     $('#payWithRazorpay').click(function (e) {
// //         e.preventDefault();

// //         var address = $("[name='selected_address']:checked").val(); // Get the selected address
																			
// // 		if (!address) {
// // 			alert("Please select an address.");
// // 			return;
// // 		}
// //         else
// //         {
            

// //             $.ajax({
// //                 method : "GET",
// //                 url : "http://127.0.0.1:8000/orders/place_order_razorpay/",
// //                 data: {'address':options.notes.address, csrfmiddlewaretoken: options.token},

// // 			    success: function (responsec) {
// // 					alert(responsec.order)
																	
																								
// // 					window.location.href = `http://127.0.0.1:8000/orders/place_order/${responsec.order}`

// //                 }
// //             })


// //             var options = {
// //                 "key": "rzp_test_NeEG40WVR5k4Of", // Enter the Key ID generated from the Dashboard
// //                 "amount": "response.toatal_price", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
// //                 "currency": "INR",
// //                 "name": "Vintiq", //your business name
// //                 "description": "Thank you",
// //                 "image": "https://example.com/your_logo",
// //                 "order_id": "{{ payment.id }}", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
// //                 "handler": function (response){
// //                     alert(response.razorpay_payment_id);
// //                     alert(response.razorpay_order_id);
// //                     alert(response.razorpay_signature)
// //                 },
// //                 "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
// //                     "name": "Gaurav Kumar", //your customer's name
// //                     "email": "gaurav.kumar@example.com", 
// //                     "contact": "9000090000"  //Provide the customer's phone number for better conversion rates 
// //                 },
// //                 "notes": {
// //                     "address": "Razorpay Corporate Office"
// //                 },
// //                 "theme": {
// //                     "color": "#3399cc"
// //                 }

// //             };
// //             var token = $("[name='csrfmiddlewaretoken']").val();
// // 			console.log(address, 'from event handler');
																			
// // 			// Update the 'address' property in the 'options' object
// // 			options.notes.address = address;
// // 		    options.token = token  
// //             var rzp1 = new Razorpay(options);
// //             rzp1.on('payment.failed', function (response){
// //                     alert(response.error.code);
// //                     alert(response.error.description);
// //                     alert(response.error.source);
// //                     alert(response.error.step);
// //                     alert(response.error.reason);
// //                     alert(response.error.metadata.order_id);
// //                     alert(response.error.metadata.payment_id);
// //             });
// //             rzp1.open();

// //         };
// //     });
// // });

// $(document).ready(function () {
//     $('#payWithRazorpay').click(function (e) {
//         e.preventDefault();

//         var address = $("[name='selected_address']:checked").val(); // Get the selected address
//         if (!address) {
//             alert("Please select an address.");
//             return;
//         } else {
//             // var paymentId = "{{ order.payment.id }}";
//             var options = {
//                 "key": "rzp_test_NeEG40WVR5k4Of", // Enter the Key ID generated from the Dashboard
//                 "amount": 50000, // Replace with the actual order amount
//                 "currency": "INR",
                
//                 "name": "Vintiq", // your business name
//                 "description": "Thank you",
//                 "image": "https://example.com/your_logo",
//                 "order_id": "{{ payment.id }}", // This is a sample Order ID. Pass the `id` obtained in the response of Step 1
//                 "handler": function (response) {
//                     alert(response.razorpay_payment_id);
//                     alert(response.razorpay_order_id);
//                     alert(response.razorpay_signature);
//                 },
//                 "prefill": {
//                     "name": "Gaurav Kumar", // your customer's name
//                     "email": "gaurav.kumar@example.com",
//                     "contact": "9000090000" // Provide the customer's phone number for better conversion rates
//                 },
//                 "notes": {
//                     "address": "Razorpay Corporate Office"
//                 },
//                 "theme": {
//                     "color": "#3399cc"
//                 }
//             };

//             var token = $("[name='csrfmiddlewaretoken']").val();
//             console.log(address, 'from event handler');

//             // Update the 'address' property in the 'options' object
//             options.notes.address = address;
//             options.token = token;
            
//             $.ajax({
//                 method: "GET",
//                 url: "http://127.0.0.1:8000/orders/place_order_razorpay/",
//                 data: { 'address': options.notes.address, csrfmiddlewaretoken: options.token },

//                 success: function (responsec) {
//                     alert(responsec.order);

//                     window.location.href = `http://127.0.0.1:8000/orders/place_order/${responsec.order}`;
//                 }
//             });

//             var rzp1 = new Razorpay(options);
//             rzp1.on('payment.failed', function (response) {
//                 alert(response.error.code);
//                 alert(response.error.description);
//                 alert(response.error.source);
//                 alert(response.error.step);
//                 alert(response.error.reason);
//                 alert(response.error.metadata.order_id);
//                 alert(response.error.metadata.payment_id);
//             });
//             rzp1.open();
//         }
//     });
// });
