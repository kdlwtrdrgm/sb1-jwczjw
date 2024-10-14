from flask import Flask, render_template, request, jsonify
from crypto_analyzer import CryptoAnalyzer
from config import DEFAULT_SYMBOL
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form.get('symbol', DEFAULT_SYMBOL)
        start_date = request.form.get('start_date', '2023-01-01')
        exchange = request.form.get('exchange', 'binance')
        timeframe = request.form.get('timeframe', '1h')

        analyzer = CryptoAnalyzer(exchange, symbol, timeframe)
        analyzer.analyze(start_date)
        report = analyzer.generate_report()

        # Generate interactive plot using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=analyzer.data.index, y=analyzer.data['close'], name='Close Price'))
        fig.add_trace(go.Scatter(x=analyzer.data.index, y=analyzer.data['MA20'], name='MA20'))
        fig.add_trace(go.Scatter(x=analyzer.data.index, y=analyzer.data['MA50'], name='MA50'))
        fig.update_layout(title=f'{symbol} Price and Moving Averages', xaxis_title='Date', yaxis_title='Price')
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('result.html', report=report, plot_json=plot_json)
    
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.json
    symbol = data.get('symbol', DEFAULT_SYMBOL)
    start_date = data.get('start_date', '2023-01-01')
    exchange = data.get('exchange', 'binance')
    timeframe = data.get('timeframe', '1h')

    analyzer = CryptoAnalyzer(exchange, symbol, timeframe)
    analyzer.analyze(start_date)
    report = analyzer.generate_report()

    return jsonify({"report": report, "data": analyzer.data.to_dict(orient='records')})

if __name__ == '__main__':
    app.run(debug=True)