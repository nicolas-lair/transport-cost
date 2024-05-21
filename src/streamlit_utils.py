from typing import Any
import streamlit as st

from src.cost_calculator import MultiRefExpedition, SingleRefExpedition
from src.constant import BOTTLE, MAGNUM, Package
from src.app_generics.postal_code import get_postal_code_list
from src.departement import DEPARTMENTS_TO_CODE
from my_transporters import StefApp


COST_CALCULATOR = {
    "Stef": StefApp(),
    # "Chronopost": ChronopostApp(),
}


def init_session_state(var_name: str, init_value: Any = None):
    if st.session_state.get(var_name) is None:
        st.session_state[var_name] = init_value


@st.cache_data
def retrieve_postal_code():
    return get_postal_code_list()


@st.experimental_fragment
def define_style():
    st.markdown(
        """
    <style>
    .mid-font {
        font-size:25px;
        text-align: center
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <style>
    .big-font {
        font-size:50px !important;
        text-align: center
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def cost_calculator_callback():
    st.session_state.cost_calculator = COST_CALCULATOR[st.session_state.transporter]


def cost_callback():
    st.session_state.department = st.session_state.postal_code[:2]
    st.session_state.expedition = MultiRefExpedition(
        [
            SingleRefExpedition(
                n_bottles=st.session_state.bottle, bottle_type=BOTTLE, package=Package()
            ),
            SingleRefExpedition(
                n_bottles=st.session_state.magnum, bottle_type=MAGNUM, package=Package()
            ),
        ]
    )
    st.session_state.detail_cost = st.session_state.cost_calculator.compute_cost()
    st.session_state.cost = round(sum(st.session_state.detail_cost.values(), 0), 2)


def bottle_input():
    (
        col1,
        col2,
    ) = st.columns([0.25, 0.25])
    with col1:
        st.number_input(
            "Bouteilles (75 cL)",
            min_value=0,
            max_value=198,
            value="min",
            step=1,
            on_change=cost_callback,
            key="bottle",
        )
    with col2:
        st.number_input(
            "Magnums (1.5 L)",
            min_value=0,
            max_value=100,
            value="min",
            step=1,
            on_change=cost_callback,
            key="magnum",
        )


def destination_city_input(df_postal_code):
    if len(df_postal_code) != 0:
        (
            commune_col,
            dept_col,
        ) = st.columns([0.7, 0.3])
        with commune_col:
            st.selectbox(
                "Destination",
                options=df_postal_code.full_name.values,
                key="postal_code",
                on_change=cost_callback,
            )
        with dept_col:
            st.text_input(
                "Département",
                value=DEPARTMENTS_TO_CODE[st.session_state.department],
                disabled=True,
            )


def input_factor(
    indicator,
    name,
    modulation_link: str,
    min_value: float,
    max_value: float,
    input_format: str,
    **kwargs,
):
    col1, col2 = st.columns([0.2, 0.5])
    with col2:
        st.text("")
        if not indicator.retrieved:
            st.error(f"Indicateur {name} non récupéré ! :disappointed:")
        elif not indicator.valid_date:
            st.warning(f"Indicateur {name} à vérifier ! :neutral_face:")
        else:
            st.success(f"Indicateur {name} récupéré !", icon="✅")
    with col1:
        st.number_input(
            f"Indice Coût {name} - [Source](%s)" % modulation_link,
            min_value=min_value,
            max_value=max_value,
            value=indicator.value,
            format=input_format,
            help="Récupéré automatiquement si possible",
            key=f"{name}_modulation",
            on_change=cost_callback,
        )


def display_result():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<p class="big-font">{st.session_state.cost} € HT</p>',
            unsafe_allow_html=True,
        )
    with col2:
        st.write(st.session_state.detail_cost)