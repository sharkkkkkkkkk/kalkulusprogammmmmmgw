# Framework that creates the app
import streamlit as st

# Parser that correct the users writing
from sympy.parsing.sympy_parser import parse_expr

# Plotting library from sympy
from sympy.plotting.plot import plot

# All the letters as symbols
from sympy.abc import *

# Makes the algebraic computation
import sympy as sp

# Plot the functions
import matplotlib as mpl
import matplotlib.pyplot as plt

# Numerical calculations for the plot
import numpy as np

# ------------- CONFIGURATIONS -----------------

# Set matplotlib parameters to default
mpl.rcParams.update(mpl.rcParamsDefault)
mpl.rcParams.update({"font.family": "serif"})


# Set the configuration of the page with TITLE and ICON
st.set_page_config(
    page_title="FUNGSI",
    page_icon="👨‍🏫",
)

# ----------- TEXT PARAMETERS -----------------
# Write down the function you want to analyze and press ENTER
txt_input = "Ketik untuk menganalis. Kamu bisa menggunakan variabel x, y dan z"


# ----------- INITIALIZE SESSION STATES --------------

if 'function_input' not in st.session_state:
    st.session_state['function_input'] = "x^2 + exp(x)"

if 'x_lim_inf' not in st.session_state:
    st.session_state['x_lim_inf'] = -10.0

if 'x_lim_sup' not in st.session_state:
    st.session_state['x_lim_sup'] = 10.0

if 'integral_variable' not in st.session_state:
    st.session_state['integral_variable'] = "x"

if 'integral_lower_limit' not in st.session_state:
    st.session_state['integral_lower_limit'] = "0"

if 'integral_upper_limit' not in st.session_state:
    st.session_state['integral_upper_limit'] = "1"


st.title("Calculus Calculator")

# ------------- GET USER INPUT ------------------------
with st.form("Masukkan"):
    st.write(txt_input)
    function_input = st.text_input(txt_input, key="function_input", label_visibility="collapsed")    
    submitted = st.form_submit_button("Masukkan")


# ------------- OPERATIONS WITH THE INPUT -------------------
# Parse the string of the raw input and convert to latex
function_parsed = parse_expr(function_input, transformations='all')
function_latex = sp.latex(function_parsed)

# Derivative with respect to x and convert to latex
derivative = sp.diff(function_parsed, x)
derivative_latex = sp.latex(derivative)

# Integral of the function with respect to x and convert to latex
integral_variable = parse_expr(st.session_state['integral_variable'], transformations='all')
function_integrated = sp.integrate(function_parsed, integral_variable)
integral_expression = sp.latex(sp.Integral(function_parsed, integral_variable))
integral_latex = sp.latex(function_integrated)

integral_lower_limit_parsed = parse_expr(st.session_state['integral_lower_limit'], transformations='all')
integral_upper_limit_parsed = parse_expr(st.session_state['integral_upper_limit'], transformations='all')
integral_with_limits_expression = sp.latex(sp.Integral(function_parsed, (integral_variable, integral_lower_limit_parsed, integral_upper_limit_parsed)))
integral_with_limits_value = sp.integrate(function_parsed, (integral_variable, integral_lower_limit_parsed, integral_upper_limit_parsed))

# Get the values of the session state
plot_min_x = st.session_state["x_lim_inf"]
plot_max_x = st.session_state["x_lim_sup"]

# Create a list of numbers from the limits of the plot
x_values = np.linspace(plot_min_x, plot_max_x, 640)

# Create a numeric function from the symbolic function parsed
function_numpy = sp.lambdify(x, function_parsed, "numpy")

# Create a list of the y_values for this function
y_values = function_numpy(x_values)


def derivative_to_input():
    st.session_state['function_input'] = str(derivative)

def integral_to_input():
    st.session_state['function_input'] = str(function_integrated)

# ------------ SHOW RESULTS INTO TABS --------------------

tab_function, tab_derivative, tab_integral, tab_plot = st.tabs(["Function", "Derivative", "Integral", "Plot"])

# Show the function parsed
with tab_function:
    st.latex(r'''f(x)=''' + function_latex)



# Show the derivative
with tab_derivative:
    st.latex(r'''\frac{d}{dx} \left(''' + function_latex + r'''\right) = ''')
    st.latex(derivative_latex)

    st.button("Use the derivative as input", key="derivative_into_input_button", on_click=derivative_to_input)


# Show the integral
with tab_integral:
    st.latex(integral_expression + r'''=''')
    st.latex(integral_latex)

    st.button("Use the integral as input", key="integral_into_input_button", on_click=integral_to_input)
    with st.form("integral_parameters"):

        st.write("Definite Integral")
        st.latex(integral_with_limits_expression + r'''=''')
        st.latex(integral_with_limits_value)

        col1, col2, col3, col4 = st.columns(4)

        with col1: 
            integral_variable = st.text_input("Variable", key="integral_variable")
        with col2:
            integral_lower_limit = st.text_input("Integral Lower Limit", key="integral_lower_limit")
        with col3:
            integral_upper_limit = st.text_input("Integral Upper Limit", key="integral_upper_limit")
        with col4:
            st.write("")
            st.write("")
            integral_parameters_submitted = st.form_submit_button("Submit")
    
# Plot the function
with tab_plot:
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values)
    ax.set(xlabel='$x$', ylabel='$f(x)$')
    ax.grid()
    st.latex(r'''f(x)=''' + function_latex)
    st.pyplot(fig)

    # Change the values of the plot range
    with st.form("plot_range"):
        st.write("Set the minimum and maximum values of the plot")
        col1, col2, col3 = st.columns([3,3,1], gap="small")

        with col1:
            x_lim_inf = st.number_input("x inferior limit", key="x_lim_inf", label_visibility="collapsed")
        
        with col2:
            x_lim_sup = st.number_input("x superior limit", key="x_lim_sup", label_visibility="collapsed")
        
        with col3:
            x_limits_submitted = st.form_submit_button("Submit")

st.write("")
st.caption("GABUTTTTTTTTTTTTTTTTTTTTTTTTT")
