let plotData = [];

function generateSignal() {
    const params = {
        lf_shape: document.getElementById("lf_shape").value,
        lf_freq: parseFloat(document.getElementById("lf_freq").value),
        lf_amp: parseFloat(document.getElementById("lf_amp").value),
        hf_freq: parseFloat(document.getElementById("hf_freq").value),
        mod_depth: parseFloat(document.getElementById("mod_depth").value) / 100,
        output_ch: document.getElementById("output_ch").value,
    };

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Signal generated:", data);
        updateScope();
    });
}

function updateScope() {
    fetch("/capture")
    .then(res => res.json())
    .then(data => {
        plotData = data.signal;
        Plotly.newPlot("oscilloscope", [{
            y: plotData,
            type: "line",
            line: { color: "blue" },
        }], {
            title: "Red Pitaya Oscilloscope",
            xaxis: { title: "Samples" },
            yaxis: { title: "Voltage (V)", range: [-1.1, 1.1] },
        });
    });
}

// Auto-refresh scope every 500ms
setInterval(updateScope, 500);