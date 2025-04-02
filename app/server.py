from flask import Flask, render_template, request, jsonify
import numpy as np
import redpitaya_scpi as scpi
from signal_utils import generate_modulated_signal

app = Flask(__name__)
IP = 'rp-f0cf17.local'
rp = scpi.scpi(IP)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_signal():
    params = request.json
    modulated = generate_modulated_signal(
        params["lf_shape"],
        float(params["lf_freq"]),
        float(params["lf_amp"]),
        float(params["hf_freq"]),
        float(params["mod_depth"]),
    )
    
    # Send to selected DAC channel
    ch = params["output_ch"]
    rp.tx_txt(f'SOUR{ch}:FUNC ARB')
    rp.tx_txt(f'SOUR{ch}:TRAC:DATA:DATA ' + ','.join(map(str, modulated)))
    rp.tx_txt(f'SOUR{ch}:VOLT 1')
    rp.tx_txt(f'OUTPUT{ch}:STATE ON')
    
    return jsonify({"status": f"Signal sent to DAC{ch}!"})

@app.route("/capture", methods=["GET"])
def capture_signal():
    # Read ADC data (scope function)
    rp.tx_txt('ACQ:RST')
    rp.tx_txt('ACQ:DEC 8')
    rp.tx_txt('ACQ:START')
    rp.tx_txt('ACQ:TRIG NOW')
    buffer = rp.txrx_txt('ACQ:SOUR1:DATA?')
    signal = np.array([float(x) for x in buffer.split(',')])
    return jsonify({"signal": signal.tolist()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
