#importing required libraries

from flask import Flask, request, render_template, flash, jsonify, session
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import os
import json
from datetime import datetime
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load the model
#hello
try:
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pickle', 'model.pkl')
    print(f"🔍 Loading model from: {model_path}")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"File missing at: {model_path}")

    with open(model_path, "rb") as f:
        gbc = pickle.load(f)

    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Model load failed: {e}")
    gbc = None
    
def get_feature_analysis(features):
    feature_names = [
        "Using IP Address", "Long URL", "Short URL", "Symbol @", "Redirecting",
        "Prefix/Suffix", "Sub Domains", "HTTPS", "Domain Registration Length",
        "Favicon", "Non-Standard Port", "HTTPS Domain URL", "Request URL",
        "Anchor URL", "Links in Script Tags", "Server Form Handler",
        "Info Email", "Abnormal URL", "Website Forwarding", "Status Bar Customization",
        "Disable Right Click", "Using Popup Window", "Iframe Redirection",
        "Age of Domain", "DNS Recording", "Website Traffic", "Page Rank",
        "Google Index", "Links Pointing to Page", "Stats Report"
    ]
    
    analysis = []
    # Ensure feature_names and features have the same length
    for i, feature in enumerate(features):
        if i < len(feature_names):
            status = "safe" if feature == 1 else "warning" if feature == 0 else "danger"
            analysis.append({
                "name": feature_names[i],
                "status": status,
                "value": feature,
                "description": get_feature_description(feature_names[i], feature)
            })
    return analysis

def get_feature_description(feature_name, value):
    descriptions = {
        "Using IP Address": {
            1: "URL uses a domain name instead of an IP address.",
            -1: "URL uses an IP address directly, which is suspicious."
        },
        "Long URL": {
            1: "URL length is within a normal range.",
            0: "URL length is slightly long, proceed with caution.",
            -1: "URL is unusually long, a common phishing tactic."
        },
        "Short URL": {
            1: "URL is not using a URL shortening service.",
            -1: "URL uses a shortening service, which can hide the true destination."
        },
        "Symbol @": {
            1: "No '@' symbol found in the URL.",
            -1: "URL contains '@' symbol, which can be used to mislead users."
        },
        "Redirecting": {
            1: "No suspicious '//' redirects found in the URL path.",
            -1: "URL contains '//' in the path, indicating a potential redirect."
        },
        "Prefix/Suffix": {
            1: "Domain name does not contain a suspicious '-' prefix/suffix.",
            -1: "Domain name contains a '-' symbol, often used in phishing URLs."
        },
        "Sub Domains": {
            1: "A normal number of subdomains are present.",
            0: "A moderate number of subdomains are present.",
            -1: "An excessive number of subdomains are present, which is suspicious."
        },
        "HTTPS": {
            1: "The website uses a valid HTTPS protocol.",
            -1: "The website does not use HTTPS, which is a security risk."
        },
        "Domain Registration Length": {
            1: "The domain's registration length is valid for over a year.",
            -1: "The domain is registered for a short period, which is suspicious."
        },
        "Favicon": {
            1: "The favicon is hosted on the same domain.",
            -1: "The favicon is loaded from an external or suspicious domain."
        },
        "Non-Standard Port": {
            1: "The URL uses standard web ports (80 or 443).",
            -1: "A non-standard port is specified, which is unusual for websites."
        },
        "HTTPS Domain URL": {
            1: "The domain name does not contain 'https' as a substring.",
            -1: "The domain name itself contains 'https', which is a misleading tactic."
        },
        "Request URL": {
            1: "Most content (images, audio) is loaded from the same domain.",
            0: "A moderate amount of content is loaded from external domains.",
            -1: "A high percentage of content is loaded from external domains."
        },
        "Anchor URL": {
            1: "Most links on the page point to the same domain.",
            0: "A moderate number of links point to external or invalid domains.",
            -1: "A high percentage of links point to suspicious or external domains."
        },
        "Links in Script Tags": {
            1: "Links within <script> and <link> tags appear to be from the same domain.",
            0: "Some links in tags point to external domains.",
            -1: "A high percentage of links in tags point to external domains."
        },
        "Server Form Handler": {
            1: "Forms on the page submit data to the same domain.",
            0: "Form handlers are suspicious (e.g., mailto) or point externally.",
            -1: "Forms submit to a blank or invalid location, which is a high-risk indicator."
        },
        "Info Email": {
            1: "The page does not contain suspicious 'mailto' links.",
            -1: "The page contains 'mailto' links, which can be used for phishing."
        },
        "Abnormal URL": {
            1: "The URL structure appears to be normal.",
            -1: "The URL is abnormal (e.g., domain name in path)."
        },
        "Website Forwarding": {
            1: "The URL has a minimal number of redirects.",
            0: "The URL has a moderate number of redirects.",
            -1: "The URL has an excessive number of redirects, which is suspicious."
        },
        "Status Bar Customization": {
            1: "The website does not attempt to manipulate the browser status bar.",
            -1: "The website uses scripts to customize the status bar, a common phishing tactic."
        },
        "Disable Right Click": {
            1: "Right-click functionality is not disabled.",
            -1: "The website attempts to disable the right-click menu."
        },
        "Using Popup Window": {
            1: "The page does not use suspicious pop-up windows.",
            -1: "The page uses pop-up windows with text fields, which is a phishing indicator."
        },
        "Iframe Redirection": {
            1: "The page does not use iframes for redirection.",
            -1: "The page uses invisible iframes, which can be used for malicious purposes."
        },
        "Age of Domain": {
            1: "The domain is more than 6 months old.",
            -1: "The domain is very new, which is a high-risk factor."
        },
        "DNS Recording": {
            1: "A DNS record was found for the domain.",
            -1: "No DNS record was found, or the domain is not registered."
        },
        "Website Traffic": {
            1: "The website has a high volume of traffic (Alexa top 100k).",
            0: "The website has a moderate level of traffic.",
            -1: "The website has very low or no traffic, which is suspicious for a legitimate site."
        },
        "Page Rank": {
            1: "The website has a good page rank.",
            -1: "The website has a very low or zero page rank."
        },
        "Google Index": {
            1: "The website is indexed by Google.",
            -1: "The website is not indexed by Google, which is suspicious."
        },
        "Links Pointing to Page": {
            1: "The page has a healthy number of inbound links.",
            0: "The page has a low number of inbound links.",
            -1: "The page has very few or no inbound links."
        },
        "Stats Report": {
            1: "The domain is not associated with known phishing IPs or hosts.",
            -1: "The domain's host or IP is on a list of known malicious entities."
        }
    }
    # Return a default description if the specific value is not found
    return descriptions.get(feature_name, {}).get(value, "No specific description available for this value.")


