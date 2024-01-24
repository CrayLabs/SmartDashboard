# BSD 2-Clause License
#
# Copyright (c) 2021-2024, Hewlett Packard Enterprise
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import pathlib

import streamlit as st

from smartdashboard.utils.pageSetup import local_css, set_streamlit_page_config

set_streamlit_page_config()

curr_path = pathlib.Path(os.path.abspath(__file__)).parent.parent
local_css(str(curr_path / "static/style.css"))

st.header("Welcome to the SmartSim Dashboard Help Page")
st.write("")
st.markdown("""We're here to guide you through the features and functionalities
      of the SmartSim Dashboard,
    designed to enhance your experience with simulation
    experiments. This guide will help
    you navigate through the dashboard, understand its capabilities,
    and make the most of its powerful features.""")
st.write("")

with st.expander(label="Experiment Overview"):
    st.markdown("""Discover comprehensive insights about your experiment's
        entities within the Experiment Overview section.
        Get access to configuration details, comprehensive logs,
        real-time statuses, and relevant information regarding any
        colocated databases, if applicable.
        """)
    st.markdown("""
        To access detailed information about experiments, models, orchestrators,
        and ensembles, please refer to their respective documentation pages below:
        - [Experiments](https://www.craylabs.org/docs/experiment.html#)
        - [Models](https://www.craylabs.org/docs/experiment.html#model)
        - [Orchestrators](https://www.craylabs.org/docs/orchestrator.html)
        - [Ensembles](https://www.craylabs.org/docs/experiment.html#ensemble)""")

st.write("")

with st.expander(label="Support"):
    st.markdown("""Should you encounter any issues or require assistance while
        using the SmartSim Dashboard, we're here to help!""")
    st.markdown("""The complete SmartSim documentation can be found
        [here](https://www.craylabs.org/docs/overview.html).
        You can also contact us at craylabs@hpe.com.""")
