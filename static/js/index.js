
function promptLikeEvent() {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar")

    // Add the "show" class to DIV
    x.className = "show";
    x.textContent = "Event Liked!";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

function promptSaveEvent() {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar")

    // Add the "show" class to DIV
    x.className = "show";
    x.textContent = "Event Added to Your List!";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

function saveEvent(event_id){
    $.post(appConfig.save_event_url, { "id":event_id } );  //Your values here..
    promptSaveEvent();
}

function likeEvent(event_id){
    $.post(appConfig.like_event_url, { "id":event_id } );  //Your values here..
    console.log("finding id = #thumb" + event_id);
    // document.getElementById('thumb' + event_id).className = "";
    $("#thumb" + event_id).removeClass().addClass("fas fa-thumbs-up orange-text");
    //grey-text text-darken-3
    promptLikeEvent();
}
