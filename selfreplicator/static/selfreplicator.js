$( document ).ready( function() {
    $('#execute-btn').click(function() {
        $('.execute-btn-text').add(".hidden");
        $('.executed-btn-text').remove(".hidden");
        $('#execute-btn').attr("disabled", true);
        
        getGitHubAuth();
    });
});

function getGitHubAuth(){
    $.ajax({
        type : 'POST',
        url : '/',
        data : {
            getting_auth : "true"
        },
        success : function(responseText) {
            //console.log(responseText)
        },
        complete : function(responseText) {
            console.log(responseText)
            // do stuff
        },
        error : function(xhr, status) {
            console.log('Error saving ePaper');
            console.log('error ' + xhr.status + " ---- " + xhr.statusText + ' --- ' + status);
        }
    });
}