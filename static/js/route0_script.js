document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([40.4406, -79.995888], 7);
    
    // Load and display tile layers on the map
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 15,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Function to get a distinct color for each route
    function getColor(index) {
        const colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'];
        return colors[index % colors.length];
    }

    fetch('/api/routes')
    .then(response => response.json())
    .then(routes => {
        // Use a specific index, for example 0 for the first route
        let index = 0; // Adjust this index to select the specific route you want
        let route = routes[index];

        // Flip the coordinates for each point in the route
        var correctedRoute = route.map(coord => [coord[1], coord[0]]);
        var polyline = L.polyline(correctedRoute, {
            color: getColor(index),
            weight: 4
        }).addTo(map);

        // Add markers for the start and end points
        L.marker(correctedRoute[0]).addTo(map).bindPopup('Start of Route ' + (index + 1));
        L.marker(correctedRoute[correctedRoute.length - 1]).addTo(map).bindPopup('End of Route ' + (index + 1));
    })
    .catch(error => console.error('Error:', error));
});
