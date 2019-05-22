$( document ).ready( function() {
    $('#execute-btn').click(function() {
        
        // Show loading text
        value = $('.executed-btn-text').attr("class").replace("hidden-text", "");
        $('.executed-btn-text').attr("class", value);
        
        // Make button hidden
        $('.execute-btn-text').hide();
        $('#execute-btn').attr("disabled", true);
        
    });
});