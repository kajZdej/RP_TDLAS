function generateSignal() {
    const params = {
        lf_freq: document.getElementById("lf_freq").value,
        lf_amp: document.getElementById("lf_amp").value,
        hf_freq: document.getElementById("hf_freq").value,
        mod_depth: document.getElementById("mod_depth").value / 100,
    };

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params),
    })
    .then(() => updateScope());
}

function updateScope() {
    fetch("/capture")
    .then(res => res.json())
    .then(data => {
        Plotly.newPlot("oscilloscope", [{
            y: data.signal,
            type: "line",
        }]);
    });
}