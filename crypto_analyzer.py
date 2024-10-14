import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import talib
from data_collector import DataCollector
from technical_analysis import TechnicalAnalysis
from machine_learning import MachineLearning

class CryptoAnalyzer:
    def __init__(self, exchange_id, symbol, timeframe='1h'):
        self.data_collector = DataCollector(exchange_id, symbol, timeframe)
        self.technical_analysis = TechnicalAnalysis()
        self.machine_learning = MachineLearning()
        self.symbol = symbol
        self.data = None
        self.predictions = None

    def fetch_data(self, start_date):
        self.data = self.data_collector.fetch_ohlcv(start_date)

    def analyze(self, start_date):
        self.fetch_data(start_date)
        self.data = self.technical_analysis.calculate_indicators(self.data)
        self.data = self.technical_analysis.identify_patterns(self.data)
        self.predict_prices()

    def predict_prices(self):
        X, y = self.machine_learning.prepare_data(self.data)
        self.machine_learning.build_model((X.shape[1], X.shape[2]))
        self.machine_learning.train_model(X, y)
        self.predictions = self.machine_learning.predict(X)

    def generate_report(self):
        report = f"Crypto Analysis Report for {self.symbol}\n"
        report += f"Date Range: {self.data.index[0]} to {self.data.index[-1]}\n\n"

        report += "Current Indicators:\n"
        report += f"Price: {self.data['close'].iloc[-1]:.2f}\n"
        report += f"RSI: {self.data['RSI'].iloc[-1]:.2f}\n"
        report += f"MACD: {self.data['MACD'].iloc[-1]:.2f}\n"
        report += f"Signal: {self.data['MACD_signal'].iloc[-1]:.2f}\n"

        report += "\nRecent Patterns:\n"
        for pattern in ['CDL2CROWS', 'CDL3BLACKCROWS', 'CDLENGULFING', 'CDLHAMMER', 'CDLMORNINGSTAR']:
            if self.data[pattern].iloc[-1] != 0:
                report += f"{pattern} detected\n"

        report += "\nPerformance Metrics:\n"
        initial_price = self.data['close'].iloc[0]
        final_price = self.data['close'].iloc[-1]
        total_return = (final_price - initial_price) / initial_price * 100
        report += f"Total Return: {total_return:.2f}%\n"

        # Calculate Sharpe Ratio
        returns = self.data['close'].pct_change().dropna()
        sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std()
        report += f"Sharpe Ratio: {sharpe_ratio:.2f}\n"

        # Calculate Maximum Drawdown
        cumulative_returns = (1 + returns).cumprod()
        max_drawdown = (cumulative_returns.cummax() - cumulative_returns).max()
        report += f"Maximum Drawdown: {max_drawdown:.2f}%\n"

        if self.predictions is not None:
            report += "\nPrice Prediction:\n"
            report += f"Next period: {self.predictions[-1][0]:.2f}\n"

        return report