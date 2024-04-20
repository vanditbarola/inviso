document.addEventListener("DOMContentLoaded", function() {
    // Get references to relevant elements
    const encodeBtn = document.getElementById("encode-btn");
    const decodeBtn = document.getElementById("decode-btn");
    const purchaseBtn = document.getElementById("purchase-btn");
    const encodePage = document.getElementById("encode-page");
    const mainPage = document.getElementById("main-page");
    const purchasePage = document.getElementById("purchase-page");
    const decodePage = document.getElementById("decode-page");
    const selectImageDropdown = document.querySelector('select[name="select-image"]');

    // Hide encode page, purchase page, and decode page initially
    encodePage.style.display = "none";
    purchasePage.style.display = "none";
    decodePage.style.display = "none";

    // Add event listener to the encode button
    encodeBtn.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent default link behavior
        // Hide main page, purchase page, and decode page
        mainPage.style.display = "none";
        purchasePage.style.display = "none";
        decodePage.style.display = "none";
        // Show encode page
        encodePage.style.display = "block";
        
        // Fetch image files from the server
        fetch('/encode')
            .then(response => response.json())
            .then(data => {
                // Clear existing dropdown options
                selectImageDropdown.innerHTML = '';
                const defaultOption = document.createElement('option');
                defaultOption.textContent = 'Select an image';
                defaultOption.disabled = true;
                defaultOption.selected = true;
                selectImageDropdown.appendChild(defaultOption);
                // Add options for each image file
                data.image_files.forEach(file => {
                    const option = document.createElement('option');
                    option.value = file;
                    option.textContent = file;
                    selectImageDropdown.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching image files:', error));

    });

    // Add event listener to the decode button
    decodeBtn.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent default link behavior
        // Hide main page, purchase page, and encode page
        mainPage.style.display = "none";
        purchasePage.style.display = "none";
        encodePage.style.display = "none";
        // Show decode page
        decodePage.style.display = "block";
    });

    // Add event listener to the purchase button
    purchaseBtn.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent default link behavior
        // Hide main page, encode page, and decode page
        mainPage.style.display = "none";
        encodePage.style.display = "none";
        decodePage.style.display = "none";
        // Show purchase page
        purchasePage.style.display = "block";
    });
    
});
