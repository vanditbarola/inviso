document.addEventListener("DOMContentLoaded", function() {
    const purchaseBtn = document.getElementById("purchase-btn");
    const mainPage = document.getElementById("main-page");
    const encodePage = document.getElementById("encode-page");
    const decodePage = document.getElementById("decode-page");
    const purchasePage = document.getElementById("purchase-page");

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