def validate_url(url):
    if not url:
        return False, "Please enter a URL"
    if not url.startswith(('http://', 'https://')):
        return False, "URL must start with http:// or https://"
    return True, None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            url = request.form["url"]
            is_valid, error_message = validate_url(url)
            
            if not is_valid:
                flash(error_message, "danger")
                return render_template("index.html", xx=-1)
            
            obj = FeatureExtraction(url)
            features = obj.getFeaturesList()

            # --- DEBUGGING ---
            # Print the number of features extracted to the terminal
            print(f"✅ DEBUG: Extracted {len(features)} features.")
            # Print the features themselves
            print(f"✅ DEBUG: Features list: {features}")
            # -----------------
            
            # Check if the number of features is correct before reshaping
            if len(features) != 30:
                error_msg = f"Feature extraction failed. Expected 30 features, but got {len(features)}. Please check the terminal logs."
                flash(error_msg, "danger")
                return render_template("index.html", xx=-1)

            x = np.array(features).reshape(1,30)
            
            if gbc is None:
                flash("Model not loaded properly. Please contact administrator.", "danger")
                return render_template("index.html", xx=-1)
            
            try:
                y_pred = gbc.predict(x)[0]
                y_pro_phishing = gbc.predict_proba(x)[0, 0]
                y_pro_non_phishing = gbc.predict_proba(x)[0, 1]
                print("✅ Prediction done:", y_pred)
            except Exception as e:
                print(f"❌ Prediction error: {e}")
                flash("Prediction failed. Please check server logs.", "danger")
                return render_template("index.html", xx=-1)
            
            # Use non-phishing probability for safety score
            threat_level = y_pro_non_phishing * 100 
            if threat_level > 70:
                status = "safe"
                prediction = f"This URL appears to be safe ({threat_level:.2f}% confidence)"
            elif threat_level > 30:
                status = "warning"
                prediction = f"Exercise caution with this URL ({threat_level:.2f}% confidence)"
            else:
                status = "danger"
                prediction = f"This URL appears to be unsafe ({threat_level:.2f}% confidence)"
            
            # Get feature analysis
            feature_analysis = get_feature_analysis(features)
            
            # Store scan history in session
            if 'scan_history' not in session:
                session['scan_history'] = []
            
            scan_entry = {
                'url': url,
                'status': status,
                'score': round(threat_level),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'features': feature_analysis
            }
            
            session['scan_history'].insert(0, scan_entry)
            session['scan_history'] = session['scan_history'][:20] # Keep last 20 scans
            session.modified = True
            
            return render_template('index.html', 
                                   xx=round(threat_level/100,2), 
                                   url=url, 
                                   prediction=prediction,
                                   threat_level=threat_level,
                                   status=status,
                                   feature_analysis=feature_analysis,
                                   scan_history=session.get('scan_history', []))
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", "danger")
            return render_template("index.html", xx=-1)
    
    return render_template("index.html", xx=-1, scan_history=session.get('scan_history', []))

@app.route("/clear-history", methods=["POST"])
def clear_history():
    session.pop('scan_history', None)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
