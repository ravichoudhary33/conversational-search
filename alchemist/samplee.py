import json

["Midi","Skinny","Mini","Black","Slim","[30.00 TO 59.99]","XL","M","Tops","Shirts","V-Neck"]

affinity = {
    "length_uFilter": {
      "Midi": 526,
      "Mini": 445,
      "Maxi": 253,
      "Long": 1
    },
    "color_uFilter": {
      "Black": 79,
      "White": 62,
      "Green": 56,
      "Blue": 50,
      "Pink": 47,
      "Red": 32,
      "Brown": 22
    },
    "v_storeIds": {
      "163": 68,
      "291": 64,
      "318": 66,
      "394": 65,
      "466": 88,
      "573": 73,
      "700": 79
    },
    "fit_uFilter": {
      "Slim": 168,
      "Extra Slim": 75,
      "Classic": 35,
      "Skinny": 20,
      "Editor": 11,
      "Body Contour": 9,
      "Relaxed": 6
    },
    "sortPrice": {
      "[0.00 TO 29.99]": 212,
      "[30.00 TO 59.99]": 75,
      "[60.00 TO 89.99]": 20,
      "[0.0029.99]": 19,
      "[90.00 TO 119.99]": 10,
      "[90.00119.99]": 3,
      "[120.00 TO 149.99]": 3
    },
    "v_color_uFilter": {
      "Black": 478,
      "White": 386,
      "Blue": 258,
      "Pink": 223,
      "Green": 147,
      "Neutral": 111,
      "Brown": 95
    },
    "size_uFilter": {
      "2": 175,
      "4": 166,
      "14": 172,
      "L": 231,
      "S": 200,
      "M": 187,
      "XL": 177
    },
    "categoryType_uFilter": {
      "Tops": 2452,
      "Dresses & Jumpsuits": 1526,
      "Bottoms": 1439,
      "Shirts": 1015,
      "Pants": 392,
      "Jackets": 342,
      "Accessories": 301
    },
    "type_uFilter": {
      "Blouses": 561,
      "Tanks": 268,
      "Button Down Shirts": 226,
      "Tees": 225,
      "Tees & Henleys": 197,
      "Shirts": 158,
      "Suit Jacket": 153
    },
    "gender_uFilter": {
      "women": 791,
      "men": 342
    },
    "legShape_uFilter": {
      "Straight": 196,
      "Skinny": 179,
      "Wide Leg": 159,
      "Flare": 137,
      "Ankle": 106,
      "Skyscraper": 86,
      "Boot": 86
    },
    "v_size_uFilter": {
      "10": 210,
      "16": 199,
      "M": 614,
      "L": 458,
      "XL": 365,
      "S": 363,
      "XS": 226
    },
    "sleeveLength_uFilter": {
      "3": 1,
      "Short": 254,
      "Long": 238,
      "Sleeveless": 81,
      "3/4 Sleeve": 29,
      "Sleeveless (79)": 1
    },
    "occasion_uFilter": {
      "Cocktail & Party": 187,
      "Work": 57,
      "Casual": 50,
      "Party": 1
    },
    "styleRefinement_uFilter": {
      "Denim": 67,
      "Editor": 25,
      "Stylist": 20,
      "Essentials": 13,
      "Slim": 12,
      "Relaxed": 10,
      "Jumpsuit & Romper": 5
    },
    "rise_uFilter": {
      "High Waisted": 194,
      "Mid Rise": 169,
      "Super High Waisted": 106,
      "Low Rise": 32,
      "High Waisted (54)": 1
    },
    "neckline_uFilter": {
      "Crew": 29,
      "V-Neck": 14,
      "Square": 6,
      "Collared": 4,
      "Scoop": 3,
      "One Shoulder": 1,
      "Off the Shoulder": 1
    },
    "brands_uFilter": {
      "MYTAGALONGS": 8,
      "Express": 6,
      "PRE-OWNED LOUIS VUITTON": 3,
      "PRE-OWNED CELINE": 2,
      "PRE-OWNED HERMES": 1,
      "PRE-OWNED YVES SAINT LAURENT": 1
    },
    "wash_uFilter": {
      "Medium": 13,
      "White": 13,
      "Black": 10,
      "Dark": 7,
      "Color": 6,
      "Light": 3,
      "Gray": 1
    },
    "fabrication_uFilter": {
      "Satin": 10,
      "Cotton Stretch": 9,
      "Hyper Stretch": 9,
      "Modern Tech Knit": 8,
      "Linen": 4,
      "Stretch": 3,
      "Poplin": 2
    },
    "v_color_ufilter": {
      "multi-color": 3,
      "gray": 2,
      "light pink": 2,
      "neutral": 2,
      "green": 1,
      "pink": 1,
      "purple": 1,
      "orange": 1
    },
    "Fit": {
      "Extra Slim": 1,
      "Classic": 1
    },
    "collar_uFilter": {
      "Buttondown": 2
    },
    "trend_uFilter": {
      "Wraps & Ties": 3,
      "Corseting": 2,
      "Cozy": 2,
      "Crop Top": 1
    },
    "pattern_uFilter": {
      "Graphics": 6,
      "Solid": 3
    },
    "heelHeight_uFilter": {
      "Flat": 2,
      "Mid": 2,
      "High": 1,
      "Low": 1
    }
  }


pop_filters = []

for facet in affinity:
    pop_filters.append(facet.keys()[0])
    pop_filters.append(facet.keys()[1])

print(pop_filters)