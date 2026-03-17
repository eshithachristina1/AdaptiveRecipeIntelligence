import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re

st.title("🍲 Adaptive Recipe Intelligence")
st.write("Adapt recipes based on dietary restrictions while maintaining similar nutrition.")

# -----------------------------
# Nutrition Database
# -----------------------------

nutrition_db = {

"chicken breast":{"calories":165,"protein":31,"fat":3.6},
"mushrooms":{"calories":22,"protein":3.1,"fat":0.3},
"flour":{"calories":364,"protein":10,"fat":1},
"almond flour":{"calories":579,"protein":21,"fat":53},
"butter":{"calories":717,"protein":0.8,"fat":81},
"olive oil":{"calories":884,"protein":0,"fat":100},
"egg noodles":{"calories":210,"protein":8,"fat":2},
"gluten-free noodles":{"calories":350,"protein":7,"fat":2},
"carrots":{"calories":41,"protein":0.9,"fat":0.2},
"celery":{"calories":16,"protein":0.7,"fat":0.2},
"onion":{"calories":40,"protein":1.1,"fat":0.1},
"vegetable broth":{"calories":15,"protein":1,"fat":0}

}

# -----------------------------
# Substitution Rules
# -----------------------------

substitution_rules = {

"Vegetarian":{
"chicken breast":"mushrooms"
},

"Vegan":{
"butter":"olive oil",
"chicken breast":"mushrooms"
},

"Gluten-free":{
"flour":"almond flour",
"egg noodles":"gluten-free noodles"
},

"Low-fat":{
"butter":"olive oil"
}

}

# -----------------------------
# Ingredient Extraction
# -----------------------------

def extract_ingredients(recipe):

    ingredients=[]

    recipe=recipe.lower()

    for item in nutrition_db:

        if item in recipe:

            ingredients.append(item)

    return ingredients


# -----------------------------
# Nutrition Calculation
# -----------------------------

def calculate_nutrition(ingredients):

    total={"calories":0,"protein":0,"fat":0}

    for ing in ingredients:

        if ing in nutrition_db:

            for n in total:

                total[n]+=nutrition_db[ing][n]

    return total


# -----------------------------
# Ingredient Substitution
# -----------------------------

def substitute_ingredients(ingredients,diet):

    new_ingredients=[]
    substitutions=[]

    rules=substitution_rules.get(diet,{})

    for ing in ingredients:

        if ing in rules:

            new_ing=rules[ing]

            new_ingredients.append(new_ing)

            substitutions.append((ing,new_ing))

        else:

            new_ingredients.append(ing)

    return new_ingredients,substitutions


# -----------------------------
# Nutrition Adjustment
# -----------------------------

def adjust_nutrition(original,adapted):

    adjusted=adapted.copy()

    for n in original:

        if adapted[n]!=0:

            factor=original[n]/adapted[n]

            adjusted[n]=adapted[n]*factor

    return adjusted


# -----------------------------
# Plot Nutrition
# -----------------------------

def plot_nutrition(original,adapted):

    nutrients=list(original.keys())

    orig=list(original.values())
    new=list(adapted.values())

    x=np.arange(len(nutrients))
    width=0.35

    fig,ax=plt.subplots()

    ax.bar(x-width/2,orig,width,label="Original")
    ax.bar(x+width/2,new,width,label="Adapted")

    ax.set_xticks(x)
    ax.set_xticklabels(nutrients)

    ax.set_title("Nutrition Comparison")

    ax.legend()

    return fig


# -----------------------------
# UI Inputs
# -----------------------------

recipe=st.text_area("Enter your recipe")

diet=st.selectbox(

"Select Dietary Restriction",

["Vegetarian","Vegan","Gluten-free","Low-fat"]

)

# -----------------------------
# Adapt Recipe Button
# -----------------------------

if st.button("Adapt Recipe"):

    if recipe=="":

        st.warning("Please enter a recipe")

    else:

        # Extract Ingredients
        original_ingredients=extract_ingredients(recipe)

        # Substitute Ingredients
        new_ingredients,subs=substitute_ingredients(original_ingredients,diet)

        # Nutrition
        original_nutrition=calculate_nutrition(original_ingredients)
        adapted_nutrition=calculate_nutrition(new_ingredients)

        # Adjust nutrition
        adjusted_nutrition=adjust_nutrition(original_nutrition,adapted_nutrition)

        # -----------------------------
        # Show Adapted Recipe
        # -----------------------------

        st.subheader("🍽 Adapted Ingredients")

        for i in new_ingredients:

            st.write(i)

        # -----------------------------
        # Substitution Explanation
        # -----------------------------

        st.subheader("🔄 Ingredient Substitutions")

        if subs:

            for old,new in subs:

                st.write(f"{old} → {new} (to satisfy {diet} diet)")

        else:

            st.write("No substitutions required.")

        # -----------------------------
        # Nutrition
        # -----------------------------

        st.subheader("🥗 Nutritional Information")

        st.write("Original Recipe")

        st.json(original_nutrition)

        st.write("Adapted Recipe")

        st.json(adjusted_nutrition)

        # -----------------------------
        # Plot
        # -----------------------------

        fig=plot_nutrition(original_nutrition,adjusted_nutrition)

        st.pyplot(fig)
