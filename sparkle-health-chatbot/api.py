from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import base64
from io import BytesIO

from hybrid_insight_engine import generate_combined_insights
from trends import plot_health_trends

app = Flask(__name__)

CORS(app, resources={r"/upload-csv/*": {
    "origins": [
        "https://devulapellykushalhie.vercel.app",
        "http://localhost:3000"
    ]
}})

@app.route('/upload-csv/', methods=['POST'])
def upload_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Read CSV into DataFrame
        df = pd.read_csv(file)
        print("✅ CSV successfully loaded.")
        print("📊 Data preview:\n", df.head())

        # Generate insights
        insights = generate_combined_insights(df)
        print("✅ Insights generated.")

        # Generate trend plot and convert to base64
        fig = plot_health_trends(df)
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()

        return jsonify({
            "insights": insights,
            "trend_image": img_str
        })

    except Exception as e:
        print("❌ Error during processing:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
