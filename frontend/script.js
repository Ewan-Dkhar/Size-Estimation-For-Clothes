const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const estimateBtn = document.getElementById("estimateBtn");
const loader = document.getElementById("loader");

let selectedFile = null;

// Show selected file name
fileInput.addEventListener("change", () => {
  selectedFile = fileInput.files[0];
  fileName.textContent = selectedFile ? selectedFile.name : "No File Chosen";
});

// Button click → loading → result page
estimateBtn.addEventListener("click", async () => {
  if (!selectedFile) {
    alert("Please select an image first");
    return;
  }

  loader.classList.remove("hidden");
  estimateBtn.disabled = true;

  // Placeholder for ML API call
  setTimeout(() => {
    window.location.href = "result.html";
  }, 2000);
});
