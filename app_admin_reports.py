import gradio as gr
import pandas as pd
import numpy as np
import requests

from ui_fast_utils import get_authorization_header, BACKEND_URL

simple = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=9, freq='D').strftime("%d"),
    'Average number of inferences': np.interp([28, 55, 43, 91, 81, 53, 19, 87, 52], [19, 91], [5, 20])
})


import random

increasing_sequence = [random.randint(1, 50) for _ in range(100)]

# random_numbers = [random.randint(1, 10) for _ in range(100)]

# Rearrange the numbers in decreasing zigzag order
# random_numbers = np.array(random_numbers)
# random_numbers = np.sort(random_numbers)[::-1]
# random_numbers[1::2] = random_numbers[1::2][::-1]
decreasing_sequence = [(50 - el) // 10 + random.randint(0, 3) for el in increasing_sequence]
simple5 = pd.DataFrame({
    'Total number of predictions': increasing_sequence,
    'Daily number of predictions': decreasing_sequence
})

seq1 = [3 + random.randint(el//10, 10 + el//10) for el in range(100)]
seq2 = [30 + random.randint(0, 20 + el//10) for el in range(100)]
simple2 = pd.DataFrame({
    'Instances': list(range(100)) + list(range(100)),
    'Number': seq1 + seq2,
    'Data description': ["Number of requests in queue"] * 100 + ["Number of seconds per one inference"] * 100
})

def find_reports(request: gr.Request):
    header = get_authorization_header(request)
    data = requests.get('http://localhost:7246/reports', headers=header)
    return pd.DataFrame.from_dict(data.json())

def create_demo():
    with gr.TabItem(id=0, label='Maintenance Status') as demo:

        button = gr.Button("Generate Report!", variant='primary')
        with gr.Row():
            barplot = gr.BarPlot(
                simple,
                x="Date",
                y="Average number of inferences",
                title="Average number of inference requests per day",
                tooltip=['Date', 'Average number of inferences'],
                y_lim=[0, 25],
                height=512,
                width=512,
            )
            gr.LinePlot(
                simple2,
                x="Instances",
                y="Number",
                title="Rate of inference time compared to number of requests",
                tooltip=['Instances', 'Number', 'Data description'],
                color='Data description',
                y_lim=[0, 100],
                height=512,
                width=512,
            )
        gr.ScatterPlot(
            simple5,
            x="Total number of predictions",
            y="Daily number of predictions",
            title="Daily activity in relation to total activity",
            tooltip=['Total number of predictions', 'Daily number of predictions'],
            y_lim=[-1, 11],
            height=512,
            width=512
        )
        button.click(find_reports, inputs=[], outputs=[barplot])

    return demo
