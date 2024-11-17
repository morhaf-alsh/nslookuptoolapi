// script.js

let domainCount = 0;
const maxManualDomains = 10;
const maxCsvDomains = 100;

// Adds a new domain input field
function addDomainInput() {
  if (domainCount < maxManualDomains) {
    const inputDiv = document.createElement("div");
    inputDiv.innerHTML = `<div class="row"><input type="text" name="domain" placeholder="Enter domain name" required> <button id="delete">delete</button><div>`;
    document.getElementById("domainInputs").appendChild(inputDiv);
    domainCount++;
  } else {
    alert(`You can only add up to ${maxManualDomains} domains manually.`);
  }
}

// Reads CSV file and extracts domains
function handleCsvUpload(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = function(event) {
      const rows = event.target.result.split("\n").map(row => row.trim());
      if (rows.length > maxCsvDomains) {
        reject(`CSV file can contain up to ${maxCsvDomains} domains.`);
      } else {
        resolve(rows.filter(row => row.length > 0));
      }
    };
    reader.onerror = () => reject("Failed to read file.");
    reader.readAsText(file);
  });
}

// Handles form submission
async function submitForm() {
  const domains = [];
  
  // Collect domains from manual inputs
  document.querySelectorAll("input[name='domain']").forEach(input => {
    if (input.value.trim()) {
      domains.push(input.value.trim());
    }
  });

  // Collect domains from CSV if a file is uploaded
  const csvFile = document.getElementById("csvFile").files[0];
  if (csvFile) {
    try {
      const csvDomains = await handleCsvUpload(csvFile);
      domains.push(...csvDomains);
    } catch (error) {
      document.getElementById("responseMessage").textContent = error;
      return;
    }
  }

  // Ensure total domains count is within limit
  if (domains.length === 0) {
    document.getElementById("responseMessage").textContent = "Please enter or upload at least one domain.";
    return;
  }
  if (domains.length > maxCsvDomains) {
    document.getElementById("responseMessage").textContent = `Total domains cannot exceed ${maxCsvDomains}.`;
    return;
  }

  console.log(domains);
  // Send domains to the remote API
  try {
    const url = new URL("https://nslookuptoolapi.vercel.app/dnslookup");
    url.searchParams.append("record_type", "A");
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(domains)
    });
    const result = await response.json();
    document.getElementById("responseMessage").textContent = result.message || "Domains uploaded successfully!";
  } catch (error) {
    document.getElementById("responseMessage").textContent = "Failed to upload domains.";
  }
}
