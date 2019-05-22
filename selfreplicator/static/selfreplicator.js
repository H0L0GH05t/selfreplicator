$( document ).ready( function() {
    $('#execute-btn').click(function() {
        
        // Show loading text
        value = $('.executed-btn-text').attr("class").replace("hidden-text", "");
        $('.executed-btn-text').attr("class", value);
        
        // Make button hidden
        $('.execute-btn-text').hide();
        $('#execute-btn').attr("disabled", true);
        
        getGitHubAuth();
    });
});

function getGitHubAuth(){
    $.ajax({
        type : 'POST',
        url : 'results/',
        success : function(responseText) {
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