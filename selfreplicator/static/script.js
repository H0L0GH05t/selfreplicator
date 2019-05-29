$( document ).ready( function() {
    
    $('#techspecs-tab').click(function(evt) {
        openTab(evt, 'techspecs');
    });
    
    $('#requirements-tab').click(function(evt) {
        openTab(evt, 'requirements');
    });
    
    $('#installation-tab').click(function(evt) {
        openTab(evt, 'installation');
    });
    
    $('#links-tab').click(function(evt) {
        openTab(evt, 'links');
    });
    
    function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;
    
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
    }
    $('#execute-btn').click(function() {
        
        // Show loading text
        value = $('.executed-btn-text').attr("class").replace("hidden-text", "");
        $('.executed-btn-text').attr("class", value);
        
        // Make button hidden
        $('.execute-btn-text').hide();
        $('#execute-btn').attr("disabled", true);
        
    });
    document.getElementById("techspecs-tab").click();
});