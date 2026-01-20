document.getElementById("api-url").textContent = "Connected to API (via server routes)";

async function callAPI(endpoint, outputId) {
  const out = document.getElementById(outputId);
  out.textContent = "Loading...";
  try {
    const resp = await fetch(endpoint);
    const data = await resp.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    out.textContent = "Error: " + err.message;
  }
}

document.getElementById("callBtn").addEventListener("click", () =>
  callAPI("/call-query", "out")
);

document.getElementById("callBtnData").addEventListener("click", () =>
  callAPI("/call-query-data", "out2")
);

document.getElementById("callBtnUserQuery").addEventListener("click", () =>
  callAPI("/call-user-query", "out3")
);

document.getElementById("callBtnUserQueryStack").addEventListener("click", () =>
  callAPI("/call-user-query-stack", "out4")
);

document.getElementById("callBtnVerdict").addEventListener("click", () =>
  callAPI("/call-verdict", "out5")
);