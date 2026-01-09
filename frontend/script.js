const fileInput = document.getElementById("fileInput");
const heightInput = document.getElementById("heightInput");
const fileName = document.getElementById("fileName");
const estimateBtn = document.getElementById("estimateBtn");
const loader = document.getElementById("loader");
const form = document.querySelector('form')
const result = document.querySelector("#result")

let selectedFile = null;

// Show selected file name
fileInput.addEventListener("change", () => {
  selectedFile = fileInput.files[0];
  // console.log(selectedFile)
  fileName.textContent = selectedFile ? selectedFile.name : "No File Chosen";
});

// Button click → loading → result page
estimateBtn.addEventListener("click", async () => {
  if (!selectedFile) {
    alert("Please select a video first");
    return;
  }

  loader.classList.remove("hidden");
  estimateBtn.disabled = true;
  
  const formData = new FormData();
  formData.append("video", fileInput.files[0]);
  formData.append("height_cm", heightInput.value);
  
  const res = await fetch('http://127.0.0.1:8000/estimate-size', {
    method: 'post',
    body: formData
  })

  const data = await res.json()

  // console.log(data)
  
  loader.classList.add("hidden");
  estimateBtn.disabled = false;
  
  result.classList.remove("hidden")
  result.textContent = `Estimated Size: ${data.size} (Confidence = ${data.confidence}%)`

});
