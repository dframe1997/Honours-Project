//Drag and drop
var dragHandler = function(evt){
    evt.preventDefault();
    document.getElementById('text').style = "background: rgba(255,255,255,0.5); border: 2px dashed black";
};

var outHandler = function(evt){
    evt.preventDefault();
    document.getElementById('text').style = "background: rgba(255,255,255,1); border: 0";
};

var dropHandler = function(evt){
    evt.preventDefault();
    var files = evt.originalEvent.dataTransfer.files;

    reader = new FileReader();

    try{
        // Read file as text    
        reader.readAsText(files[0], "UTF-8");

        //Runs once the reader has loaded
        reader.onload = function(e) {
            fileText = e.target.result
            document.getElementById('text').value = fileText;    
            checkLength(); 
        };
    }
    catch(exception){
        document.getElementById('text').value = "Error: Unsupported file type. Please drag a text (.txt) file."; 
    }

    document.getElementById('text').style = "background: rgba(255,255,255,1); border: 0";
    reader.onload; 
};

var handleDropArea = {
    dragover: dragHandler,
    drop: dropHandler,
    dragleave: outHandler
};

$(".droparea").on(handleDropArea);