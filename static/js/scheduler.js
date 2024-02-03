
import { createClient } from '@supabase/supabase-js'
// const supabaseUrl = 'https://pebawjinuyvzzosaksdl.supabase.co'
// const supabaseKey = process.env.SUPABASE_KEY
// const supabase = createClient(supabaseUrl, supabaseKey)
const supabase = createClient('https://pebawjinuyvzzosaksdl.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBlYmF3amludXl2enpvc2Frc2RsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDY5Mzc1OTIsImV4cCI6MjAyMjUxMzU5Mn0.Zn5_wepHSjy0sxgPryPV6p4VRJ5sM0Orxhi0TtS_Gw8')

document.addEventListener('DOMContentLoaded', function() {
    const deliveryForm = document.getElementById('deliveryForm');
    console.log("SHIT")
    if (deliveryForm) {
        // Make the function async to use await inside
        deliveryForm.addEventListener('submit', async function(event) {
            event.preventDefault();
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
            console.log('before the try')
            try {
                const { data, error } = await supabase
                    .from('truckDeliveries')
                    .insert([deliveryData]);

                if (error) {
                    throw error;
                }

                console.log('Data inserted successfully', data);
                // Reset the form fields
                // deliveryForm.reset();
            } catch (error) {
                console.error('Error inserting data:', error);
                print("HELPPP")
            }
            // deliveryForm.reset();
        });
    }
});

// Sidebar toggle function
function toggleSidebar() {
    var sidebar = document.getElementById("mySidebar");
    sidebar.style.width = sidebar.style.width === '250px' ? '0' : '250px';
}

// Function to close the sidebar
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
}
