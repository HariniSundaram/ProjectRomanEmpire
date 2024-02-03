document.addEventListener('DOMContentLoaded', function() {
    const deliveryForm = document.getElementById('deliveryForm');
    
    if (deliveryForm) {
        deliveryForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the form from submitting as a normal HTTP request
            
            // Collect form data
            const startCityName = document.getElementById('startCityName').value;
            const startCityCoordinates = document.getElementById('startCityCoordinates').value;
            const intermediateCityName = document.getElementById('intermediateCityName').value;
            const intermediateCityCoordinates = document.getElementById('intermediateCityCoordinates').value;
            const timeMinutes = document.getElementById('timeMinutes').value;
            const delay = document.getElementById('delay').value;
            const date = document.getElementById('date').value;
            
            // Create an object with the collected data
            const deliveryData = {
                startCityName,
                startCityCoordinates,
                intermediateCityName,
                intermediateCityCoordinates,
                timeMinutes,
                delay,
                date
            };
            
            // Send the data to SupaBase or perform any necessary operations
            // Example: You can use SupaBase client to insert data into the dataset
            
            // Clear the form fields after submission
            deliveryForm.reset();
        });
    }
});
