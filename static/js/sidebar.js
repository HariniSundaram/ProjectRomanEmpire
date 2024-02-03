document.addEventListener('DOMContentLoaded', function() {
    var menuIcon = document.getElementById('menuIcon');
    var sidebar = document.getElementById('sidebar');
  
    menuIcon.addEventListener('click', function() {
      // Check if the sidebar is open and toggle the class accordingly
      if (sidebar.classList.contains('open-sidebar')) {
        sidebar.classList.remove('open-sidebar');
      } else {
        sidebar.classList.add('open-sidebar');
      }
    });
  });