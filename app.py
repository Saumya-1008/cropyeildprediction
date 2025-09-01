from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load data
df = pd.read_csv("crop_yield.csv")
print("Data loaded")

# Extract unique values
seasons = sorted(df["Season"].unique())
states = sorted(df["State"].unique())
years = sorted(df["Crop_Year"].unique())

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    recommended_crop = None
    benefits = ""
    error = None

    if request.method == "POST":
        try:
            state = request.form["State"]
            season = request.form["Season"]
            year = int(request.form["Crop_Year"])
            area = float(request.form["Area"])
            production = float(request.form["Production"])
            rainfall = float(request.form["Annual_Rainfall"])
            fertilizer = float(request.form["Fertilizer"])
            pesticide = float(request.form["Pesticide"])

            # Suggest crop based on state and season
            filtered = df[(df["State"] == state) & (df["Season"] == season)]
            if not filtered.empty:
                recommended_crop = filtered["Crop"].mode()[0]
            else:
                recommended_crop = "No common crop found"

            # Yield Calculation
            result = round((production / area), 2)

            # Example crop benefits
            #   
            crop_info = {
    "Arecanut": "Grown throughout the year. Requires well-drained soil and high humidity. Average yield: 1.5–2 tons/ha.",
    "Arhar/Tur": "Kharif crop. Needs warm climate and well-drained loamy soil. Average yield: 1–1.2 tons/ha.",
    "Bajra": "Kharif crop. Drought-resistant, grows well in sandy soil. Average yield: 1.2–1.5 tons/ha.",
    "Banana": "Perennial. Requires rich soil and abundant water. Average yield: 30–35 tons/ha.",
    "Barley": "Rabi crop. Needs cool climate and loamy soil. Average yield: 2.2–2.5 tons/ha.",
    "Black pepper": "Perennial. Thrives in hot, humid climate with shade. Average yield: 0.4–0.5 tons/ha.",
    "Cardamom": "Perennial. Requires humid, cool climate and rich forest soil. Yield: 0.1–0.2 tons/ha.",
    "Cashewnut": "Perennial. Suited for coastal regions with sandy soil. Yield: 1–2 tons/ha.",
    "Castor seed": "Kharif crop. Grows in tropical climates with moderate rainfall. Yield: 1–1.5 tons/ha.",
    "Coconut": "Perennial. Needs high rainfall, sandy loam soil. Yield: 10–15 tons/ha (nut equivalent).",
    "Coriander": "Grown year-round. Needs cool climate and well-drained soil. Yield: 1–1.2 tons/ha.",
    "Cotton(lint)": "Kharif crop. Requires warm climate and black soil. Yield: 1.5–2 tons/ha.",
    "Cowpea(Lobia)": "Kharif crop. Grows well in sandy loam. Yield: 1–1.2 tons/ha.",
    "Dry chillies": "Grown year-round. Thrives in warm, dry weather. Yield: 0.8–1 tons/ha.",
    "Garlic": "Year-round. Needs cool climate and sandy loam soil. Yield: 4–5 tons/ha.",
    "Ginger": "Kharif crop. Requires warm, humid climate and well-drained soil. Yield: 15–18 tons/ha.",
    "Gram": "Rabi crop. Thrives in dry climate with sandy loam soil. Yield: 1–1.5 tons/ha.",
    "Groundnut": "Kharif crop. Needs sandy loam and moderate rainfall. Yield: 2–3 tons/ha.",
    "Guar seed": "Kharif crop. Drought-tolerant, suited for sandy soils. Yield: 0.8–1 tons/ha.",
    "Horse-gram": "Kharif crop. Grows in poor soils with low rainfall. Yield: 0.5–0.8 tons/ha.",
    "Jowar": "Kharif crop. Drought-resistant, needs light soil. Yield: 1–2 tons/ha.",
    "Jute": "Kharif crop. Needs warm, humid climate and alluvial soil. Yield: 2–2.5 tons/ha (fiber).",
    "Khesari": "Rabi crop. Hardy pulse crop suited for poor soils. Yield: 1–1.2 tons/ha.",
    "Linseed": "Rabi crop. Cold-tolerant, requires moderate rainfall. Yield: 0.7–1 tons/ha.",
    "Maize": "Kharif crop. Grows in well-drained soil and needs moderate rain. Yield: 2.5–3.5 tons/ha.",
    "Masoor": "Rabi crop. Requires cool climate and loamy soil. Yield: 1–1.2 tons/ha.",
    "Mesta": "Kharif crop. Grown for fiber. Requires warm, humid climate. Yield: 1.2–1.5 tons/ha.",
    "Moong(Green Gram)": "Kharif crop. Fast-growing, needs light soil. Yield: 0.8–1.2 tons/ha.",
    "Moth": "Kharif crop. Drought-resistant legume. Yield: 0.5–0.8 tons/ha.",
    "Niger seed": "Kharif crop. Thrives in hilly, tribal regions. Yield: 0.3–0.5 tons/ha.",
    "Oilseeds total": "Aggregate of oilseeds grown across seasons. Yield varies: ~1–2 tons/ha.",
    "Onion": "Year-round. Requires cool temperature and well-drained soil. Yield: 15–20 tons/ha.",
    "Other Rabi pulses": "Group of pulses grown in Rabi. Yield: ~1–1.2 tons/ha.",
    "Other Cereals": "Miscellaneous cereals. Seasonal and regional variations. Yield: 1–2 tons/ha.",
    "Other Kharif pulses": "Group of pulses for Kharif. Yield: ~1–1.3 tons/ha.",
    "Other Summer Pulses": "Legumes sown in summer. Needs irrigation. Yield: ~1 tons/ha.",
    "Peas & beans (Pulses)": "Rabi crop. Needs cool weather. Yield: 1.2–1.5 tons/ha.",
    "Potato": "Grown year-round. Requires cool temp, fertile soil. Yield: 20–25 tons/ha.",
    "Ragi": "Kharif crop. Thrives in poor soil, drought-resistant. Yield: 1–1.5 tons/ha.",
    "Rapeseed & Mustard": "Rabi crop. Requires cool climate and loamy soil. Yield: 1–1.5 tons/ha.",
    "Rice": "Kharif crop. Requires high rainfall and water-logged soil. Yield: 2–2.5 tons/ha.",
    "Safflower": "Rabi crop. Drought-tolerant, suited for dryland farming. Yield: 0.6–1 tons/ha.",
    "Sannhamp": "Year-round. Used as green manure/fodder. Yield: 1–1.5 tons/ha (dry matter).",
    "Sesamum": "Kharif crop. Needs dry climate, grows in light soil. Yield: 0.4–0.6 tons/ha.",
    "Small millets": "Kharif crop. Hardy cereals for hilly/dry areas. Yield: 0.8–1.2 tons/ha.",
    "Soyabean": "Kharif crop. Needs warm climate and moderate rain. Yield: 1.5–2 tons/ha.",
    "Sugarcane": "Perennial. High water requirement, grows in deep loamy soil. Yield: 60–80 tons/ha.",
    "Sunflower": "Kharif crop. Needs sunshine and light soil. Yield: 1.2–1.5 tons/ha.",
    "Sweet potato": "Year-round. Needs loamy soil and warm weather. Yield: 10–12 tons/ha.",
    "Tapioca": "Year-round. Requires tropical climate and light soil. Yield: 20–25 tons/ha.",
    "Tobacco": "Year-round. Needs sandy loam and dry climate. Yield: 1.5–2 tons/ha.",
    "Turmeric": "Year-round. Requires warm, humid climate. Yield: 5–8 tons/ha.",
    "Urad": "Kharif crop. Needs warm climate, loamy soil. Yield: 0.7–1 tons/ha.",
    "Wheat": "Rabi crop. Prefers cool, dry climate and loamy soil. Yield: 2.5–3 tons/ha.",
    "other oilseeds": "Kharif group. Includes minor oilseed crops. Yield: ~1 tons/ha.",
}

            benefits = crop_info.get(recommended_crop, "No specific data available. Refer to agriculture department or trusted sources.")

        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template("index.html", result=result, error=error,
                           seasons=seasons, states=states, years=years,
                           recommended_crop=recommended_crop, benefits=benefits)

if __name__ == "__main__":
    app.run(debug=True)
