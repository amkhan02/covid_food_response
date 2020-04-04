$(document).ready(function() {
    $('#test-form').bootstrapValidator({
        //submitButtons: '#postForm',
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },        
        fields: {
            Name: {
             message: 'The first name is not valid',
                validators: {
                    notEmpty: {
                        message: 'The first name is required and cannot be empty'
                    },
                    stringLength: {
                        min: 1,
                        max: 30,
                        message: 'The first name must be more than 1 and less than 30 characters long'
                    }/*,
                    regexp: {
                        regexp: /^[A-z]+$/,
                        message: 'The first name can only accept alphabetical input'
                    },*/
                }
            },
            "Street Address": {
                message: 'Address is not valid',
                validators: {
                    notEmpty: {
                        message: 'Address is required and cannot be empty'
                    }
                }
            },
			"Zip code": {
                message: 'Zip code is not valid',
                validators: {
                    notEmpty: {
                        message: 'Zip code is required and cannot be empty'
                    },
					between: {
						inclusive: true,
						min: 29400,
						max: 29500,
						message: 'Please enter a Charleston area Zip Code'
					}
                }
            },
			"Phone Number": {
                message: 'Phone number is not valid',
                validators: {
                    notEmpty: {
                        message: 'Phone number is required and cannot be empty'
                    },
					regexp: {
                        regexp: /^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/,
                        message: 'Please enter a valid phone number'
                    }
                }
            },
            "Email (optional)": {
                validators: {
                    emailAddress: {
                        message: 'The email address is not valid'
                    }
                }
            },
             

        }
    })
    .on('success.form.bv', function(e) {
        // Prevent form submission
        e.preventDefault();

        // Get the form instance
        var $form = $(e.target);

        // Get the BootstrapValidator instance
        var bv = $form.data('bootstrapValidator');

        // Use Ajax to submit form data
        var url = 'https://script.google.com/macros/s/AKfycbwR2oJeXmuD4hI4QUKr8QE-dZIInYmzsXRJH422DhJBJFlWEgY/exec';
        var redirectUrl = '#';
        // show the loading 
        $('#postForm').prepend($('<span></span>').addClass('glyphicon glyphicon-refresh glyphicon-refresh-animate'));
        var jqxhr = $.get(url, $form.serialize(), function(data) {
            console.log("Success! Data: " + data.statusText);
            $(location).attr('href',redirectUrl);
        })
            .fail(function(data) {
                console.warn("Error! Data: " + data.statusText);
                // HACK - check if browser is Safari - and redirect even if fail b/c we know the form submits.
                if (navigator.userAgent.search("Safari") >= 0 && navigator.userAgent.search("Chrome") < 0) {
                    //alert("Browser is Safari -- we get an error, but the form still submits -- continue.");
                    $(location).attr('href',redirectUrl);                
                }
            });
		
		url = 'http://127.0.0.1:5000/'
		var jqxhr2 = $.post(url, $form.serialize(), function(data) {
            console.log("Success! Data: " + data.statusText);
            $(location).attr('href',redirectUrl);
        })
            .fail(function(data) {
                console.warn("Error! Data: " + data.statusText);
                // HACK - check if browser is Safari - and redirect even if fail b/c we know the form submits.
                if (navigator.userAgent.search("Safari") >= 0 && navigator.userAgent.search("Chrome") < 0) {
                    //alert("Browser is Safari -- we get an error, but the form still submits -- continue.");
                    $(location).attr('href',redirectUrl);                
                }
            });
    });
});

function addHouseMembers(that){
	var large = document.getElementById("family-info");
	var family = document.getElementById("family-input-container");
	while(family.hasChildNodes()){
		family.removeChild(family.lastChild);
	}
	for(var i = 1; i < that.value; i++){
		family.appendChild(document.createTextNode("Family Member " + (i+1)));
		family.appendChild(document.createElement("br"));
		
		//name
		family.appendChild(document.createTextNode("Name: " ));
		var input = document.createElement("input");
		input.type = "text";
		input.name = "member" + i + "_name";
		family.appendChild(input);
		family.appendChild(document.createElement("br"));
		
		//date of birth
		family.appendChild(document.createTextNode("Date of Birth: " ));
		input = document.createElement("input");
		input.type = "date";
		input.name = "member" + i + "_dob";
		family.appendChild(input);
		family.appendChild(document.createElement("br"));
		
		//relationship
		family.appendChild(document.createTextNode("Relationship: " ));
		input = document.createElement("input");
		input.type = "text";
		input.name = "member" + i + "_relationship";
		family.appendChild(input);
		family.appendChild(document.createElement("br"));
		
		//race
		family.appendChild(document.createTextNode("Race: " ));
		var selection = document.createElement("select");
		var options = [];
		
		for(var ii = 0; ii < 6; ii++){
			options.push(document.createElement("option"));
		}
		options[0].text = "Black (Not of Hispanic Origin)"; 
		options[0].name = "black";
		
		options[1].text = "White (Not of Hispanic Origin)";
		options[1].name = "white";
		
		options[2].text = "Asian";
		options[2].name = "asian";
		
		options[3].text = "Hispanic";
		options[3].name = "hispanic";
		
		options[4].text = "American Indian/Alaskan Native";
		options[4].name = "native-american";
		
		options[5].text = "Native Hawaiian/Pacific Islander";
		options[5].name = "pacific-islander";
		
		for(var ii = 0; ii < options.length; ii++){
			selection.appendChild(options[ii]);
		}
		
		selection.name = "member" + i + "_race";
		family.appendChild(selection);
		family.appendChild(document.createElement("br"));
		
		//gender
		family.appendChild(document.createTextNode("Race: " ));
		selection = document.createElement("select");
		options = [];
		
		for(var ii = 0; ii < 2; ii++){
			options.push(document.createElement("option"));
		}
		options[0].text = "Male"; 
		options[0].name = "Male";
		
		options[1].text = "Female";
		options[1].name = "Female";
		
		for(var ii = 0; ii < options.length; ii++){
			selection.appendChild(options[ii]);
		}
		
		selection.name = "member" + i + "_gender";
		family.appendChild(selection);
		family.appendChild(document.createElement("br"));
		family.appendChild(document.createElement("br"));
	}
}
