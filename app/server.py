from flask import Flask, render_template, request, jsonify
import numpy as np
from redpitaya_scpi import scpi

app = Flask(__name__)
rp = scpi("192.168.1.100")  # Replace with your Red Pitaya IP

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_signal():
    params = request.json
    lf_freq = float(params["lf_freq"])
    lf_amp = float(params["lf_amp"])
    hf_freq = float(params["hf_freq"])
    mod_depth = float(params["mod_depth"])

    # Generate modulated signal (see signal_utils.py)
    modulated_signal = generate_modulated_signal(lf_freq, lf_amp, hf_freq, mod_depth)
    
    # Send to Red Pitaya DAC
    rp.tx_txt('GEN:RST')
    rp.tx_txt('SOUR1:FUNC ARB')
    rp.tx_txt('SOUR1:TRAC:DATA:DATA ' + ','.join(map(str, modulated_signal)))
    rp.tx_txt('SOUR1:VOLT 1')
    rp.tx_txt('OUTPUT1:STATE ON')

    return jsonify({"status": "Signal generated!"})

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
