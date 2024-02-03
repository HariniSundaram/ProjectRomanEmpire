// document.addEventListener('DOMContentLoaded', function() {
//     // Fetch routes data from your server
//     fetch('/api/routes')
//         .then(response => response.json())
//         .then(data => {
//             data.routes.forEach(route => {
//                 // Assuming 'route' has 'latitude' and 'longitude'
//                 var marker = L.marker([route.latitude, route.longitude]).addTo(map);
//                 marker.bindPopup(`<b>${route.name}</b><br>${route.details}`).openPopup();
                
//                 // Add more interaction as needed
//             });
//         })
//         .catch(error => console.error('Error:', error));
// });
