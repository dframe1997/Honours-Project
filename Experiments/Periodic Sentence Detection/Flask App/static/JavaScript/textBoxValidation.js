submitButton = document.getElementById("submit");
textarea = document.getElementById("text");
textType = document.getElementById("textType");
$('#text').on('input propertychange', function() {
    checkLength();
});
$('#textType').on('input propertychange', function() {
    checkLength();
});
function checkLength(){
    console.log("Textarea length: " + textarea.value.length)
    if(textarea.value.length > 0 || textType.value == "Test"){
        submitButton.disabled = false;
    }
    else{
        submitButton.disabled = true;
    }
}