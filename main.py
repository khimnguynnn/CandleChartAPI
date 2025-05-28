from flask import Flask, send_file
import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)


@app.route('/currencies/<symbol>')
def get_area_chart(symbol):
    interval = '1m'
    limit = 60

    url = "https://fapi.binance.com/fapi/v1/klines"
    params = {
        'symbol': symbol.upper(),
        'interval': interval,
        'limit': limit
    }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        return {"error": "Binance API failed"}, 500

    data = res.json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['timestamp'] = df['timestamp'].dt.tz_localize(
        'UTC').dt.tz_convert('Asia/Bangkok')
    df['close'] = df['close'].astype(float)

    # Vẽ biểu đồ line chart vùng
    fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
    ax.plot(df['timestamp'], df['close'], color='#00b386', linewidth=1.5)
    ax.set_ylim(df['close'].min() * 0.995, df['close'].max() * 1.005)
    ax.fill_between(df['timestamp'], df['close'], color='#00b386', alpha=0.2)
    ax.set_title(f"{symbol.upper()} Price - 1m (Last 1 hour)", fontsize=14)
    ax.set_ylabel("Price (USDT)")
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Trả ảnh PNG
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close(fig)
    return send_file(buffer, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
